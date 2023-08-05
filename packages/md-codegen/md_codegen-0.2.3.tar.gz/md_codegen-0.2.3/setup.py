#!/usr/bin/env python
from setuptools import setup, find_packages
name = "md_codegen"

requires = ['nodejs_codegen>=0.3.3', 'codegenhelper>=0.0.12']

setup(
    name = name,
    version = '0.2.3',
    scripts = ["scripts/codegen"],
    author = 'Zongying Cao',
    author_email = 'zongying.cao@dxc.com',
    description = 'codegen is a library for generating the infrastructure code of microservices.',
    long_description = """codegen is a library for generating the infrastructure code of microservices.""",
    packages = [name],
    package_dir = {'md_codegen': 'codegen'},
    package_data = {'md_codegen': ["*.py"]},
    include_package_data = True,
    install_requires = requires,
    license = 'Apache',
    classifiers = [
               'Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: Apache Software License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Libraries',
           ],
)
