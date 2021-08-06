#!/usr/bin/env python3
"""Run sliding window test."""

from collections import defaultdict

from tolkein import tofile
from tolkein import tostats

FASTA = "examples/sliding_windows/Athaliana_1_5_m_c.fasta"
WINDOWSIZE = 1000
OVERLAP = 0

ctr = defaultdict(int)
gc_bases = defaultdict(list)
kmer_diversity = defaultdict(list)
for (title, seq_str) in tofile.stream_fasta(
    FASTA, windowsize=WINDOWSIZE, overlap=OVERLAP
):
    ctr[title] += 1
    gc_bases[title].append(tostats.base_composition(seq_str)[0])
    kmer_diversity[title].append(tostats.count_unique_kmers(seq_str))
    if ctr[title] == 1:
        print(title)

print(kmer_diversity["NC_003070.9"][:9])
