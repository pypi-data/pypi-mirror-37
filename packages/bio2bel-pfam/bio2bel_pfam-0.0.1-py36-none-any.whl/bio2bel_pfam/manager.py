# -*- coding: utf-8 -*-

"""Manager for Bio2BEL PFAM."""

from typing import Mapping, Optional

from bio2bel import AbstractManager
from bio2bel.manager.flask_manager import FlaskMixin
from bio2bel.manager.namespace_manager import BELNamespaceManagerMixin
from pybel.manager.models import Namespace, NamespaceEntry

from .constants import MODULE_NAME
from .models import Base, Clan, Family
from .parsers import get_clan_mapping_df


class Manager(AbstractManager, BELNamespaceManagerMixin, FlaskMixin):
    """Manages the Bio2BEL PFAM database."""

    module_name = MODULE_NAME
    _base = Base
    flask_admin_models = [Family, Clan]

    namespace_model = Family
    identifiers_recommended = 'Pfam'
    identifiers_pattern = '^PF\d{5}$'
    identifiers_miriam = 'MIR:00000028'
    identifiers_namespace = 'pfam'
    identifiers_url = 'http://identifiers.org/pfam/'

    def count_families(self) -> int:
        """Count the number of families in the database."""
        return self._count_model(Family)

    def count_clans(self) -> int:
        """Count the number of clans in the database."""

    def is_populated(self) -> bool:
        """Check if the Bio2BEL PFAM database is populated."""
        return 0 < self.count_families()

    def summarize(self) -> Mapping[str, int]:
        """Summarize the contents of the Bio2BEL PFAM database."""
        return dict(
            families=self.count_families(),
            clans=self.count_clans(),
        )

    def populate(self, clan_mapping_url: Optional[str] = None) -> None:
        """Populate the Bio2BEL PFAM database."""
        clan_mapping_df = get_clan_mapping_df(url=clan_mapping_url)
        print(clan_mapping_df.head())
        # slice the dataframe. It's not so big so this is okay.
        pfam_df = clan_mapping_df[['family_id', 'family_name', 'family_summary']]
        print(pfam_df.head())
        pfam_df.columns = ['pfam_id', 'name', 'summary']
        pfam_df.to_sql(Family.__tablename__, self.engine, if_exists='append', index=False)
        self.session.commit()

    @staticmethod
    def _get_identifier(family: Family) -> str:
        return family.pfam_id

    def _create_namespace_entry_from_model(self, family: Family, namespace: Namespace) -> NamespaceEntry:
        return NamespaceEntry(
            namespace=namespace,
            name=family.name,
            identifier=family.pfam_id,
            encoding='P',
        )
