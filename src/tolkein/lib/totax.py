#!/usr/bin/env python3
"""Taxonomy methods."""

import re

from .tofile import open_file_handle
from ete3 import NCBITaxa


def parse_ncbi_taxdump(path=None, root=None):
    """Expand lineages from ete3 NCBITaxa.

    Args:
        parg (str): path to NCBI taxdump.tar.gz.
        root (int): Root taxon taxid.

    Returns:
        Generator: Each call yields a descendant taxon as a tuple made up of taxon_id-<taxid>, lineage. Lineage is a list of ancestral lineage tuples with {taxon_id, rank, scientific_name}
    """
    ncbi = NCBITaxa(taxdump_file=path)

    if root is None:
        root = [1]
    if not isinstance(root, list):
        root = [root]
    roots = list(map(int, root))

    for root_taxon_id in roots:
        descendants = ncbi.get_descendant_taxa(
            root_taxon_id,
            intermediate_nodes=True,
            rank_limit=None,
            collapse_subspecies=False,
            return_tree=False,
        )
        for taxon_id in descendants:
            lineage_nodes_list = ncbi.get_lineage(taxon_id)
            lineage_scientific_names_list = ncbi.translate_to_names(lineage_nodes_list)
            lineage_rank_dict = ncbi.get_rank(lineage_nodes_list)
            lineage_scientific_names_dict = dict(
                zip(lineage_nodes_list, lineage_scientific_names_list)
            )
            lineage = [
                {
                    "taxon_id": i,
                    "rank": lineage_rank_dict[i],
                    "scientific_name": lineage_scientific_names_dict[i],
                }
                for i in lineage_nodes_list
            ]
            yield "taxon_id-%s" % taxon_id, lineage


def parse_taxonomy(taxonomy_type, path, root=None):
    """Parse taxonomy into list of dicts."""
    parsers = {"ncbi": parse_ncbi_taxdump}
    parser = parsers.get(taxonomy_type.lower(), None)
    if parser is None:
        return None
    return parser(path, root)
