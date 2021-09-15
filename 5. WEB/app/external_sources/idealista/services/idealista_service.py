from app.external_sources.idealista.models import Historic


def get_historic(geo_zone_id: int):
    """Get historic from geo zone

    Args:
        geo_zone_id (int): geo zone id to get historic

    Returns:
        QuerySet: List with historic info
    """
    return Historic.objects.filter(geo_zone=geo_zone_id, value_type="current").order_by(
        "date"
    )


def get_predictions(geo_zone_id: int):
    """Get predictions from geo zone

    Args:
        geo_zone_id (int): geo zone id to get predicitons

    Returns:
        QuerySet: List with predictions info
    """
    return Historic.objects.filter(
        geo_zone=geo_zone_id, value_type="prediction"
    ).order_by("date")


def get_last_info(geo_zone_id: int):
    """Get last historic from geo zone

    Args:
        geo_zone_id (int): geo zone id to get last historic

    Returns:
        Historic: las historic info
    """
    return (
        Historic.objects.filter(geo_zone=geo_zone_id, value_type="current")
        .order_by("-date")
        .first()
    )
