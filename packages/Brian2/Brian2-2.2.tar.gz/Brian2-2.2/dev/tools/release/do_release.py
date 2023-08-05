import os
import sys

raw_input('This will upload a new version of Brian2 to PyPI, press return to continue ')
# upload to pypi
os.chdir('../../..')
os.system('%s setup.py sdist --with-cython --fail-on-error' % sys.executable)
