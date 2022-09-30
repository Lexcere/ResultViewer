# For relative imports to work in Python 3.6
# https://itsmycode.com/importerror-attempted-relative-import-with-no-known-parent-package/
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
