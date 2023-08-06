# -*- coding: utf-8 -*-

"""Parsers for Bio2BEL PFAM."""

from bio2bel.downloading import make_df_getter

from .constants import CLAN_MAPPING_HEADER, CLAN_MAPPING_PATH, CLAN_MAPPING_URL

__all__ = [
    'get_clan_mapping_df',
]

get_clan_mapping_df = make_df_getter(
    CLAN_MAPPING_URL,
    CLAN_MAPPING_PATH,
    sep='\t',
    compression='gzip',
    names=CLAN_MAPPING_HEADER,
)
