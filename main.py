#!/usr/bin/env python

from context import Context
from ui.main_ui import MainUI

__author__ = "Tim Ofenbach"
__copyright__ = "Copyright 2021, AuPyCity"
__credits__ = []
__license__ = "GPL"
__version__ = "Pre Alpha 1.0.0"
__maintainer__ = "Tim Ofenbach"
__email__ = "t.ofenbach@web.de"
__status__ = "Development"

""" AuDaCity Alternative created by Tim Ofenbach
    Year: 2021 """


if __name__ == '__main__':
    """ Display Default UI """
    context = Context()
    mainUI = MainUI(context)

