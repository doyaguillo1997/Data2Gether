from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from app.external_sources.places.models import GoogleElement


def get_places_in_circle(center: Point, radius: int):
    return GoogleElement.objects.filter(coord__distance_lte=(center, D(km=radius)))
