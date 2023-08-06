# -*- coding: utf-8 -*-
# Copyright (c) 2018  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Chenxiong Qi <cqi@redhat.com>
#            Qixiang Wan <qwan@redhat.com>

""" Various utilities """
import os
import re
import gi
gi.require_version('Modulemd', '1.0')  # noqa
from gi.repository import Modulemd

from jinja2 import Environment, PackageLoader
from ursa_major.logger import log


def validate_mail_address(addr):
    """
    Validate e-mail address format.
    """

    mail_pattern = r"^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$"
    match = re.match(mail_pattern, addr)
    if match:
        return True

    log.error("E-mail address <%s> is not valid.", addr)
    return False


def jinja2_env(category):
    env = Environment(
        loader=PackageLoader("ursa_major", "templates/" + category)
    )

    def regex_replace(s, find, replace):
        return re.sub(find, replace, s)
    env.filters['regex_replace'] = regex_replace

    return env


def get_env_var(var, raise_if_not_exist=False):
    """
    Get variable value from os environ

    :param raise_if_not_exist: If true, raise ValueError when variable is
        not present in os environ, otherwise return None.
    """
    if var not in os.environ and raise_if_not_exist:
        raise ValueError("ENV variable '{}' does not exist.".format(var))
    return os.environ.get(var, None)


def load_mmd(yaml, is_file=False):
    """ Create Modulemd.Module object from string or file and return. """
    try:
        if is_file:
            mmd = Modulemd.Module().new_from_file(yaml)
        else:
            mmd = Modulemd.Module().new_from_string(yaml)
        # If the modulemd was v1, it will be upgraded to v2
        mmd.upgrade()
    except Exception:
        error = 'Invalid modulemd: {0}'.format(yaml)
        log.error(error)
        raise

    return mmd


def mmd_has_requires(mmd, requires):
    """
    Check whether a module represent by the mmd has requires.

    :param mmd: Modulemd.Module object
    :param requires: dict of requires, example:
        {'platform': 'f28', 'python3': 'master'}
    """
    deps_list = mmd.peek_dependencies()
    mmd_requires = deps_list[0].peek_requires() if deps_list else {}

    neg_reqs = pos_reqs = []
    for req_name, req_streams in requires.items():
        if req_name not in mmd_requires.keys():
            return False

        if not(isinstance(req_streams, list)):
            req_streams = [req_streams]

        streams = mmd_requires[req_name].dup()
        neg_reqs = [s[1:] for s in req_streams if s.startswith('-')]
        pos_reqs = [s for s in req_streams if not s.startswith('-')]

        # TODO: can mmd contains negative requires like
        # {'platform': ['-f26']} ?
        if set(streams) & set(neg_reqs):
            return False
        if pos_reqs and not (set(streams) & set(pos_reqs)):
            return False
    return True
