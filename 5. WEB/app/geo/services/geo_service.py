from django.contrib.gis.geos import Point

from app.geo.models import GeoZone


def get_zone_childrens(parent_id: int):
    """Get childrens zone

    Args:
        parent_id (int): geozone parent id

    Returns:
        QuerySet: Gezone childrens
    """
    return GeoZone.objects.filter(parent=parent_id)


def get_zone(id: int):
    """Get geozone by id

    Args:
        id (int): geozone id

    Returns:
        GeoZone: gezone filtered
    """
    return GeoZone.objects.get(pk=id)


def get_zone_containing_point(point: Point, level: int):
    """Geozone of an specific level which contains a point

    Args:
        point (Point): Point to match in geozone
        level (int): Geozone level filter

    Returns:
        Geozone: Geozone that contains the point
    """
    return GeoZone.objects.filter(polygon__contains=point, level=level).first()
