#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2018, Battelle National Biodefense Institute.
#
# This file is part of happer (http://github.com/bioforensics/happer) and is
# licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

import happer
from happer.mutate import PloidyMismatchError
from happer.tests import data_file
import pytest
from tempfile import NamedTemporaryFile


def test_populate_hap_index():
    alsfile = open(data_file('haplo-test1.bed'), 'r')
    alleles = happer.allele.parse_alleles(alsfile)
    ploidy, haplotypes = happer.mutate.populate_haplotype_index(alleles)
    print(haplotypes)
    assert ploidy == 2
    assert len(haplotypes) == 1
    assert 'chr17' in haplotypes
    assert len(haplotypes['chr17']) == 2
    assert [len(hap) for hap in haplotypes['chr17']] == [5, 5]


def test_bad_ploidy():
    alsfile = open(data_file('ploidy-mismatch.bed'), 'r')
    alleles = happer.allele.parse_alleles(alsfile)
    with pytest.raises(PloidyMismatchError) as pme:
        pldy, hapl = happer.mutate.populate_haplotype_index(alleles)
    assert 'ploidy confusion' in str(pme)


def test_mutate_simple():
    seqfile = open(data_file('pico-refr.fa'), 'r')
    sequences = [seq for label, seq in happer.seqio.parse_fasta(seqfile)]
    seqfile = open(data_file('pico-refr.fa'), 'r')
    allelefile = open(data_file('pico-hapl-1.bed'), 'r')
    mutator = happer.mutate.mutate(seqfile, allelefile)
    haploseqs = [sequence for label, sequence in mutator]
    assert len(haploseqs) == 6
    assert 'CAACCTTACGATCTA' in haploseqs[0]
    assert 'CAACCTTCCGATCTA' in haploseqs[1]
    assert 'GGGATAGACCCGTGG' in haploseqs[0]
    assert 'GGGATAGGCCCGTGG' in haploseqs[1]
    assert haploseqs[2] == sequences[1]
    assert haploseqs[3] == sequences[1]
    assert 'TGGACCGCATTGCAG' in haploseqs[4]
    assert 'TGGACCTCATTGCAG' in haploseqs[5]


@pytest.mark.parametrize('mainmethod', [
    happer.mutate.main,
    happer.__main__.main,
])
def test_mutate_cli(mainmethod):
    with NamedTemporaryFile() as outfile:
        arglist = [
            '--out', outfile.name, data_file('pico-refr.fa'),
            data_file('pico-hapl-1.bed')
        ]
        args = happer.get_parser().parse_args(arglist)
        mainmethod(args)
        outseqs = list(happer.seqio.parse_fasta(open(outfile.name, 'r')))
        deflines = [label for label, sequence in outseqs]
        sequences = [sequence for label, sequence in outseqs]
        assert len(deflines) == 6
        assert len(sequences) == 6
        assert deflines == ['chr1:hap1', 'chr1:hap2', 'chr2:hap1', 'chr2:hap2',
                            'chr3:hap1', 'chr3:hap2']
        assert 'CAACCTTACGATCTA' in sequences[0]
        assert 'TGGACCTCATTGCAG' in sequences[5]
