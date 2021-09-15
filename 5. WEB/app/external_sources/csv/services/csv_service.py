import json

import pandas as pd
from django.contrib.gis.db.models import Count

from app.external_sources.csv.models import Load
from app.external_sources.csv.models import PropertyDirty


def get_loads_resume(account_id: int):
    """Resume of account loads

    Args:
        account_id (int):

    Returns:
        List: list of the resume loads
    """
    dirty_properties = PropertyDirty.objects.filter(load__account=account_id)
    # Get load info, count and sort by date
    resume = list(
        dirty_properties.values("load__id", "load__name", "load__date")
        .annotate(count=Count("property__id"))
        .order_by("-load__date")
    )

    # Load cadastral info loaded in load and format date
    for load in resume:
        load["not_null_count"] = len(
            dirty_properties.filter(
                load=load["load__id"], property__cadastre__isnull=False
            )
        )
        load["load__date"] = load["load__date"].strftime("%Y-%m-%d %H:%M:%S")

    return resume


def get_load_properties(load_id: int):
    return PropertyDirty.objects.filter(load__id=load_id, property__isnull=False)


def get_loads(account_id: int):
    return Load.objects.filter(account=account_id)


def get_load_df(load_id: int):
    """Get load as dataframe

    Args:
        load_id (int):

    Returns:
        DataFrame: csv as dataFrame
    """
    dirty_properties = PropertyDirty.objects.filter(load__id=load_id).values_list(
        "data"
    )
    # DataFrame from JSON in dirtyProperties
    df = pd.DataFrame([property_data[0] for property_data in dirty_properties])

    # Remove columns added with the mapper
    mapper = json.loads(Load.objects.get(id=load_id).mapper)
    df.drop(list(mapper.keys()), axis=1)

    return df
