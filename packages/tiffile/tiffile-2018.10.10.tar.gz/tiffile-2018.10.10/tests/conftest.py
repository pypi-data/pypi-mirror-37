# -*- coding: utf-8 -*-
# tiffile/test/conftest.py

collect_ignore = ['_tmp', 'data']


def pytest_report_header(config):
    try:
        import tiffile
        import imagecodecs
        return 'versions: tiffile-%s, imagecodecs-%s' % (
            tiffile.__version__, imagecodecs.__version__)
    except Exception:
        pass
