import pytest
import propyties as p


@pytest.mark.parametrize('input,expected',
                         [('a', ['a']),
                          ('a\nb', ['a', 'b']),
                          ('a\\b', ['a\\b']),
                          ('a\\\nb', ['ab']),
                          ('a\\\\nb', ['a\\\\nb']),
                          ('a\\\n\n', ['a', ''])])  # splitlines keepends?
def test_fold_lines(input, expected):
    assert p.fold_lines(input) == expected


RAW_PROP = '''\
Truth = Beauty
# Comment 1
! Comment 2
  Truth:Beauty
 Truth                    :Beauty
fruits                           apple, banana, pear, \\
                                 cantaloupe, watermelon, \\
                                 kiwi, mango'''

PARSED_PROP = {u'Truth': u'Beauty',
               u'fruits': (u'apple, banana, pear, cantaloupe, '
                           u'watermelon, kiwi, mango')}


@pytest.mark.parametrize('input,expected',
                         [('a', {u'a': None}),
                          ('a\\t', {'a\\t': None}),
                          ('a=b\\\\\nc', {u'a': u'b\\\\', u'c': None}),
                          (RAW_PROP, PARSED_PROP)])
def test_parse_lines(input, expected):
    assert p.parse_lines(input) == expected
