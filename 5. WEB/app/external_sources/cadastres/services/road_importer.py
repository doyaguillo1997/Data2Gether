from app.external_sources.cadastres.models import Road
from app.external_sources.cadastres.services.cadastre_api import CadastreApi


class RoadImporter:
    """
    Get and load roads
    """

    service: CadastreApi

    def __init__(self):
        self.service = CadastreApi()
        self.load_roads()

    def load_roads(self):
        roads_xml = self.service.get_roads("Madrid", "Madrid")
        for road_xml in roads_xml.roads:
            road = Road(name=road_xml.name, type=road_xml.type)
            road.save()
