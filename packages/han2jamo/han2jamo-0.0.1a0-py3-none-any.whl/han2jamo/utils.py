from __future__ import unicode_literals
import six
import functools
import sys


def to_unichr(x):
    return six.unichr(x)


def __items(x):
    return six.iteritems(x)


if sys.version_info[0] <= 2:
    import codecs


    def __u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def __u(x):
        return x

TYPE_INITIAL = 0x001
TYPE_MEDIAL = 0x010
TYPE_FINAL = 0x100

INITIALS = list(map(to_unichr, [0x3131, 0x3132, 0x3134, 0x3137, 0x3138, 0x3139,
                                0x3141, 0x3142, 0x3143, 0x3145, 0x3146, 0x3147,
                                0x3148, 0x3149, 0x314a, 0x314b, 0x314c, 0x314d,
                                0x314e]))

MEDIALS = list(map(to_unichr, [0x314f, 0x3150, 0x3151, 0x3152, 0x3153, 0x3154,
                               0x3155, 0x3156, 0x3157, 0x3158, 0x3159, 0x315a,
                               0x315b, 0x315c, 0x315d, 0x315e, 0x315f, 0x3160,
                               0x3161, 0x3162, 0x3163]))

FINALS = list(map(to_unichr, [0x3131, 0x3132, 0x3133, 0x3134, 0x3135, 0x3136,
                              0x3137, 0x3139, 0x313a, 0x313b, 0x313c, 0x313d,
                              0x313e, 0x313f, 0x3140, 0x3141, 0x3142, 0x3144,
                              0x3145, 0x3146, 0x3147, 0x3148, 0x314a, 0x314b,
                              0x314c, 0x314d, 0x314e]))

CHAR_LISTS = {TYPE_INITIAL: INITIALS, TYPE_MEDIAL: MEDIALS, TYPE_FINAL: FINALS}
CHAR_SETS = dict(map(lambda x: (x[0], set(x[1])), __items(CHAR_LISTS)))
CHARSET = functools.reduce(lambda x, y: x.union(y), CHAR_SETS.values(), set())
CHAR_INDICES = dict(
    map(lambda x: (x[0], dict([(c, i) for i, c in enumerate(x[1])])),
        __items(CHAR_LISTS)))


def check_syllable(x):
    return 0xAC00 <= ord(x) <= 0xD7A3


def jamo_type(x):
    t = 0x000

    for type_code, jamo_set in __items(CHAR_SETS):
        if x in jamo_set:
            t |= type_code

    return t
