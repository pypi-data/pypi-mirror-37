import out

import test_mod; test_mod  # pyflakes
print('-' * 50)

#~ ltd = out
#~ while ltd is not None:
    #~ print(f'  logger: {ltd.name}, level:{ltd.level}, id:{id(ltd)}, {ltd.handlers}')
    #~ ltd = ltd.parent


def test_it(full=True):

    out('no explicit level')
    out.trace('trace msg: %s', 'Absurdly voluminous details…')
    out.debug('debug message')
    out.info('info message - Normal feedback')
    out.note('note message - Important positive feedback to remember.')
    out.warn('warn message - Something to worry about.')

    if full:
        try:
            1/0
        except Exception as err:
            out.error('error message - Pow!')
            out.exception('exception message - Kerblooey!')
            out.exc('exc message - Kerblooey!')
            out.exc()

        out.critical('critical message - *flatline*')
        out.fatal('fatal message - *flatline*')
    print('-' * 50)


print()
out.configure(level='trace')
out.debug('version: %r', out.__version__)
test_it()
out.log_config()

out.configure(lexer='json')
out.debug('debug message: JSON: %s', '{"data": [null, true, false, "hi", 123]}')

out.configure(lexer='xml')
out.trace('debug message: XML: %s', '<foo><bar attr="woot">baz</bar></foo><!-- hi -->')

out.configure(lexer='python3')
out.note('debug message: PyON: %s # hi',
         {'data': [None, True, False, 'hi', 123]})
out.note('debug message2: PyON: %(data)s # hi',
         {'data': [None, True, False, 'hi', 123]})
#~ out.note('debug message: PyON: {} # hi',
         #~ {'data': [None, True, False, 'hi', 123]})  # Exception
#~ out.note('debug message: PyON: {} # hi', 1)
out.note('debug message: PyON: %s # hi', [1, 2, 3])


#~ if False:
if True:
    print()
    #~ out.configure(  # monochrome
        #~ style='mono',
        #~ msgfmt='{asctime}.{msecs:03.0f} {on}{levelname:<7} '
                #~ '{name}/{funcName}:{lineno} {message} {off}',
    #~ )
    #~ test_it()

    #~ print('Set to plain theme, with std formatter for modest speed boost:\n')
    out.configure(
        #~ theme='plain',
        theme='json',
    )
    out('no explicit level')
    out.trace('trace msg: %s', 'Absurdly voluminous details…')
    out.debug('debug message')

    #~ print('=========== APP OUTPUT ===========')
    #~ print('=========== APP OUTPUT ===========')
