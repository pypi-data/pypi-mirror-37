import configparser
import json
import subprocess
import re
import sys

from setuptools import setup, find_packages

def get_git_version():
    git_tag = subprocess.check_output(["git", "describe"]).decode(
        'utf-8').strip()
    if re.match("^\d+\.\d+\.\d+$", git_tag) is None:
        print("{} is not semantic versioning Major.Minor.Patch".format(git_tag))
        sys.exit(-1)
    return git_tag

def read_file(file_path):
    try:
        with open(file_path) as file:
            return file.read()
    except Exception as e:
        return ""

def read_necessary_dependency():
    deps = []
    pipfile = configparser.ConfigParser()
    pipfile.read('Pipfile')
    pipfile_lock = json.loads(read_file('Pipfile.lock'))['default']
    for dep in pipfile['packages']:
        deps.append("{}{}".format(dep, pipfile_lock[dep]['version']))
    return deps

setup_params = {
    "name": "generic_report_generator_psql",
    "author": "David Ng",
    "author_email": "david.ng.dev@gmail.com",
    "description": ("The generic report generator for postgresql"),
    "long_description": read_file('README.md'),
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/davidNHK/generic-report-generator-psql",
    "license": "BSD",
    "packages": find_packages("./", exclude=["tests"]),
    "install_requires": read_necessary_dependency()
}

if sys.argv[-1] in ('publish', 'sdist'):
    setup_params['version'] = get_git_version()

setup(
    **setup_params
)