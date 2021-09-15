# FUERA DE SERVICIO. USAR WEB

# import json
# from app.main.settings import BASE_DIR

# from django.core.management.base import BaseCommand

# from app.accounts.models import Account
# from app.external_sources.csv.services.csv_importer import CsvImporter

# class Command(BaseCommand):
#     help = "Load CSV. Example format: ./manage.py load_csv 1 propiedades_validas.csv "
#     # "{\"external_id\":\"external\", \"RC\":\"referencia\"}"

#     def add_arguments(self, parser):
#         parser.add_argument("account_id", type=int, help="Account Id")
#         parser.add_argument("csv_name", type=str, help="Nombre del CSV")
#         parser.add_argument("mapper", type=str, help="Mappeo de las columnas")

#     def handle(self, *args, **kwargs):
#         account = Account.objects.filter(id=kwargs["account_id"]).first()
#         if account is None:
#             raise Exception(f"Account_id: {kwargs['account_id']} does not exists")
#         mapper_dic = json.loads(kwargs["mapper"])
#         csv_file = (BASE_DIR / "csv_files" / kwargs["csv_name"]).resolve()
#         CsvImporter(account=account, mapper=mapper_dic, csv_file=csv_file)
