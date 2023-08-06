# -*- coding: utf-8 -*-
"""scons-tool-cxxtestgen
"""

from setuptools import setup
import setuptools.command.install
import setuptools.command.develop
import os
import sys

if sys.version_info < (3,0):
    from io import open as uopen
else:
    uopen = open

here = os.path.abspath(os.path.dirname(__file__))

readme_rst = os.path.join(here, 'README.rst')
with uopen(readme_rst, encoding='utf-8') as f:
    readme = f.read()

about = {}
about_py = os.path.join(here, 'about.py')
with uopen(about_py, encoding='utf-8') as f:
    exec(f.read(), about)

class develop(setuptools.command.develop.develop):

    def run(self, *args, **kw):
        subdir = os.path.join(here, 'sconstool', 'cxxtestgen')
        if not os.path.exists(subdir):
            os.makedirs(subdir)

        init_py = os.path.join(subdir, '__init__.py')
        if not os.path.exists(init_py):
            os.symlink('../../__init__.py', init_py)

        about_py = os.path.join(subdir, 'about.py')
        if not os.path.exists(about_py):
            os.symlink('../../about.py', about_py)

        readme_txt = os.path.join(subdir, 'README.txt')
        if not os.path.exists(readme_txt):
            with open(readme_txt, 'w') as f:
                f.write('The __init__.py symlink is just a workaround for ' +
                        'broken "pip install -e ."')

        setuptools.command.develop.develop.run(self, *args, **kw)


install = setuptools.command.install.install


setup(
        name='scons-tool-cxxtestgen',
        version=about['__version__'],
        package_dir={'sconstool.cxxtestgen': '.'},
        packages=['sconstool.cxxtestgen'],
        namespace_packages=['sconstool'],
        description='SCons tool for cxxtestgen command',
        long_description=readme,
        long_description_content_type='text/x-rst',
        url='https://github.com/ptomulik/scons-tool-cxxtestgen',
        author='Paweł Tomulik',
        author_email='ptomulik@meil.pw.edu.pl',
        cmdclass={'develop': develop, 'install': install}
)

# vim: set expandtab tabstop=4 shiftwidth=4:
