from sklearn.base import BaseEstimator, TransformerMixin
from generalFunctions import isNan, isNumber, longitudCategorias


class RangeOtherEncoder(BaseEstimator, TransformerMixin):
    """
    Crea agrupaciones entre las categorías numéricas para generar rangos y agrupa las literales en una categoría other.

    :param transformed_columns: Columna del dataframe sobre la que se aplica el encoder.
    :param exclude_other_values: Valores que no queramos que se incluyan en el campo other.
    :param threshold: Punto de corte para añadir una categoria a un grupo.
    :param margin_threshold: Margen sobre el que se junta categorias resudiales al algoritmo.
    :param literals_as_other: Combierte los valor no numericos en la categoria "other".
    :param mapper: Contiene las asociaciones de los valores de la columna a su rango.
    :return:
    """

    def __init__(self, transformed_columns, exclude_other_values, threshold, margin_threshold,
                 literals_as_other=True):
        super().__init__()
        self.transformed_columns = transformed_columns

        self.exclude_other_values = exclude_other_values

        self.threshold = threshold

        self.margin_threshold = margin_threshold

        self.literals_as_other = literals_as_other

        self.mapper_ = {}

    def fit(self, X, y=None):
        if type(self.exclude_other_values) is not list:
            self.exclude_other_values = self.exclude_other_values

        dictLongitudes = longitudCategorias(X, self.transformed_columns)

        dictValues = {"numbers": [], "other": [], "excluded": self.exclude_other_values}

        asociaciones = {}
        asociaciones.update(dict(zip(dictValues["excluded"], dictValues["excluded"])))

        for key in dictLongitudes.keys():
            if key not in self.exclude_other_values:
                if isNumber(key):
                    dictValues["numbers"].append(key)
                else:
                    dictValues["other"].append(key)

        if self.literals_as_other:
            for value in dictValues["other"]:
                asociaciones[str(value)] = "other"
        else:
            asociaciones.update(dict(zip(dictValues["other"], dictValues["other"])))

        dictValues["numbers"] = list(map(int, dictValues['numbers']))
        dictValues["numbers"].sort()  # inplace
        dictValues["numbers"] = list(map(str, dictValues['numbers']))

        group = {"categ": [], "cuantity": 0}  # Values to group
        groups = {}

        for cat in dictValues["numbers"]:
            if group["cuantity"] <= (self.threshold - 1):
                group["categ"].append(cat)
                group["cuantity"] = group["cuantity"] + dictLongitudes[cat]

            if group["cuantity"] >= self.threshold:
                if len(group["categ"]) > 1:
                    rango = str(group["categ"][0]) + "-" + str(group["categ"][-1])
                else:
                    rango = str(group["categ"][0])

                groups[rango] = group["categ"]
                group = {"categ": [], "cuantity": 0}

        # Agregamos los ultimos elementos, puede darse el caso de que queden residuos < threshold
        self.margin_threshold = int(self.threshold/(abs(self.margin_threshold) + 1))
        if group["cuantity"] > self.margin_threshold:
            if len(group["categ"]) > 1:
                rango = str(group["categ"][0]) + "-" + str(group["categ"][-1])
            else:
                rango = str(group["categ"][0])
            groups[rango] = group["categ"]
        else:
            headMargin = group["categ"][0]  # Valor mas bajo de los marginales
            distance = float("inf")
            keyToGroup = ""
            for key in groups.keys():
                vals = key.split("-")
                if (int(headMargin) - int(vals[-1])) < distance:
                    distance = int(headMargin) - int(vals[-1])
                    keyToGroup = key
            for val in group['categ']:
                groups[keyToGroup].append(val)

            if len(group["categ"]) > 1:
                rango = str(groups[keyToGroup][0]) + "-" + str(groups[keyToGroup][-1])
            else:
                rango = str(group[keyToGroup][0])
            groups[rango] = groups.pop(keyToGroup)

        for clave, valor in groups.items():
            if type(valor) is list:
                for number in valor:
                    asociaciones[str(number)] = clave
            else:
                asociaciones[valor] = clave

        self.mapper_ = asociaciones.copy()

        return self

    def transform(self, X, y=None):
        X_ = X.copy()

        dictLongitudes = longitudCategorias(X, self.transformed_columns)

        not_in_mapper = []

        for value in dictLongitudes.keys():
            if value not in self.mapper_.keys():
                not_in_mapper.append(value)

        for cat in not_in_mapper:
            if isNumber(cat):
                distanceUpper = float("inf")
                distanceLower = float("inf")

                for rango in list(set(self.mapper_.values())):
                    vals = rango.split("-")
                    if isNumber(vals[-1]) and isNumber(vals[0]):
                        if abs((int(cat) - int(vals[-1]))) < distanceUpper:
                            distanceUpper = abs((int(cat) - int(vals[-1])))
                            upperKeyToGroup = rango
                        if abs((int(cat) - int(vals[0]))) < distanceLower:
                            distanceLower = abs((int(cat) - int(vals[-1])))
                            lowerKeyToGroup = rango

                if distanceLower <= distanceUpper:
                    self.mapper_[cat] = lowerKeyToGroup
                else:
                    self.mapper_[cat] = upperKeyToGroup
            else:
                self.mapper_[cat] = "other"

        X_[self.transformed_columns] = X_[self.transformed_columns].apply(
            lambda categoria: categoria if isNan(categoria) else self.mapper_[str(categoria)])
        return X_
