import re
ENDING_ESCAPES = re.compile(r'\\+$')


def fold_lines(string):
    lines = []

    line = ''
    for raw_line in string.splitlines():
        raw_line = raw_line.lstrip()
        line += raw_line
        continues = ENDING_ESCAPES.search(raw_line)
        # an odd number of line escapes means this is a real
        # continuation character
        if not (continues and (len(continues.group()) % 2)):
            lines.append(line)
            line = ''
        elif continues:
            line = line[:-(len(raw_line) - continues.start())]

    if line or raw_line == line:
        lines.append(line)
    return lines


SEPS = '=:\s'
ESCAPE = r'\\'
_KEY = ('(', ESCAPE, '.',          # any escaped character is ok
        '|',                       # or
        '[^', ESCAPE, SEPS, ']+',  # anything that isn't one
                                   # of our key separators
        ')*')
KEY = re.compile(''.join(_KEY))

_VALUE = ('(?:',
          '(?:\s*=\s*)|(?:\s*:\s*)|\s*)',
          '(.*)')
VALUE = re.compile(''.join(_VALUE))

KEY_VALUE = re.compile(''.join(_KEY + _VALUE))


def parse_lines(string):
    kvs = {}

    for line in fold_lines(string):
        # keys start at first non-whitespace character on line...
        line = line.lstrip()
        # blank or comment; skip
        if not line or line.startswith(('#', '!')):
            continue

        m = KEY_VALUE.match(line)
        if not m:
            continue
        key, value = m.groups()
        kvs[key] = value or None

    return kvs
