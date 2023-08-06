# -*- coding: utf-8 -*-

"""Constants for Bio2BEL PFAM."""

import os

from bio2bel import get_data_dir

__all__ = [
    'VERSION',
    'MODULE_NAME',
    'DATA_DIR',
    'CLAN_MAPPING_URL',
    'CLAN_MAPPING_PATH',
    'CLAN_MAPPING_HEADER',
]

VERSION = '0.0.1'
MODULE_NAME = 'bio2bel_pfam'
DATA_DIR = get_data_dir(MODULE_NAME)

CLAN_MAPPING_URL = 'ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.clans.tsv.gz'
CLAN_MAPPING_PATH = os.path.join(DATA_DIR, 'Pfam-A.clans.tsv.gz')
CLAN_MAPPING_HEADER = [
    'family_id',
    'clan_id',
    'clan_name',
    'family_name',
    'family_summary',
]
