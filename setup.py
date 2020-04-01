#!/usr/bin/python3
# coding=utf-8
# pylint: disable=I0011,C0103,C0301,W0702

#   Copyright 2020 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
    Auth setup script
"""

import pkgutil
import importlib
import subprocess

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required_dependencies = f.read().splitlines()

setup(
    name="auth",
    version="0.0.1",
    license="Apache License 2.0",
    author="Carrier team",
    author_email="artem_rozumenko@epam.com",
    url='https://getcarrier.io',
    description="Auth middleware",
    long_description="Auth middleware",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=required_dependencies,
    entry_points={"console_scripts": ["app = auth.app:main"]},
)
