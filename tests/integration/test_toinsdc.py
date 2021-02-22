#!/usr/bin/env python3
"""Test functions in toinsdc."""

import types

import pytest

from tolkein import toinsdc


def test_count_taxon_assembly_meta():
    """Test count of INSDC assemblies for a root taxon."""
    count = toinsdc.count_taxon_assembly_meta(3702)
    assert count > 0
    invalid_count = toinsdc.count_taxon_assembly_meta(-3702)
    assert invalid_count is None


def test_fetch_wgs_assembly_meta():
    """Test fetching WGS set metadata for a root taxon."""
    wgs_meta = toinsdc.fetch_wgs_assembly_meta(3702)
    assert isinstance(wgs_meta, dict)
    assert len(wgs_meta.keys()) > 0
    key = next(iter(wgs_meta))
    assert key.startswith("SAMN")
    assert "wgs_accession" in wgs_meta[key]
    invalid_meta = toinsdc.count_taxon_assembly_meta(-3702)
    assert invalid_meta is None


def test_stream_taxon_assembly_meta():
    """Test fetching assembly metadata for a root taxon."""
    meta_stream = toinsdc.stream_taxon_assembly_meta(3702)
    assert isinstance(meta_stream, types.GeneratorType)
    asm_meta = next(iter(meta_stream))
    assert isinstance(asm_meta, dict)
    assert len(asm_meta.keys()) > 0
    assert "gca_accession" in asm_meta
    assert "taxon_id" in asm_meta
    invalid_meta = toinsdc.stream_taxon_assembly_meta(-3702)
    assert isinstance(invalid_meta, types.GeneratorType)
    with pytest.raises(StopIteration):
        next(invalid_meta)
