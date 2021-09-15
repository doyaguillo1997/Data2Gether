from django.test import TestCase
from app.external_sources.csv.services.csv_importer import CsvImporter


class CsvImporterTest(TestCase):
    def test_validate_mapper_all_mandatory(self):
        """Mapper has mandatory columns"""
        mapper = {"external_id": "external", "RC": "referencia"}
        CsvImporter.validate_mapper(mapper)

    def test_validate_mapper_not_mandatory(self):
        """Mapper has not all mandatory columns"""
        mapper = {"random": "random", "RC": "referencia"}
        with self.assertRaises(Exception):
            CsvImporter.validate_mapper(mapper)
