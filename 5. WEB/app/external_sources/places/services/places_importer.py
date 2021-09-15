import csv
import logging

from django.contrib.gis.geos import Point

from app.external_sources.places.models import GoogleElement
from app.external_sources.places.models import GoogleType

logger = logging.getLogger(__name__)


class PlacesImporter:
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
            google_element = GoogleElement(
                find_type=GoogleType.objects.filter(
                    type=row["find_type"],
                ).first(),
                name=row["name"],
                rating=row["rating"],
                user_ratings_total=row["user_ratings_total"],
                coord=Point(float(row["longitude"]), float(row["latitude"])),
                price_level_missing=row["price_level_missing"],
                price_level=int(float(row["price_level"])),
                price_level_weights=float(
                    row["price_level_weights"],
                ),
            )
            google_element.save()

    def iter_rows(self):
        """Read csv

        Yields:
            Dict: row information
        """
        with open(self.csv_file) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                yield row
