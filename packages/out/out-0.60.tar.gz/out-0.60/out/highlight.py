'''
    out - Simple logging with a few fun features.
    © 2018, Mike Miller - Released under the LGPL, version 3+.

    Highlighting with Pygments!
'''
from . import _CHOSEN_PALETTE


try:
    if _CHOSEN_PALETTE:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.token import (Keyword, Name, Comment, String, Error,
                                    Number, Operator, Generic, Token, Punctuation)

        if _CHOSEN_PALETTE in ('extended', 'truecolor'):
            from pygments.formatters import Terminal256Formatter
            from pygments.style import Style

            class AStyle(Style):
                styles = {
                    Token.String:           '#b52',  # orange, amber
                    Comment:                'italic #777',

                    Keyword:                'bold #ansiblue',
                    Keyword.Constant:       'nobold #ansiteal',
                    Number:                 '#ansidarkgreen',

                    Name.Tag:               '#ansipurple',
                    Name.Attribute:         '#ansipurple',
                    Punctuation:            'nobold #db5',
                }
            term_formatter = Terminal256Formatter(style=AStyle)

        elif _CHOSEN_PALETTE == 'basic':
            from pygments.formatters import TerminalFormatter

            TERMINAL_COLORS = {     # dark-bg      # light-bg
                Token:              ('',            ''),

                Comment:            ('darkgray',    'darkgray'),
                Comment.Preproc:    ('teal',        'turquoise'),

                Keyword.Constant:   ('teal',        'turquoise'),
                Keyword:            ('*darkblue*',   'blue'),
                Keyword.Type:       ('teal',        'turquoise'),
                Name.Attribute:     ('purple',    'fuchsia'),
                Name.Builtin.Pseudo:('teal',        'turquoise'),
                Name.Builtin:       ('teal',        'turquoise'),
                Name.Decorator:     ('fuchsia',     'purple'),
                Name.Exception:     ('teal',        'turquoise'),
                Name.Namespace:     ('',            ''),
                Name.Tag:           ('purple',    'fuchsia'),
                Name.Variable:      ('darkred',     'red'),
                Number:             ('darkgreen',     'green'),
                #~ Operator:           ('brown',      'yellow'),  # :-/
                Operator.Word:      ('*darkblue*',   'blue'),
                #~ Punctuation:        ('brown',      'yellow'),
                String:             ('purple',       'fuchsia'),

                Generic.Deleted:    ('darkred',     'red'),
                Generic.Inserted:   ('darkgreen',   'green'),
                Generic.Heading:    ('**',          '**'),
                Generic.Subheading: ('*purple*',    '*fuchsia*'),
                Generic.Error:      ('red',         'red'),
                Error:              ('_red_',       '_red_'),
            }
            term_formatter = TerminalFormatter(colorscheme=TERMINAL_COLORS)

    else:
        raise RuntimeError('color support not available.')

except (ImportError, RuntimeError):
    highlight = term_formatter = get_lexer_by_name = None
