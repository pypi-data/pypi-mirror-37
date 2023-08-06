from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    long_description = f"See the Homepage for a better formatted version.\n {long_description}"

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

install_reqs = parse_requirements("translator/requirements.txt") #, session="i")
requirements = [str(r) for r in install_reqs]
setup(
    name = 'ros-translator',
    packages = [ 'translator' ], # this must be the same as the name above
    package_data={ 'translator' : [] },
    version = '0.114',
    description = 'NCATS Translator Knowledge Network Workflow Engine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'Steve Cox',
    author_email = 'scox@renci.org',
    install_requires = requirements,
    include_package_data=True,
    url = 'http://github.com/NCATS-Tangerine/ros-translator.git',
    download_url = 'http://github.com/NCATS-Tangerine/ros-translator/archive/0.001.tar.gz',
    keywords = [ 'knowledge', 'network', 'graph', 'biomedical' ],
    classifiers = [ ],
)
