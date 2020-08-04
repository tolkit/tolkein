#!/usr/bin/env python3

"""Fetch methods."""

import os
import tarfile
import urllib.request

from tqdm import tqdm


class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`.

    From tqdm documentation.
    """

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        Tqdm update_to method.

        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


def fetch_tar(url, path):
    """Fetch and extract tarred archive."""
    with TqdmUpTo(
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        miniters=1,
        desc="Fetch %s" % url.split("/")[-1],
    ) as t:
        file_tmp = urllib.request.urlretrieve(
            url, filename=None, reporthook=t.update_to, data=None
        )[0]
        t.total = t.n
    with tarfile.open(file_tmp) as tar:
        # Go over each member
        for member in tqdm(
            iterable=tar.getmembers(), total=len(tar.getmembers()), desc="Extract files"
        ):
            # Extract member
            tar.extract(member=member, path=path)
