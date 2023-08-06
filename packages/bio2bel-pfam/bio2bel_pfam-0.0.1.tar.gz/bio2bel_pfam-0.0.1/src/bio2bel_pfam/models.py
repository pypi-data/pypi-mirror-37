# -*- coding: utf-8 -*-

"""SQLAlchemy models for Bio2BEL PFAM."""

import logging

import pybel.dsl
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from .constants import MODULE_NAME

__all__ = [
    'Base',
    'Family',
    'Clan'
]

logger = logging.getLogger(__name__)

FAMILY_TABLE_NAME = f'{MODULE_NAME}_family'
CLAN_TABLE_NAME = f'{MODULE_NAME}_clan'

Base: DeclarativeMeta = declarative_base()


class Family(Base):
    """A PFAM Protein Family."""

    __tablename__ = FAMILY_TABLE_NAME
    id = Column(Integer, primary_key=True)

    pfam_id = Column(String, nullable=False, index=True, unique=True)
    name = Column(String, nullable=True)
    summary = Column(String, nullable=True)

    def as_pybel(self) -> pybel.dsl.Protein:
        """Serialize as a PyBEL protein."""
        return pybel.dsl.protein(
            namespace='pfam',
            name=self.name,
            identifier=self.pfam_id,
        )

    def __repr__(self):  # noqa: D105
        return f'<Family pfam_id={self.pfam_id}, name={self.name}, summary={self.summary}>'


class Clan(Base):
    """A PFAM Protein Clan."""

    __tablename__ = CLAN_TABLE_NAME
    id = Column(Integer, primary_key=True)

    clan_id = Column(String, nullable=False, index=True, unique=True)
    name = Column(String, nullable=True)
