# -*- coding: utf-8 -*-
"""sconstool.cxxtestgen.detail_

Implementation details for cxxtestgen tool.
"""

#
# Copyright (c) 2018 Paweł Tomulik
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
import os
import re

try:
    from site_tools.util import ToolFinder, Selector
except ImportError:
    from sconstool.util import ToolFinder, Selector


__all__ = ('ToolFinder',
           'Selector',
           'findCxxTestGen',
           'findCxxTestGenPython',
           'shallWorkOnPy3')


def findCxxTestGen(env):
    return _cxxTestGenFinder(env)


def findCxxTestGenPython(env, cxxtestgen):
    if cxxtestgen:
        if shallWorkOnPy3(cxxtestgen):
            _python = ToolFinder('python', name=['python3', 'python'])
        else:
            _python = ToolFinder('python', name=['python2', 'python'])
        python = _python(env)
    else:
        python = None
    return python


def shallWorkOnPy3(cxxtestgen):
    return not _has_issue_135(cxxtestgen) and _has_py3_impl(cxxtestgen)


class _CxxTestGenFinder(ToolFinder):
    _binpath = os.path.pathsep.join([
        os.path.join('$CXXTESTINSTALLDIR', 'bin'),
        os.path.join('$CXXTESTINSTALLDIR', 'python', 'python3', 'scripts'),
        os.path.join('$CXXTESTINSTALLDIR', 'python', 'scripts')
    ])

    @property
    def priority_path(self):
        # Change the default value of priority_path
        return self._kw.get('priority_path', '$CXXTESTBINPATH')

    @property
    def strip_path(self):
        # Change the default value of strip_path
        return self._kw.get('strip_path', False)

    def __call__(self, env):
        # Put it here, so 'exists' and 'generate' should get same results
        env.SetDefault(CXXTESTINSTALLDIR=env.Dir('#/cxxtest').get_abspath())
        env.SetDefault(CXXTESTBINPATH=self._binpath)

        ret = ToolFinder.__call__(self, env)

        if isinstance(ret, str):
            if sys.platform == 'win32' and ret.lower().endswith('.bat'):
                # Ironically, on Windows we shall avoid 'cxxtestgen.bat'.
                # It's broken and doesn't work with SCons in most cases.
                py = ret[:-4]
            else:
                py = ret
            if self._is_cxxtestgen_py(py):
                ret = py
        return ret

    def _is_small_file(self, fname):
        if not os.path.isfile(fname):
            return False
        try:
            si = os.stat(fname)
        except IOError:
            return False
        # avoid large files; limiting to 256 standard lines should be enough
        return (si.st_size <= 256*82)

    def _is_cxxtestgen_py(self, fname):
        if not self._is_small_file(fname):
            return False
        try:
            with open(fname, 'r') as f:
                content = f.read()
        except IOError:
            return False
        return bool(re.search(r'\bcxxtest(?:gen)?\.main\s*\(', content, re.M))


_cxxTestGenFinder = _CxxTestGenFinder('cxxtestgen')


def _has_issue_135(script):
    # See https://github.com/CxxTest/cxxtest/pull/135
    with open(script, 'r') as f:
        content = f.read()
    regex = r'os\.path\.sep\.join\(\[currdir,\s*\'\.\.\',\s*python3\]\)'
    return bool(re.search(regex, content, re.M))


def _has_py3_impl(script):
    script = os.path.realpath(script)   # resolve symlinks
    scriptdir = os.path.dirname(script)
    outerdir = os.path.dirname(scriptdir)
    regex = re.compile(r'^\s*from\s+\.\s+import\s+__release__\s*$', re.M)
    for parts in [(scriptdir, 'cxxtest', 'cxxtestgen.py'),
                  (scriptdir, 'python3', 'cxxtest', 'cxxtestgen.py'),
                  (outerdir, 'cxxtest', 'cxxtestgen.py'),
                  (outerdir, 'python3', 'cxxtest', 'cxxtestgen.py'),
                  (outerdir, 'python', 'cxxtest', 'cxxtestgen.py'),
                  (outerdir, 'python', 'python3', 'cxxtest', 'cxxtestgen.py')]:
        fname = os.path.join(*parts)
        try:
            with open(fname, 'r') as f:
                code = f.read()
        except IOError:
            pass
        else:
            if regex.search(code, re.M):
                return True
    return False


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
