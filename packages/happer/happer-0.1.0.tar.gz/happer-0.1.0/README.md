# happer

Daniel Standage, 2018  
https://github.com/bioforensics/happer

**happer** is a minimal Python library for generating complete haplotype sequences.
Given a reference sequence and haplotype alleles annotated in BED format, happer will mutate the reference and produce sequences to match the specified haplotypes.


## Installation

To install:

```bash
pip3 install happer
```

To make sure the package installed correctly:

```bash
pip3 install pytest
py.test --pyargs happer
```

happer requires Python version 3.


## Usage

Reference sequences must be provided in Fasta format, and haplotype alleles must be specified in BED format as follows.
Alleles corresponding to different haplotypes at the locus are separated by a `|` character, so for example a diploid individual should have 2 `|`-separated alleles annotated at each locus, while a tetraploid would have 4 alleles.
In the example below, the `CCGA` alleles are phased and represent one haplotype, while the `TATG` alleles are phased and represent another haplotype.

```txt
#SeqID    Start  End     Alleles
chr1     38827  38828   C|T
chr1     59288  59289   C|A
chr2     24771  24772   G|T
chr4     201191 201192  A|G
```

To invoke happer from the command line:

```
[standage@lappy ~]$ happer --out haploseqs.fasta refr.fasta alleles.bed
```

To invoke happer directly in Python:

```python
>>> import happer
>>> seqfile = open('refr.fasta', 'r')
>>> alleles = open('alleles.bed', 'r')
>>> for label, haploseq in happer.mutate.mutate(seqfile, alleles):
...     # do whatever you'd like with the sequences
```
