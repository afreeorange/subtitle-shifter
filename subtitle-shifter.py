"""
Quick script to offset subtitles in .srt files. Didn't
Google first to realize that this exists:

https://github.com/byroot/pysrt

Oh well.
"""

import re
import sys

TIME_REGEX = '(\d{2})\:(\d{2})\:(\d{2})\,(\d{3})'
DURATION_REGEX = re.compile(f'{TIME_REGEX}\s\-\->\s{TIME_REGEX}')


def __to_milliseconds(srt_timestamp_iterable):
    """
    Convert an interable of the form (hh, mm, ss, ms) to milliseconds.
    All values provided must be integers.
    """
    return  srt_timestamp_iterable[0] * 60 * 60 * 1000 + \
            srt_timestamp_iterable[1] * 60 * 1000 + \
            srt_timestamp_iterable[2] * 1000 + \
            srt_timestamp_iterable[3]


def __to_timestamp(milliseconds):
    """
    Convert milliseconds to an SRT timestamp format of the form
    hh:mm:ss,ms
    """
    hh =  milliseconds // (60 * 60 * 1000)
    mm = (milliseconds % (60 * 60 * 1000)) // (60 * 1000)
    ss = (milliseconds % (60 * 1000)) // (1000)
    ms =  milliseconds % 1000

    return f'{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}'


def shift_subtitles(subtitles_file, offset):
    """
    Shift subtitles!
    """
    subtitles_list = [_.strip() for _ in open(subtitles_file).readlines()]

    for _ in subtitles_list:
        matches = re.match(DURATION_REGEX, _)

        if matches:
            groups = [int(__) for __ in matches.groups()]

            print(
                __to_timestamp(__to_milliseconds(groups[0:4]) + offset),
                '-->',
                __to_timestamp(__to_milliseconds(groups[4:]) + offset),
            )
        else:
            print(_)


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        offset = int(sys.argv[2])
    except Exception:
        print('Usage: subtitle-shifter.py <srt file> <offset in milliseconds>')
    else:
        shift_subtitles(filename, offset)
