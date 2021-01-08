#!/usr/bin/env python3

"""Calculate sequence statistics."""
import re
from collections import Counter
from collections import OrderedDict
from collections import defaultdict
from itertools import combinations


def base_composition(seq_str):
    """Sequence base composition summary."""
    counts = Counter(seq_str.upper())
    at_bases = ["A", "T", "W"]
    gc_bases = ["C", "G", "S"]
    at_count = 0
    gc_count = 0
    for base in at_bases:
        at_count += counts[base]
    for base in gc_bases:
        gc_count += counts[base]
    acgt_count = at_count + gc_count
    try:
        gc_portion = float("%.4f" % (gc_count / acgt_count))
    except ZeroDivisionError:
        gc_portion = 0
    n_count = len(seq_str) - acgt_count
    return gc_portion, n_count


def count_unique_kmers(seq_str, *, kmer_length=4):
    """Count unique kmers in a sequence."""
    if kmer_length > 7:
        raise ValueError("kmer_length must be <= 7")
    bases = set({"A", "C", "G", "T"})
    kmers = set()
    seq_str = seq_str.upper()
    for i in range(len(seq_str) - kmer_length):
        kmer = seq_str[i : i + kmer_length]
        kmers.add(kmer)
    ctr = 0
    for kmer in kmers:
        valid = True
        for base in kmer:
            if base not in bases:
                valid = False
                break
        if valid:
            ctr += 1
    return ctr


if __name__ == "__main__":
    import doctest

    doctest.testmod()
