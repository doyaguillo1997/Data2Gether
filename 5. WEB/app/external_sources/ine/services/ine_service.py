from app.external_sources.ine.models import DemographicElement


def get_demographic_info(geo_zone_id: int):
    """Get sociodemographic info from geo zone

    Args:
        geo_zone_id (int): geo zone id to filter

    Returns:
        DemographicElement: sociodemographic information from geo zone
    """
    return DemographicElement.objects.filter(geo_zone=geo_zone_id).first()
