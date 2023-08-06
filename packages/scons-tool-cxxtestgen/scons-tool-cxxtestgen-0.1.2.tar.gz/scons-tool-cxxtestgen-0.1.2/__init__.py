# -*- coding: utf-8 -*-
"""sconstool.cxxtestgen

Tool-specific initialization for cxxtestgen.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
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

from .about import __version__

from sconstool.util import ToolFinder
from SCons.Builder import Builder
from SCons.Util import CLVar
import sys
import os
import re


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


_cxxtestgen = _CxxTestGenFinder('cxxtestgen')


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

def _shall_work_on_py3(cxxtestgen):
    return not _has_issue_135(cxxtestgen) and _has_py3_impl(cxxtestgen)


def createCxxTestGenBuilder(env):
    try:
        builder = env['BUILDERS']['CxxTestGen']
    except KeyError:
        builder = Builder(action='$CXXTESTGENCOM',
                          suffix='$CXXTESTGENSUFFIX',
                          src_suffix='$CXXTESTGENSRCSUFFIX')
        env['BUILDERS']['CxxTestGen'] = builder
    return builder


def generate(env):
    createCxxTestGenBuilder(env)

    cxxtestgen = _cxxtestgen(env)

    if cxxtestgen:
        if _shall_work_on_py3(cxxtestgen):
            _python = ToolFinder('python', name=['python3', 'python'])
        else:
            _python = ToolFinder('python', name=['python2', 'python'])

    env.SetDefault(CXXTESTGENPYTHON=_python(env) or sys.executable)
    env.SetDefault(CXXTESTGEN=cxxtestgen or 'cxxtestgen')
    env.SetDefault(CXXTESTGENRUNNER='ErrorPrinter')


    env.SetDefault(CXXTESTGENFLAGS=CLVar())
    env.SetDefault(CXXTESTGENSUFFIX='.t.cpp')
    env.SetDefault(CXXTESTGENSRCSUFFIX='.t.h')
    env['CXXTESTGENCOM'] = '$CXXTESTGENPYTHON $CXXTESTGEN --runner=$CXXTESTGENRUNNER $CXXTESTGENFLAGS -o $TARGET $SOURCE'


def exists(env):
    return env.Detect(env.get('CXXTESTGEN', _cxxtestgen(env)))

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
