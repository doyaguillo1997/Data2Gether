from app.models.services.model_importer import ModelImporter
from app.main.settings import BASE_DIR

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """NOT USE. IN DEVELOPMENT

    Args:
        BaseCommand ([type]): [description]
    """

    help = (
        "Load Model. Example format: ./manage.py load_model model.pkl nombre_model 1.0"
    )

    def add_arguments(self, parser):
        parser.add_argument("pkl_file", type=str, help="Nombre del pkl")
        parser.add_argument("name", type=str, help="Nombre del modelo")
        parser.add_argument("version", type=float, help="Versión del modelo")

    def handle(self, *args, **kwargs):
        pkl_file = (BASE_DIR / "app/models_files" / kwargs["pkl_file"]).resolve()
        ModelImporter(pkl_file=pkl_file, name=kwargs["name"], version=kwargs["version"])
