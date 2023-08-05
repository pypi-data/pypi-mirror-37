#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2018, Battelle National Biodefense Institute.
#
# This file is part of happer (http://github.com/bioforensics/happer) and is
# licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

from sys import stdout


def parse_fasta(data):
    """Load sequences in Fasta format.

    This generator function yields a tuple containing a defline and a sequence
    for each record in the Fasta data. Stolen shamelessly from
    http://stackoverflow.com/a/7655072/459780.
    """
    defline, sequence = None, list()
    for line in data:
        line = line.rstrip()
        if line.startswith('>'):
            if defline:
                yield (defline[1:], ''.join(sequence))
            defline, sequence = line, list()
        else:
            sequence.append(line)
    yield (defline[1:], ''.join(sequence))


def format(seq, outstream=stdout, linewidth=70):
    """Print the sequence to be legible in a human-readable width."""
    if linewidth == 0 or len(seq) < linewidth:
        print(seq, file=outstream)
        return
    i = 0
    while i < len(seq):
        print(seq[i:i+linewidth], file=outstream)
        i += linewidth
