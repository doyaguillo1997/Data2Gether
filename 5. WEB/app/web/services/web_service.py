from colour import Color

from app.external_sources.csv.services.csv_service import get_load_properties
from app.external_sources.idealista.services.idealista_service import get_last_info
from app.external_sources.idealista.services.idealista_service import get_predictions
from app.geo.services.geo_service import get_zone_childrens
from app.geo.services.geo_service import get_zone_containing_point


def get_geo_elements(parent_id: int):
    """Load web info on geo elements

    Args:
        parent_id (int): parent geo id

    Returns:
        list: list of geo zones with color info and historic info
    """
    geo_elements = list(get_zone_childrens(parent_id))

    # Load las historic for each geo zone
    prices = []
    for geo_element in geo_elements:
        geo_element.historic = get_last_info(geo_element.pk)
        geo_element.best_moment = None
        if geo_element.historic:
            prices.append(geo_element.historic.price)
            if geo_element.level.id < 3:
                best_moment = get_predictions(geo_element.pk).order_by("-price").first()
                if int(best_moment.price) > geo_element.historic.price:
                    geo_element.best_moment = best_moment

    # Range of colors
    colors = list(
        Color("#b6d148").range_to(Color("green"), int(len(geo_elements) * 100))
    )
    min_price = min(prices)
    max_price = max(prices)
    # Unit of color for each increase in price
    unit_color = (len(colors) - 1) / (max_price - min_price)

    for geo_element in geo_elements:
        if geo_element.historic:  # There are zones without historic
            geo_element.color = str(
                colors[int((geo_element.historic.price - min_price) * unit_color)]
            )

    return geo_elements


def get_wallet(load_id: int):
    properties = list()
    geo_resume = {"neighborhoods": {}, "districts": {}}
    # Get Properties
    dirty_properties = list(get_load_properties(load_id))
    future_predicions_dates = list(get_predictions(1).values("date"))
    # Prepare data structure
    future_estimation_resume = {
        "date": [date["date"] for date in future_predicions_dates],
        "price": [0] * len(future_predicions_dates),
        "conf_up": [0] * len(future_predicions_dates),
        "conf_low": [0] * len(future_predicions_dates),
    }
    wallet = {
        "account_id": dirty_properties[0].load.account.id,
        "load": {
            "id": dirty_properties[0].load.id,
            "name": dirty_properties[0].load.name,
        },
    }

    for dirty_property in dirty_properties:
        property = {}
        property["cadastre"] = {
            "builded_surface": dirty_property.property.cadastre.private_builded_surface,
            "year_built": dirty_property.property.cadastre.year_built,
            "cadastral_reference": dirty_property.property.cadastre.cadastral_reference,
        }
        property["buyed_price"] = dirty_property.property.buyed_price
        property["estimated_price"] = dirty_property.property.estimated_price
        neighborhood = get_zone_containing_point(
            dirty_property.property.cadastre.location, 3
        )
        property["geo"] = {
            "neighborhood": {"id": neighborhood.id, "name": neighborhood.name},
            "district": {
                "id": neighborhood.parent.id,
                "name": neighborhood.parent.name,
            },
            "location": {
                "latitude": dirty_property.property.cadastre.latitude,
                "longitude": dirty_property.property.cadastre.longitude,
            },
        }

        # Get Idealista historic info
        district_historic = get_predictions(neighborhood.parent.id)
        actual_district_price = get_last_info(neighborhood.parent.id).price
        index = 0
        for historic in list(district_historic):
            future_estimation_resume["price"][index] = (
                future_estimation_resume["price"][index]
                + (historic.price / actual_district_price)
                * dirty_property.property.estimated_price
            )

            future_estimation_resume["conf_up"][index] = (
                future_estimation_resume["conf_up"][index]
                + (historic.conf_up / actual_district_price)
                * dirty_property.property.estimated_price
            )

            future_estimation_resume["conf_low"][index] = (
                future_estimation_resume["conf_low"][index]
                + (historic.conf_low / actual_district_price)
                * dirty_property.property.estimated_price
            )

            index = index + 1

        # Check best moment to sell
        best_moment = district_historic.order_by("-price").first()
        if (
            (best_moment.price / actual_district_price)
            * dirty_property.property.estimated_price
            > dirty_property.property.estimated_price
        ):
            property["best_moment"] = {
                "date": best_moment.date,
                "estimated_price": (best_moment.price / actual_district_price)
                * dirty_property.property.estimated_price,
            }

        properties.append(property)

        addPropertyGeoResume(
            geo_resume, dirty_property.property, neighborhood.name, "neighborhoods"
        )
        addPropertyGeoResume(
            geo_resume, dirty_property.property, neighborhood.parent.name, "districts"
        )

    wallet["properties"] = properties
    wallet["future_estimations"] = future_estimation_resume

    geo_resume["neighborhoods"] = {
        k: v
        for k, v in sorted(
            geo_resume["neighborhoods"].items(),
            key=lambda item: item[1]["total_estimated"],
            reverse=True,
        )
    }
    geo_resume["districts"] = {
        k: v
        for k, v in sorted(
            geo_resume["districts"].items(),
            key=lambda item: item[1]["total_estimated"],
            reverse=True,
        )
    }
    wallet["geo_resume"] = geo_resume

    return wallet


def addPropertyGeoResume(geo_resume, property, geo_name, key):
    """Add Geo Resume

    Args:
        geo_resume ([type]): Datastructure to append new info
        property ([type]): Property
        geo_name ([type]): Name of zone
        key ([type]): Districts or neighborhoods
    """
    if geo_name in geo_resume[key]:
        geo_resume[key][geo_name]["total_estimated"] = (
            geo_resume[key][geo_name]["total_estimated"] + property.estimated_price
        )
        geo_resume[key][geo_name]["total_buyed"] = (
            geo_resume[key][geo_name]["total_buyed"] + property.buyed_price
        )
        geo_resume[key][geo_name]["total_properties"] = (
            geo_resume[key][geo_name]["total_properties"] + 1
        )
    else:
        geo_resume[key][geo_name] = {
            "total_estimated": property.estimated_price,
            "total_buyed": property.buyed_price,
            "total_properties": 1,
        }
