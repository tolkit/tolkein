#!/usr/bin/env python3

"""Fetch methods."""

import os
import tarfile
import urllib.request
import zlib

import requests
from tqdm import tqdm

from .tofile import write_file


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


def fetch_tmp_file(url):
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
    return file_tmp


def extract_tar(filename, path):
    """Extract tarred archive."""
    member_count = 0
    with tarfile.open(filename) as tar:
        member_count = len(tar.getmembers())
        # Go over each member
        for member in tqdm(
            iterable=tar.getmembers(), total=member_count, desc="Extract files"
        ):
            # Extract member
            tar.extract(member=member, path=path)
    return member_count


def fetch_tar(url, path):
    """Fetch and extract tarred archive."""
    file_tmp = fetch_tmp_file(url)
    member_count = extract_tar(file_tmp, path)
    return member_count


def fetch_stream(url, decode=True, show_progress=True):
    """Stream download."""
    res = requests.get(url, stream=True)
    if res.encoding is None:
        res.encoding = "utf-8"
    total_size = int(res.headers.get("content-length", 0))
    block_size = 1024
    if show_progress:
        progress = tqdm(total=total_size, unit="iB", unit_scale=True)
    dec = zlib.decompressobj(32 + zlib.MAX_WBITS)
    for data in res.iter_content(block_size):
        if decode:
            try:
                data = dec.decompress(data)
                if show_progress:
                    progress.update(len(data))
                yield data
            except zlib.error:
                decode = False
        if show_progress:
            progress.update(len(data))
        yield data
    if show_progress:
        progress.close()


def fetch_file(url, path, decode=True):
    """Fetch a remote file."""
    data = "" if decode else b""
    for part in fetch_stream(url, decode):
        data += part.decode("utf-8") if decode else part
    write_file(path, data)


def fetch_url(url):
    """Fetch a URL."""
    res = requests.get(url)
    if res.ok:
        return res.content.decode("utf-8")
    return False
