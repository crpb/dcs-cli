# Copyright © 2015-2024 Jakub Wilk <jwilk@jwilk.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
colorful text printing
'''

import builtins
import re

class _seq:
    dim = '\33[90m'
    off = '\33[0m'
    bold = '\33[1m'
    yellow = '\33[33m'
    blue = '\33[34m'
    reverse = '\33[7m'
    unreverse = '\33[27m'

def _quote_unsafe_char(ch):
    if ch < ' ' or ch == '\x7F':
        s = '^' + chr(ord('@') ^ ord(ch))
    else:
        u = ord(ch)
        s = f'<U+{u:04X}>'
    t = _seq
    return f'{t.reverse}{s}{t.unreverse}'

def _quote_unsafe(s):
    return str.join('', map(_quote_unsafe_char, s))

def _quote(s):
    if not isinstance(s, str):
        return s
    chunks = re.split(r'([\x00-\x1F\x7F-\x9F]+)', s)
    def esc():
        for i, s in enumerate(chunks):
            if i & 1:
                yield _quote_unsafe(s)
            else:
                yield s
    return str.join('', esc())

def format(_s, **kwargs):
    kwargs.update(t=_seq)
    return _s.format_map({
        key: _quote(value)
        for key, value in kwargs.items()
    })

def print(_s='', **kwargs):
    builtins.print(format(_s, **kwargs))

__all__ = [
    'format',
    'print',
]

# vim:ts=4 sts=4 sw=4 et
