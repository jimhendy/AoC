import re
import os


def run(inputs):

    # (?:^|\]) Start of line or outside [...] (non-capturing)
    # [a-z]*   Filler, lowercase letters (not [...])
    # (?P<a>[a-z]) Capture a group of single lowercase letter and call it "a"
    # (?P<b>...    Capture a group of single lowercase letter and call it "b"
    #       (?!    Negative look ahead
    #          (?P=a) Most recent match for group "a" (do not match the same letter twice)
    #                [a-z]) But do match any other lowercase letter
    # (?P=a) Then match group "a" again
    # etc.

    before_ssl = re.compile(
        "(?:^|\])[a-z]*(?P<a>[a-z])(?P<b>(?!(?P=a))[a-z])(?P=a).*\[[a-z]*(?P=b)(?P=a)(?P=b)[a-z]*\]"
    )
    after_ssl = re.compile(
        "\[[a-z]*(?P<a>[a-z])(?P<b>(?!(?P=a))[a-z])(?P=a)[a-z]*\].*(?P=b)(?P=a)(?P=b)[a-z]*(?:$|\[)"
    )

    total = 0
    for line in inputs.split(os.linesep):
        if len(before_ssl.findall(line)) or len(after_ssl.findall(line)):
            total += 1

    return total
