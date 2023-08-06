# -*- coding:utf-8 -*-

import six
import re


__all__ = ['simple_pattern_to_regex', 'grep']


def simple_pattern_to_regex(pattern, sep_chars=None, keep_dots=False, strict=False):
    """simple_pattern_to_regex converts a simple pattern into a regex pattern.
    :param pattern: a curly-bracketed pattern, like str's named format pattern, e.g. '{dataset}/{varname}.csv'
    :param sep_chars: chars that is always considered as delimiters, e.g., "/" in file path. Default: None,
    :param keep_dots: if False, "." is converted to "\.". Default: False.
    :param strict: if True, add "^" and "$" to the begining and end of the pattern. Default: False
    :return: regex pattern, e.g. r"(?P<dataset>[^/]*)/(?P<varname>[^/]*)\.nc"
    """
    try:
        valid_char_pattern = r'[^{}]'.format(sep_chars) if sep_chars else r'.'
        re_pattern = re.sub(r'\{([a-zA-Z_][^:}]*)(:[^}]*)*\}', r'(?P<\1>{}*)'.format(valid_char_pattern), pattern)
        if re_pattern != pattern:
            if not keep_dots:
                if valid_char_pattern == r'.':
                    # this is an ugly fix, to make sure that '.' is replaced only in the raw pattern.
                    re_pattern = re.sub(r'\.', '\.', pattern)
                    re_pattern = re.sub(r'\{([a-zA-Z_][^:}]*)(:[^}]*)*\}', r'(?P<\1>{}*)'.format(valid_char_pattern), re_pattern)
                else:
                    re_pattern = re.sub(r'\.', '\.', re_pattern)

            if strict:
                re_pattern = '^' + re_pattern.lstrip('^')
                re_pattern = re_pattern.rstrip('$') + '$'
            return re_pattern
        else:
            return pattern
    except Exception as e:
        return pattern


def grep(pattern, seq, flags=0, parse_info=False):
    """grep greps patterns from seqs.
Parameters:
    pattern: a regex pattern (str or compiled), a simple pattern, or a function-like object that returns True/False or info dict.
    seq: seq of str or any other stuffs, etc. If pattern is not func and seq[0] is not str/unicode, seq will be converted using str() first.
    flags: 'ILMSUX' or number of re.I|re.L|re.M|re.S|re.U|re.X .
        I: ignore case;
        L: locale dependent;
        M: multi-line;
        S: dot matches all;
        U: unicode dependent;
        X: verbose.
    parse_info: whether to return parsed info (e.g., group info of regex, or the result of func-like pattern)
Returns:
    A filtered list of matched str or (matched_str, groupdict). The latter applies only when the pattern has groups.
    """
    if isinstance(pattern, six.string_types) and '(?P<' not in pattern:
        pattern = simple_pattern_to_regex(pattern)

    if isinstance(flags, six.string_types):
        true_flags = 0
        flags = flags.upper()
        for letter in flags:
            if letter in 'ILMSUX':
                true_flags += re.__dict__[letter]
    else:
        true_flags = flags

    res = []
    if isinstance(pattern, six.string_types + (type(re.compile(r'')),)):
        for item in seq:
            target = item if isinstance(item, six.string_types) else repr(item)
            m = re.search(pattern, target, true_flags)
            if not m:
                continue

            groupdict = m.groupdict().copy()
            groups = m.groups()
            groupdict.update(dict(zip(range(1, len(groups)+1), groups)))
            if parse_info:
                res.append((item, groupdict))
            else:
                res.append(item)
    elif callable(pattern):
        for item in seq:
            info = pattern(item)
            if info:
                if parse_info:
                    if not isinstance(info, dict):
                        res.append((item, {}))
                    else:
                        res.append((item, info))
                else:
                    res.append(item)

    return res
