#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2018, Battelle National Biodefense Institute.
#
# This file is part of happer (http://github.com/bioforensics/happer) and is
# licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

from happer.allele import Allele
from happer.mutablestring import MutableString

from happer import mutate
from happer import seqio
from happer import tests

from happer.__main__ import get_parser

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
