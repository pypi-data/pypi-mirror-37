# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://github.com/mbarkhau/pycalver
#
# (C) 2018 Manuel Barkhau (@mbarkhau)
# SPDX-License-Identifier: MIT

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import re
import logging
import typing as typ
import pkg_resources
str = getattr(__builtins__, 'unicode', str)
log = logging.getLogger('pycalver.parse')
VALID_RELESE_VALUES = 'alpha', 'beta', 'dev', 'rc', 'post'
PYCALVER_RE = re.compile(
    """
\\b
(?P<version>
    (?P<calver>
       v                        # "v" version prefix
       (?P<year>\\d{4})
       (?P<month>\\d{2})
    )
    (?P<build>
        \\.                      # "." build nr prefix
        \\d{4,}
    )
    (?P<release>
        \\-                      # "-" release prefix
        (?:alpha|beta|dev|rc|post)
    )?
)(?:\\s|$)
"""
    , flags=re.VERBOSE)
RE_PATTERN_PARTS = {'pep440_version':
    '\\d{6}\\.[1-9]\\d*(a|b|dev|rc|post)?\\d*', 'version':
    'v\\d{6}\\.\\d{4,}(\\-(alpha|beta|dev|rc|post))?', 'calver': 'v\\d{6}',
    'build': '\\.\\d{4,}', 'release': '(\\-(alpha|beta|dev|rc|post))?'}
PatternMatch = typ.NamedTuple('PatternMatch', [('lineno', int), ('line',
    str), ('pattern', str), ('span', typ.Tuple[int, int]), ('match', str)])
VersionInfo = typ.NamedTuple('VersionInfo', [('pep440_version', str), (
    'version', str), ('calver', str), ('year', str), ('month', str), (
    'build', str), ('release', typ.Optional[str])])


def parse_version_info(version):
    match = PYCALVER_RE.match(version)
    if match is None:
        raise ValueError('Invalid pycalver: {0}'.format(version))
    pep440_version = str(pkg_resources.parse_version(version))
    return VersionInfo(pep440_version=pep440_version, **match.groupdict())


def iter_pattern_matches(lines, pattern):
    pattern_re = re.compile(pattern.replace('\\', '\\\\').replace('-',
        '\\-').replace('.', '\\.').replace('+', '\\+').replace('*', '\\*').
        replace('[', '\\[').replace('(', '\\(').format(**RE_PATTERN_PARTS))
    for lineno, line in enumerate(lines):
        match = pattern_re.search(line)
        if match:
            yield PatternMatch(lineno, line, pattern, match.span(), match.
                group(0))


def parse_patterns(lines, patterns):
    all_matches = []
    for pattern in patterns:
        all_matches.extend(iter_pattern_matches(lines, pattern))
    return all_matches
