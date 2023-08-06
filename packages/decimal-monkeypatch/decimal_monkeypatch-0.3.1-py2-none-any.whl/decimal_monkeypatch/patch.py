from __future__ import print_function, division


def autowrapt_decimal(_module):
    import sys
    import cdecimal

    sys.modules['decimal'] = cdecimal
    print('module decimal patched to {}'.format(sys.modules['decimal'].__name__))
    cdecimal.tmp_context = cdecimal.Context

    def patched(*args, **kwargs):
        if 'rounding' in kwargs and kwargs['rounding'] is None:
            kwargs['rounding'] = 6
        return cdecimal.tmp_context(*args, **kwargs)
    cdecimal.Context = patched

    print('cdecimal.Context monkey-patch for boto(if rounding=None, then 6 passed to Context instead) applied\n')


def autowrapt_psycopg2(module):
    import ujson
    if module.__name__ == 'psycopg2._json':
        module.json = ujson
    else:
        module._json.json = ujson
    print('psycopg2._json.json monkey-patched to ujson instead of json\n')

