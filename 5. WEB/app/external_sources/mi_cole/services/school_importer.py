import csv
import logging

from django.contrib.gis.geos import Point

from app.external_sources.mi_cole.models import School
from app.external_sources.mi_cole.models import SchoolType

logger = logging.getLogger(__name__)


class SchoolImporter:
    """Read csv and save info in models"""

    csv_file: str

    def __init__(
        self,
        csv_file: str,
    ):
        self.csv_file = csv_file
        self.process()

    def process(self):
        """Read csv and save models"""
        for row in self.iter_rows():
            school = School(
                name=row["name"],
                address=row["address"],
                price=row["price"],
                review=row["review"],
                description=row["description"],
                query=row["query"],
                coord=Point(float(row["longitude"]), float(row["latitude"])),
                price_level=row["price_level"],
                price_level_weights=row["price_level_weights"],
                type=SchoolType.objects.filter(
                    id=row["type_id"],
                ).first(),
            )
            school.save()

    def iter_rows(self):
        """Read csv

        Yields:
            Dict: row information
        """
        with open(self.csv_file) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                yield row
