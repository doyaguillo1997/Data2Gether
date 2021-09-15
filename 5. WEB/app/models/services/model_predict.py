import pickle
from threading import Lock

from django.contrib.gis.db.models import Avg
from pandas import DataFrame

from app.external_sources.cadastres.models import Cadastre
from app.external_sources.csv.services.csv_service import get_load_properties
from app.external_sources.idealista.services.idealista_service import get_last_info
from app.external_sources.ine.services.ine_service import get_demographic_info
from app.external_sources.mi_cole.services.school_service import get_schools_in_circle
from app.external_sources.places.services.places_service import get_places_in_circle
from app.geo.services.geo_service import get_zone_containing_point
from app.main.settings import BASE_DIR
from app.properties.services.property_service import update_estimated_price

__cached_model = None
__lock_model = Lock()


def get_model():
    global __cached_model
    __lock_model.acquire()
    try:
        if __cached_model is None:
            __cached_model = load_model()
    finally:
        __lock_model.release()

    return __cached_model


def load_model():
    """Read model file

    Returns:
        Pipeline: model pipeline
    """
    with open((BASE_DIR / "app/model_files/model_v1.pkl").resolve(), "rb") as f:
        return pickle.load(f)[0]


def createDataFrame(load_id: int):
    """Create dataframe with model variables from a load

    Args:
        load_id (int): load to filter

    Returns:
        DataFrame: DataFrame with model variables
    """
    dirty_properties = list(get_load_properties(load_id))
    rows = list()
    for dirty_property in dirty_properties:
        row = prepare_data(dirty_property.property.cadastre)
        row["property_id"] = dirty_property.property.id

        rows.append(row)

    return DataFrame(rows)


def predict_and_save(dataframe: DataFrame):
    """Predict on dataFrame and save in BD

    Args:
        dataframe (DataFrame): Dataframe to be predicted
    """
    model = get_model()
    property_ids = dataframe["property_id"]
    dataframe = dataframe.drop(["property_id"], axis=1)
    predictions = list(model.predict(dataframe))
    index = 0
    for property_id in property_ids:
        update_estimated_price(property_id, predictions[index])
        index = index + 1


def predict_one(cadastre: Cadastre):
    """Predict on row

    Args:
        cadastre (Cadastre): Cadastre info to make the prediction

    Returns:
        Float: Model prediction
    """
    data = DataFrame(
        [
            prepare_data(cadastre),
        ]
    )
    prediction = -1
    model = get_model()
    prediction = list(model.predict(data))[0]

    return prediction


def prepare_data(cadastre: Cadastre):
    """Add model variables

    Args:
        cadastre (Cadastre): Cadastre info to add new variables

    Returns:
        Dict: Dictionary with variables
    """
    floor = cadastre.floor
    row = {}
    if not floor.isnumeric():
        if floor == "SM":
            floor = "-1"
        else:
            floor = "NaN"
    row["ide_floor"] = floor
    row["ide_size"] = cadastre.private_builded_surface
    row["ide_longitude"] = cadastre.longitude
    row["ide_latitude"] = cadastre.latitude
    neighborhood = get_zone_containing_point(cadastre.location, 3)
    neighborhood_historic = get_last_info(neighborhood.id)
    row["his_quarterly_variation"] = neighborhood_historic.quarterly_variation
    row["his_price"] = neighborhood_historic.price
    row["his_monthly_variation"] = neighborhood_historic.monthly_variation
    row["his_annual_variation"] = neighborhood_historic.annual_variation
    row["geo_distrito"] = neighborhood.parent.name
    row["geo_barrio"] = neighborhood.name
    places = get_places_in_circle(cadastre.location, 1)
    if len(places) == 0:
        row["fe_places_weights_imputed"] = 0
    else:
        row["fe_places_weights_imputed"] = places.aggregate(Avg("price_level_weights"))[
            "price_level_weights__avg"
        ]

    demographic_info = get_demographic_info(neighborhood.id)
    row[
        "dem_Indice_de_reemplazo_de_la_poblacion_activa"
    ] = demographic_info.index_replacement_active_population
    row["dem_Indice_de_juventud"] = demographic_info.index_youth
    row[
        "dem_Indice_de_estructura_de_la_poblacion_activa"
    ] = demographic_info.index_active_population
    row["dem_Indice_de_dependencia"] = demographic_info.index_dependency
    row["dem_TasaDeParo"] = demographic_info.unemployment_rate
    row["dem_TamanoMedioDelHogar"] = demographic_info.avg_size_home
    row[
        "dem_PropSinEstudiosUniversitarios"
    ] = demographic_info.prop_without_university_studies
    row["dem_PropSinEstudios"] = demographic_info.prop_without_studies
    row[
        "dem_Proporcion_de_nacidos_fuera_de_Espana"
    ] = demographic_info.prop_born_outside
    row[
        "dem_PropConEstudiosUniversitarios"
    ] = demographic_info.prop_with_university_studies
    row["dem_PobTotal"] = demographic_info.pob_total
    row["dem_NumViviendas"] = demographic_info.count_households
    row["dem_EdadMedia"] = demographic_info.avg_age
    row["dem_Densidad_(Habit/Ha)"] = demographic_info.density
    schools = get_schools_in_circle(cadastre.location, 2)
    if len(schools) == 0:
        row["fe_micole_weights"] = 0
    else:
        row["fe_micole_weights"] = schools.aggregate(Avg("price_level_weights"))[
            "price_level_weights__avg"
        ]
    return row
