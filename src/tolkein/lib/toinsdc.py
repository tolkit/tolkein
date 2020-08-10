#!/usr/bin/env python3
"""INSDC methods."""

import re

import xmltodict
from tqdm import tqdm

from .tofetch import fetch_stream
from .tofetch import fetch_url

WAREHOUSE = "https://www.ebi.ac.uk/ena/data/warehouse"


def count_taxon_assembly_meta(root):
    """
    Count INSDC assemblies descended from root taxon.

    Args:
        root (int): Root taxon taxid.

    Returns:
        int: Count of assemblies for taxa descended from root.
    """
    url = '%s/search?query="tax_tree(%s)"&result=assembly&resultcount' % (
        WAREHOUSE,
        str(root),
    )
    body = fetch_url(url)
    if body:
        match = re.search(r"[\d,+]+", body)
        return int(match.group(0).replace(",", ""))
    return 0


def insdc_key_map(key, *, strict=False):
    """
    Map INSDC metadata keys to normalised values.

    Args:
        key (str): INSDC metadata key.
        strict (bool, optional): Flag to only return values in key_map.
            Default (False) will return lowercase version of key if no match.

    Returns:
        str: Mapped key value.
    """
    key_map = {
        "@accession": "gca_accession",
        "@alias": "alias",
        "@center_name": "center_name",
        "NAME": "assembly_name",
        "SAMPLE_REF": "biosample",
        "STUDY_REF": "bioproject",
        "ENA-LAST-UPDATED": "assembly_date",
        "total-length": "assembly_span",
        "ungapped-length": "ungapped_span",
        "n50": "assembly_n50",
        "spanned-gaps": "spanned_gaps",
        "unspanned-gaps": "unspanned_gaps",
        "scaffold-count": "scaffold_count",
        "count-contig": "contig_count",
        "contig-n50": "contig_n50",
        "contig-L50": "contig_l50",
        "contig-n75": "contig_n75",
        "contig-n90": "contig_n90",
        "scaf-L50": "scaffold_l50",
        "scaf-n75": "scaffold_n75",
        "scaf-n90": "scaffold_n90",
        "replicon-count": "replicon_count",
        "count-non-chromosome-replicon": "non_chr_replicon_count",
        "count-alt-loci-units": "alt_loci_unit_count",
        "count-regions": "region_count",
        "count-patches": "patch_count",
    }
    try:
        mapped_key = key_map[key]
    except KeyError:
        if strict:
            return None
        else:
            mapped_key = key.lower()
    return mapped_key


def _add_if_exists(key, source, dest, *, path=None, null_value=None):
    """Add key to dest if exists in source."""
    dest_key = insdc_key_map(key)
    if key in source:
        source_value = source[key]
        if path:
            for sub_key in path:
                source_value = source_value[sub_key]
        dest.update({dest_key: source_value})
    elif null_value is not None:
        dest.update({dest_key: null_value})


def parse_assembly_meta(raw_meta):
    """
    Assembly metadata Parser.

    Args:
        raw_meta (dict): Raw dict representation of INSDC metadata.

    Returns:
        dict: Normalised dict of INSDC metadata.
    """
    meta = {}
    keys = [
        "@accession",
        "@alias",
        "@center_name",
        "ASSEMBLY_LEVEL",
        "DESCRIPTION",
        "NAME",
        "TITLE",
    ]
    for key in keys:
        _add_if_exists(key, raw_meta, meta)
    for key in {"SAMPLE_REF", "STUDY_REF"}:
        _add_if_exists(key, raw_meta, meta, path=["IDENTIFIERS", "PRIMARY_ID"])
    if "WGS_SET" in raw_meta:
        meta.update(
            {
                "wgs_id": "%s0%s"
                % (raw_meta["WGS_SET"]["prefix"], raw_meta["WGS_SET"]["VERSION"])
            }
        )
    try:
        attributes = raw_meta["ASSEMBLY_ATTRIBUTES"]["ASSEMBLY_ATTRIBUTE"]
    except KeyError:
        attributes = []
    for attribute in attributes:
        key = insdc_key_map(attribute["TAG"], strict=True)
        if key is not None:
            if attribute["VALUE"].isdigit():
                value = int(attribute["VALUE"])
            else:
                value = attribute["VALUE"]
            meta[key] = value
    return meta


def stream_taxon_assembly_meta(root, *, count=-1, offset=0, page=50):
    """
    Query INSDC assemblies descended from root taxon.

    Args:
        root (int): Root taxon taxid.
        count (int): Number of assemblies to return.
            Default value (-1) returns all assemblies.
        offset (int): Offset of first assembly to return. Defaults to 0.
        page (int): Number of assemblies to fetch per API request. Defaults to 50.

    Yields:
        dict: Normalised dict of INSDC metadata.
    """
    done = 0
    while True:
        url = (
            '%s/search?query="tax_tree(%s)"&result=assembly&display=xml&offset=%d&length=%d'
            % (WAREHOUSE, str(root), offset, page)
        )
        chunk = 0
        data = b""
        for part in fetch_stream(url, show_progress=False):
            data += part
            if chunk == 0:
                data = re.split(rb"<ROOT[^>]+>", data)[1]
            chunk += 1
            assemblies = data.split(b"</ASSEMBLY>")
            if len(assemblies) > 1:
                data = assemblies.pop()
                for assembly in assemblies:
                    done += 1
                    raw_metadata = xmltodict.parse(assembly + b"</ASSEMBLY>")[
                        "ASSEMBLY"
                    ]
                    yield parse_assembly_meta(raw_metadata)
                    if count > 0 and done == count:
                        break
            if count > 0 and done == count:
                chunk = 0
                break
        if chunk == 0:
            break
        offset += page
