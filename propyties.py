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


def parse_lines(string):
    kvs = {}

    for line in fold_lines(string):
        preceding_backslash = False
        # keys start at first non-whitespace character on line...
        line = line.decode('unicode-escape').lstrip()
        # blank or comment; skip
        if not line or line.startswith(('#', '!')):
            continue

        has_sep = False
        key_len = 0

        for key_len, c in enumerate(line):
            if c in (':', '=') and not preceding_backslash:
                has_sep = True
                break
            elif c in (' ', '\t', '\f') and not preceding_backslash:
                break
            if c == '\\':
                preceding_backslash = not preceding_backslash
            else:
                preceding_backslash = False
        else:
            key_len += 1

        value_start = len(line) - 1
        for value_start, c in enumerate(line[key_len + 1:], key_len):
            if c not in (' ', '\t', '\f'):
                if not has_sep and c in ('=', ':'):
                    has_sep = True
                else:
                    break

        key, value = line[:key_len], line[value_start + 1:]
        kvs[key] = value or None

    return kvs
