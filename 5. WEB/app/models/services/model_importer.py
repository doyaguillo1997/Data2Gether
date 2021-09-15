import pandas as pd
import logging
import pickle
from app.main.settings import BASE_DIR

from app.models.models import Model

logger = logging.getLogger(__name__)


class ModelImporter:
    """NOT USE, IN DEVELOPMENT."""

    pkl_file: str
    name: str
    version: float

    def __init__(self, pkl_file: str, name: str, version: float):
        self.pkl_file = pkl_file
        self.name = name
        self.version = version
        # self.process()
        self.test()

    def process(self):
        print(type(self.pkl_file))
        with open(self.pkl_file, "rb") as f:
            model_bin = pickle.load(f)
            model = Model(
                model=pickle.dumps(model_bin), name=self.name, version=self.version
            )
            print(type(model.model))
            model.save()

    def test(self):
        with open((BASE_DIR / "app/csv_files/sample_wallet.csv").resolve()) as file:
            with open(self.pkl_file, "rb") as f:
                model_bin = pickle.load(f)
                df = pd.read_csv(file)
                tmp = list(model_bin[0].predict(df))
                for p in tmp:
                    print(p)
