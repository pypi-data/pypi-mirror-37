# -*- coding: utf-8 -*-
# tifffile.py

"""Proxy for the tifffile module in the tiffile package."""

from tiffile.tifffile import __doc__, __all__, __version__  # noqa
from tiffile.tifffile import lsm2bin, main  # noqa
from tiffile.tifffile import *  # noqa

if __name__ == '__main__':
    import sys
    sys.exit(main())
