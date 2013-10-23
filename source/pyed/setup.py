#!/usr/bin/env python

from distutils.core import setup

setup(name='pyed',
        version='0.39.0',
        description="Mange et vomis des donnees dans ed, puis les remange et les revomi dans un .nav",
        author='CanalTP',
        author_email='vincent.lara@canaltp.fr',
        url='www.navitia.io',
        packages=['pyed'],
        requires=['configobj'],
        scripts=['pyed_service.py']
)