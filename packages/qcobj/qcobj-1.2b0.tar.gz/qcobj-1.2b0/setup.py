#
# R. Vidmar, 20180906
#

from setuptools import setup, find_packages
# setuptools allows "python setup.py develop"
from pip.req import parse_requirements
from pip.download import PipSession
import subprocess
import os
import qcobj

PYSIDE = False

#------------------------------------------------------------------------------
def _get_version_tag():
    """ Talk to git and find out the tag/hash of our latest commit
    """
    try:
        p = subprocess.Popen(["git", "describe", "--abbrev=0", ],
                             stdout=subprocess.PIPE)
    except EnvironmentError as e:
        print("Couldn't run git to get a version number for setup.py")
        print('Using current version "%s"' % qcobj.__version__ )
        return qcobj.__version__
    version = p.communicate()[0].strip().decode()
    with open(os.path.join("qcobj", "__init__.py"), 'w') as the_file:
        the_file.write('__version__ = "%s"' % version)
    return version

#------------------------------------------------------------------------------
if PYSIDE:
    reqfile = "requirements_PySide.txt"
else:
    reqfile = "requirements.txt"

print("\n\nQCOBJ Setup:\nWill use %s for installing.\n" % reqfile)

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [str(ir.req)
        for ir in parse_requirements(reqfile, session=PipSession())]

setup( name='qcobj',
        version=_get_version_tag(),
        install_requires=requirements,
        author='Roberto Vidmar',
        author_email='rvidmar@inogs.it',
        description='A quantity aware configObject',
        license='MIT',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://bitbucket.org/bvidmar/qcobj',
        packages=find_packages(),
        scripts=['bin/cfggui.py', ],
        classifiers=(
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.6",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ),
        )
