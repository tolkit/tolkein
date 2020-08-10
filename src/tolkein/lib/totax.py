#!/usr/bin/env python3
"""Taxonomy methods."""

import re

from .tofile import open_file_handle


def parse_ncbi_nodes_dmp(path):
    """Parse NCBI format nodes.dmp file."""
    nodes = {}
    with open_file_handle(path) as fh:
        for line in fh:
            taxon_id, parent, rank, *_ignore = re.split(r"\s*\|\s*", line)
            if taxon_id == "1":
                continue
            nodes[taxon_id] = {"parent": parent, "rank": rank, "names": []}
    return nodes


def parse_ncbi_names_dmp(path, nodes):
    """Parse names.dmp file and add to nodes dict."""
    with open_file_handle(path) as fh:
        for line in fh:
            taxon_id, name, unique, name_class, *_ignore = re.split(r"\s*\|\s*", line)
            if taxon_id in nodes:
                if not unique:
                    unique = name
                if name_class == "scientific name":
                    nodes[taxon_id].update(
                        {
                            "taxon_id": taxon_id,
                            "scientific_name": name,
                            "unique_name": unique,
                        }
                    )
                nodes[taxon_id]["names"].append(
                    {"name": name, "unique": unique, "class": name_class}
                )


def parse_ncbi_taxdump(path, root=None):
    """Expand lineages from nodes dict."""
    if root is None:
        root = [1]
    if not isinstance(root, list):
        root = [root]
    roots = list(map(int, root))
    nodes = parse_ncbi_nodes_dmp("%s/nodes.dmp" % path)
    parse_ncbi_names_dmp("%s/names.dmp" % path, nodes)
    for taxon_id, obj in nodes.items():
        lineage = obj.copy()
        lineage.update({"lineage": []})
        descendant = False
        if int(taxon_id) in roots:
            descendant = True
        while "parent" in obj and obj["parent"] in nodes:
            parent = obj["parent"]
            obj = nodes[parent]
            lineage["lineage"].append(
                {
                    "taxon_id": obj["taxon_id"],
                    "rank": obj["rank"],
                    "scientific_name": obj["scientific_name"],
                }
            )
            if int(obj["taxon_id"]) in roots:
                descendant = True
                break
        if descendant:
            yield "taxon_id-%s" % taxon_id, lineage


def parse_taxonomy(taxonomy_type, path, root=None):
    """Parse taxonomy into list of dicts."""
    parsers = {"ncbi": parse_ncbi_taxdump}
    parser = parsers.get(taxonomy_type.lower(), None)
    if parser is None:
        return None
    return parser(path, root)
