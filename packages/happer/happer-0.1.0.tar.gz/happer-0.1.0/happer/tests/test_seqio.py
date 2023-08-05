#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2018, Battelle National Biodefense Institute.
#
# This file is part of happer (http://github.com/bioforensics/happer) and is
# licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

import happer
from io import StringIO
import pytest


def test_parse_fasta():
    seq = '>seq1\nACGT\n>seq2 yo\nGATTACA\nGATTACA\n>seq3\tdescrip\nATGATGTGA'
    seqstream = seq.split('\n')
    recordstream = happer.seqio.parse_fasta(seqstream)
    records = list(recordstream)
    assert records == [
        ('seq1', 'ACGT'),
        ('seq2 yo', 'GATTACAGATTACA'),
        ('seq3\tdescrip', 'ATGATGTGA'),
    ]


def test_parse_fasta_single():
    seqstream = '>contig1\nATGNNNNNNNNNTGA'.split('\n')
    recordstream = happer.seqio.parse_fasta(seqstream)
    records = list(recordstream)
    assert records == [('contig1', 'ATGNNNNNNNNNTGA')]


def test_format_seq():
    seq = 'CAAAATGTCAGAGAAGTGTCGGACGTAGCCGACTAAAGGATCAGAGTGATCGTTGCGCGTGAGCGCT'

    out1 = StringIO()
    happer.seqio.format(seq, out1, 0)
    assert out1.getvalue() == seq + '\n'

    out2 = StringIO()
    happer.seqio.format(seq, out2, 40)
    for outputline in out2.getvalue().split('\n'):
        assert len(outputline) <= 40

    out3 = StringIO()
    happer.seqio.format(seq, out3, 20)
    formatseq = (
        'CAAAATGTCAGAGAAGTGTC\n'
        'GGACGTAGCCGACTAAAGGA\n'
        'TCAGAGTGATCGTTGCGCGT\n'
        'GAGCGCT\n'
    )
    assert out3.getvalue() == formatseq
