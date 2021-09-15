from app.external_sources.cadastres.services.cadastre_service import CadastreService
from app.external_sources.csv.models import Load
from app.external_sources.csv.models import PropertyDirty
from app.properties.models import Property


class CadastreImporter:
    """
    Add cadastre information to a load
    """

    service: CadastreService
    load: Load
    dirty_properties: set
    cadastres_loaded: int

    def __init__(self, load: Load):
        self.service = CadastreService()
        self.cadastres_loaded = 0

        self.load = load
        if self.load:
            self.dirty_properties = self.get_properties()
            return self.process()

    def get_properties(self):
        """
        Get dirty properties associated to load
        """
        return PropertyDirty.objects.filter(load=self.load).values_list(
            "data", "property"
        )

    def process(self):
        """
        Add cadastre information for each property
        """
        for row in self.iter_rows():
            rc = row[0]
            property = Property.objects.filter(id=row[1]).first()
            if not property.cadastre:
                cadastre = self.service.get_cadastre(rc)
                if cadastre:
                    property.cadastre = cadastre
                    property.save()
                    self.cadastres_loaded = self.cadastres_loaded + 1

    def iter_rows(self):
        """
        Return iterable tuple with RC and property
        """
        for dirty_property in self.dirty_properties:
            # TODO: Use logger.info
            yield (dirty_property[0]["RC"], dirty_property[1])
