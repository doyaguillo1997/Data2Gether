from django.core.management.base import BaseCommand
from app.external_sources.csv.models import Load
from app.external_sources.cadastres.services.cadastre_importer import CadastreImporter


class Command(BaseCommand):
    help = "Load Cadastre info into load properties. Example format:"
    " ./manage.py load_cadastre 1"

    def add_arguments(self, parser):
        parser.add_argument("load_id", type=int, help="Load Id")

    def handle(self, *args, **kwargs):
        load = Load.objects.filter(id=kwargs["load_id"]).first()
        if load is None:
            raise Exception(f"load_id: {kwargs['load_id']} does not exists")
        CadastreImporter(load=load)
