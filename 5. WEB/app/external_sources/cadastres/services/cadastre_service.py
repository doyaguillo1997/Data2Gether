import logging

from django.contrib.gis.geos import Point
from django.core.cache import cache

from app.external_sources.cadastres.helpers.cadastre_xml import CadastreXml
from app.external_sources.cadastres.helpers.location_xml import LocationXml
from app.external_sources.cadastres.models import Cadastre
from app.external_sources.cadastres.models import ClassType
from app.external_sources.cadastres.models import Distribution
from app.external_sources.cadastres.models import PrimaryUse
from app.external_sources.cadastres.models import Subplot
from app.external_sources.cadastres.services.cadastre_api import CadastreApi

logger = logging.getLogger(__name__)


class CadastreService:
    """
    CadastreService is used to obtain the cadastral information of a property
    """

    service: CadastreApi

    def __init__(self):
        self.service = CadastreApi()

    @classmethod
    def is_valid(cls, rc: str):
        """
        Simple validation for cadastre id
        """
        return rc and rc.strip() and len(rc) == 20

    def get_cadastre(self, rc: str):
        """
        Return cadastre asociated to rc. If not exists in DB create Cadastre
        and models asociated
        """
        if not self.is_valid(rc):
            return

        cadastre = Cadastre.objects.filter(cadastral_reference=rc).first()
        if cadastre:  # Exists in DB
            return cadastre

        cadastre_xml = cache.get(rc)
        if not cadastre_xml:
            cadastre_xml = self.service.get_info_by_rc(rc)
            cache.set(rc, cadastre_xml)

        if not cadastre_xml:  # Not 200
            return

        try:
            if cadastre_xml.has_errors:
                logger.error(f"There are errors in cadastre with rc={rc}")
                return
            if cadastre_xml.is_estate:
                logger.warning(f"rc={rc} is an estate")
                return
            else:
                rc_plot = rc[0:14]
                location_xml = cache.get(rc_plot)
                if not location_xml:
                    location_xml = self.service.get_plot_location(rc_plot)
                    cache.set(rc_plot, location_xml)
                return self.save_cadastre_info(cadastre_xml, location_xml)

        except Exception as err:
            logger.exception(f"Exception: {err}")

    def get_cadastre_by_address(
        self,
        province: str,
        municipality: str,
        type_road: str,
        road: str,
        number: str,
        block: str,
        stairs: str,
        floor: str,
        door: str,
    ):
        cadastre_xml = self.service.get_info_by_address(
            province,
            municipality,
            type_road,
            road,
            number,
            block,
            stairs,
            floor,
            door,
        )
        try:
            if cadastre_xml.has_errors:
                logger.error(
                    f"There are errors in cadastre with rc={cadastre_xml.cadastral_reference}"
                )
                return
            if cadastre_xml.is_estate:
                logger.warning(f"rc={cadastre_xml.cadastral_reference} is an estate")
                return
            else:
                rc_plot = cadastre_xml.cadastral_reference[0:14]
                location_xml = self.service.get_plot_location(rc_plot)
                return self.save_cadastre_info(cadastre_xml, location_xml)

        except Exception as err:
            logger.exception(f"Exception: {err}")

    @classmethod
    def save_cadastre_info(cls, cadastre_xml: CadastreXml, location_xml: LocationXml):
        """
        Save cadastre info in database
        """
        cadastre = Cadastre(
            primary_use=cls.get_primary_use(cadastre_xml.primary_use),
            type=cls.get_class_type(cadastre_xml.class_type),
            cadastral_reference=cadastre_xml.cadastral_reference,
            address=cadastre_xml.address,
            province=cadastre_xml.province,
            municipality=cadastre_xml.municipality,
            builded_surface=cadastre_xml.builded_surface,
            participation_coefficient=cadastre_xml.participation_coefficient,
            year_built=cadastre_xml.year_built,
            location=cls.get_location(location_xml),
            postal_code=cadastre_xml.postal_code,
        )
        cadastre.save()

        for subplot_xml in cadastre_xml.subplots:
            subplot = Subplot(
                cadastre=cadastre,
                surface=subplot_xml.surface,
                subplot_code=subplot_xml.subplot_code,
                cadastral_qualification=subplot_xml.cadastral_qualification,
                cultivation_class=subplot_xml.cultivation_class,
                productive_intensity=subplot_xml.productive_intensity,
            )
            subplot.save()

        for distribution_xml in cadastre_xml.distributions:
            distribution = Distribution(
                cadastre=cadastre,
                princpial_use=distribution_xml.princpial_use,
                surface=distribution_xml.surface,
            )
            distribution.save()

        return cadastre

    @classmethod
    def get_primary_use(cls, text: str):
        """
        Search PrimaryUse in db. If not exists it is created
        """
        primary_use = PrimaryUse.objects.filter(text=text).first()
        if primary_use is None:
            primary_use = PrimaryUse(text=text)
            primary_use.save()
        return primary_use

    @classmethod
    def get_class_type(cls, type: str):
        """
        Search ClassType in db. If not exists it is created
        """
        class_type = ClassType.objects.filter(type=type).first()
        if class_type is None:
            class_type = ClassType(type=type)
            class_type.save()
        return class_type

    @classmethod
    def get_location(cls, location_xml: LocationXml):
        """
        Get Point object from LocationXml. If xml has errors returno none
        """
        if not location_xml.has_errors:
            return Point(location_xml.longitude, location_xml.latitude)
