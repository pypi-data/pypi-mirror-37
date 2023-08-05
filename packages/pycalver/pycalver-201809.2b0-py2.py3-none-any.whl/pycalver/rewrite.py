#!/usr/bin/env python
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
import io
import difflib
import logging
import typing as typ
from . import parse
log = logging.getLogger('pycalver.rewrite')


def rewrite(new_version, file_patterns, dry=False, verbose=False):
    new_version_nfo = parse.parse_version_info(new_version)
    new_version_fmt_kwargs = new_version_nfo._asdict()
    matches = None
    for filepath, patterns in file_patterns.items():
        with io.open(filepath, mode='rt', encoding='utf-8') as fh:
            content = fh.read()
        old_lines = content.splitlines()
        new_lines = old_lines.copy()
        matches = parse.parse_patterns(old_lines, patterns)
        for m in matches:
            replacement = m.pattern.format(**new_version_fmt_kwargs)
            span_l, span_r = m.span
            new_line = m.line[:span_l] + replacement + m.line[span_r:]
            new_lines[m.lineno] = new_line
        if dry or verbose:
            print('\n'.join(difflib.unified_diff(old_lines, new_lines,
                lineterm='', fromfile='a/' + filepath, tofile='b/' + filepath))
                )
        if dry:
            continue
        new_content = '\n'.join(new_lines)
        with io.open(filepath, mode='wt', encoding='utf-8') as fh:
            fh.write(new_content)
