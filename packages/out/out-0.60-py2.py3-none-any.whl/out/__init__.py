'''
    out - Simple logging with a few fun features.
    © 2018, Mike Miller - Released under the LGPL, version 3+.

    TODO:
        Reverse ascii icon on Win10.
'''
import os
import sys
import logging
import traceback

from console.detection import is_a_tty, choose_palette, get_available_palettes
from console.style import ForegroundPalette, EffectsPalette

__version__ = '0.60'

# these vars need to be available for Formatter objects:
_out_file = sys.stderr
_is_a_tty = is_a_tty(_out_file)

def _find_palettes(stream):
    ''' Need to configure palettes manually, since we are checking stderr. '''
    chosen = choose_palette(stream=stream)
    palettes = get_available_palettes(chosen)
    fg = ForegroundPalette(palettes=palettes)
    fx = EffectsPalette(palettes=palettes)
    return fg, fx, chosen

fg, fx, _CHOSEN_PALETTE = _find_palettes(_out_file)

# now we're ready to import these:
from .format import (ColorFormatter as _ColorFormatter,
                     JSONFormatter as _JSONFormatter)
from .themes import themes as _themes, icons as _icons, styles as _styles


# Allow string as well as constant access.  More levels will be added below:
level_map = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'warning': logging.WARN,
    'err': logging.ERROR,
    'error': logging.ERROR,
    'critical': logging.FATAL,
    'fatal': logging.FATAL,
}


class Logger(logging.Logger):
    '''
        A singleton logger with centralized configuration.
    '''
    default_level = logging.INFO
    __path__ = __path__  # allows python3 -m out.demos to work
    __version__ = __version__  # make available

    def configure(self, **kwargs):
        ''' Convenience function to set a number of parameters on this logger
            and associated handlers and formatters.
        '''
        for kwarg in kwargs:
            value = kwargs[kwarg]

            if kwarg == 'level':
                self.set_level(value)

            elif kwarg == 'default_level':
                self.default_level = level_map.get(value, value)

            elif kwarg == 'datefmt':
                self.handlers[0].formatter.datefmt = value

            elif kwarg == 'msgfmt':
                self.handlers[0].formatter._style._fmt = value

            elif kwarg == 'stream':
                global fg, fx, _CHOSEN_PALETTE
                self.handlers[0].stream = value
                fg, fx, _CHOSEN_PALETTE = _find_palettes(value)

            elif kwarg == 'theme':
                if type(value) is str:
                    theme = _themes[value]
                    if value == 'plain':
                        fmtr =  logging.Formatter(style='{', **theme)
                    elif value == 'json':
                        fmtr =  _JSONFormatter(**theme)
                    else:
                        fmtr =  _ColorFormatter(tty=_is_a_tty, **theme)
                elif type(value) is dict:
                    if 'style' in value or 'icons' in value:
                        fmtr =  _ColorFormatter(tty=_is_a_tty, **theme)
                    else:
                        fmtr =  logging.Formatter(style='{', **theme)
                self.handlers[0].setFormatter(fmtr)

            elif kwarg == 'icons':
                if type(value) is str:
                    value = _icons[value]
                self.handlers[0].formatter._theme_icons = value

            elif kwarg == 'style':
                if type(value) is str:
                    value = _styles[value]
                self.handlers[0].formatter._theme_style = value

            elif kwarg == 'lexer':
                try:
                    self.handlers[0].formatter.set_lexer(value)
                except AttributeError as err:
                    self.error('lexer: ColorFormatter not available.')
            else:
                raise NameError('unknown keyword argument: %s' % kwarg)

    def log_config(self):
        ''' Log the current logging configuration. '''
        level = self.level
        debug = self.debug
        debug('Logging config:')
        debug('/ name: {}, id: {}', self.name, id(self))
        debug('  .level: %s (%s)', level_map_int[level], level)
        debug('  .default_level: %s (%s)',
                   level_map_int[self.default_level], self.default_level)

        for i, handler in enumerate(self.handlers):
            fmtr = handler.formatter
            debug('  + Handler: %s %r', i, handler)
            debug('    + Formatter: %r', fmtr)
            debug('      .datefmt: %r', fmtr.datefmt)
            debug('      .msgfmt: %r', fmtr._fmt)
            debug('      fmt_style: %r', fmtr._style)
            try:
                debug('      theme styles: %r', fmtr._theme_style)
                debug('      theme icons:\n%r', fmtr._theme_icons)
                debug('      lexer: %r\n', fmtr._lexer)
            except AttributeError:
                pass

    def setLevel(self, level):
        if type(level) is int:
            super().setLevel(level)
        else:
            self.setLevel(level_map.get(level, level))
    set_level = setLevel

    def __call__(self, message, *args):
        if self.isEnabledFor(self.default_level):
            self._log(self.default_level, message, args)


def add_logging_level(name, value, method_name=None):
    ''' Comprehensively adds a new logging level to the ``logging`` module and
        the currently configured logging class.

        Derived from: https://stackoverflow.com/a/35804945/450917
    '''
    if not method_name:
        method_name = name.lower()

    # set levels
    logging.addLevelName(value, name)
    setattr(logging, name, value)
    level_map[name.lower()] = value

    if value == getattr(logging, 'EXCEPT', None):  # needs traceback added
        def logForLevel(self, message='', *args, **kwargs):
            if self.isEnabledFor(value):
                message = (message + ' ▾\n').lstrip() + traceback.format_exc()
                self._log(value, message, args, **kwargs)
    else:
        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(value):
                self._log(value, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):  # may not need
        logging.log(value, message, *args, **kwargs)

    # set functions
    setattr(logging.getLoggerClass(), method_name, logForLevel)
    setattr(logging, method_name, logToRoot)


# re-configure root logger
out = logging.getLogger()   # root
out.name = 'main'
out.__class__ = Logger      # one way to add call()


# odd level numbers chosen to avoid commonly configured variations
add_logging_level('TRACE', 7)
add_logging_level('NOTE', 27)
add_logging_level('EXCEPT', logging.ERROR + 3, 'exc')
add_logging_level('FATAL', logging.FATAL)
level_map_int = {
    val: key
    for key, val in level_map.items()
}
out.warn = out.warning  # fix warn
out.set_level('note')


# handler/formatter
_handler = logging.StreamHandler(stream=_out_file)
_theme_name = 'interactive' if _is_a_tty else 'production'
if os.environ.get('TERM') == 'linux':
    _theme_name = 'linux_' + _theme_name
if os.name == 'nt':
    _theme_name = 'windows_' + _theme_name
_formatter = _ColorFormatter(hl=bool(_CHOSEN_PALETTE), **_themes[_theme_name])
_handler.setFormatter(_formatter)
out.addHandler(_handler)

# save original module for later, in case it's needed.
out._module = sys.modules[__name__]

# Wrap module with instance for direct access
sys.modules[__name__] = out
