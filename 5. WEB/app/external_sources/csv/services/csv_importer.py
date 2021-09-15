import csv
import io
import json
import logging
import typing as t

from django.core.files.uploadedfile import InMemoryUploadedFile

from app.accounts.models import Account
from app.external_sources.csv.constants import MANDATORY_COLUMNS
from app.external_sources.csv.models import Load
from app.external_sources.csv.models import PropertyDirty
from app.properties.models import Property

logger = logging.getLogger(__name__)


class CsvImporter:
    """Read CSV and load info"""

    account: Account
    mapper: t.Dict
    load: Load
    csv_file: str
    property_ids: t.Set[str]
    properties_saved: int

    def __init__(
        self,
        account: Account,
        name: str,
        mapper: t.Dict,
        csv_file: InMemoryUploadedFile,
    ):
        self.properties_saved = 0
        self.validate_mapper(mapper)
        self.account = account
        self.mapper = mapper
        self.csv_file = csv_file

        self.load = Load(
            account=account,
            name=name,
            mapper=json.dumps(mapper, indent=4),
        )
        self.load.save()
        self.property_ids = self.load_properties()
        self.process()

    @classmethod
    def validate_mapper(cls, mapper: t.Dict):
        """Validate that csv has all columns

        Args:
            mapper (t.Dict): Mapper to be validated

        Raises:
            Exception: Missin Columns
        """
        mandatory = set(MANDATORY_COLUMNS)
        columns = set(mapper)
        missing = mandatory - columns
        if missing:
            raise Exception(f"Missing columns: {missing}")

        unknown = columns - mandatory
        if unknown:
            logger.warning(f"Found unkown mapper columns: {unknown}")

    def load_properties(self):
        """Get properties of the account

        Returns:
            set: set with the properties of the account
        """
        return set(
            Property.objects.filter(account=self.account).values_list(
                "external_id", flat=True
            )
        )

    def process(self):
        """Read csv and process rows"""
        for row in self.iter_rows():
            row_mapped = self.map_columns(row)
            external_id = row_mapped["external_id"]
            buyed_price = row_mapped["buyed_price"]
            if external_id not in self.property_ids:
                property = Property(
                    external_id=external_id,
                    account=self.account,
                    buyed_price=buyed_price,
                )
                property.save()
            else:
                property = Property.objects.filter(
                    external_id=external_id, account=self.account
                ).first()
            PropertyDirty(load=self.load, property=property, data=row).save()
            self.properties_saved = self.properties_saved + 1

    def iter_rows(self):
        """Read CSV

        Yields:
            dict: row information
        """
        file = self.csv_file.read().decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(file))
        for row in csv_reader:
            yield row

    def map_columns(self, row: t.Dict):
        """Map csv column names to applicaiton names

        Args:
            row (t.Dict): row from csv

        Returns:
            Dict: row form csv with application column names
        """
        for target, source in self.mapper.items():
            row[target] = row[source]
        return row
