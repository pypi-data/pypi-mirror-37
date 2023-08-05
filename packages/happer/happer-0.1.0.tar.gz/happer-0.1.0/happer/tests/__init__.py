#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2018, Battelle National Biodefense Institute.
#
# This file is part of happer (http://github.com/bioforensics/happer) and is
# licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

import os
from pkg_resources import resource_filename


def data_file(path):
    relpath = os.path.join('tests', 'data', path)
    return resource_filename('happer', relpath)
