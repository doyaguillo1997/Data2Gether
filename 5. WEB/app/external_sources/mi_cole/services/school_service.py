from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from app.external_sources.mi_cole.models import School


def get_schools_in_circle(center: Point, radius: int):
    """Get school in circle

    Args:
        center (Point): Center of circle
        radius (int): Radis of circle

    Returns:
        QuerySet: LIst of schools inside the circle
    """
    return School.objects.filter(coord__distance_lte=(center, D(km=radius)))
