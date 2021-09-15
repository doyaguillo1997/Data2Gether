from django.core.management.base import BaseCommand

from app.external_sources.cadastres.services.road_importer import RoadImporter


class Command(BaseCommand):
    """Load cadastre roads of Madrid muncipality

    Args:
        BaseCommand ([type]): [description]
    """
    help = "Load Roads from Madrid Municipality. Example format:"
    " ./manage.py load_roads"

    def handle(self, *args, **kwargs):
        RoadImporter()
