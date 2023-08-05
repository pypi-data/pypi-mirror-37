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
import logging
import typing as typ
import datetime as dt
from . import lex_id
from . import parse
log = logging.getLogger('pycalver.version')


def current_calver():
    return dt.date.today().strftime('v%Y%m')


def bump(old_version, **kwargs):
    release = kwargs.get('release', None)
    old_ver = parse.parse_version_info(old_version)
    new_calver = current_calver()
    if old_ver.calver > new_calver:
        log.warning("'version.bump' called with '{0}', ".format(old_version
            ) + 'which is from the future, '.format() +
            'maybe your system clock is out of sync.'.format())
        new_calver = old_ver.calver
    new_build = lex_id.next_id(old_ver.build[1:])
    new_release = None
    if release is None:
        if old_ver.release:
            new_release = old_ver.release[1:]
        else:
            new_release = None
    elif release == 'final':
        new_release = None
    else:
        new_release = release
    new_version = new_calver + '.' + new_build
    if new_release:
        new_version += '-' + new_release
    return new_version
