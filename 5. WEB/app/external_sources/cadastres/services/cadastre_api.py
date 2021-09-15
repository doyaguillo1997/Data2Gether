from app.external_sources.cadastres.helpers.roads_xml import RoadsXml
import logging

import requests
from requests.exceptions import HTTPError

from app.external_sources.cadastres.helpers.cadastre_xml import CadastreXml
from app.external_sources.cadastres.helpers.location_xml import LocationXml

BASE_URI = "https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/"
SRS_CODE = "EPSG:4326"
TIMEOUT = 5
WAIT_BETWEEN_RQ = 1

logger = logging.getLogger(__name__)


class CadastreApi:
    """
    CadastreApi is a raw connection for the Spain Cadastre API.
    Use CadastreService for get models associated to cadastre info
    """

    def get_info_by_rc(self, rc: str):
        """
        Get cadastre information from RC
        """
        try:
            response = requests.post(
                url=BASE_URI + "OVCCallejero.asmx/Consulta_DNPRC",
                data={"Provincia": "", "Municipio": "", "RC": rc.upper()},
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            xml = response.text
            return CadastreXml(xml)
        except HTTPError as http_err:
            logger.exception(f"HTTPError occurred: {http_err}. RC={rc}")
        except Exception as err:
            logger.exception(f"Error occurred: {err}. RC={rc}")

    def get_info_by_address(
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
        """
        Get cadastre information from RC
        """
        try:
            response = requests.post(
                url=BASE_URI + "OVCCallejero.asmx/Consulta_DNPLOC",
                data={
                    "Provincia": province,
                    "Municipio": municipality,
                    "Sigla": type_road,
                    "Calle": road,
                    "Numero": number,
                    "Bloque": block,
                    "Escalera": stairs,
                    "Planta": floor,
                    "Puerta": door,
                },
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            xml = response.text
            return CadastreXml(xml)
        except HTTPError as http_err:
            logger.exception(f"HTTPError occurred: {http_err}. RC={rc}")
        except Exception as err:
            logger.exception(f"Error occurred: {err}. RC={rc}")

    def get_plot_location(self, plot_rc: str):
        """
        Get location from plot RC
        """
        try:
            response = requests.post(
                url=BASE_URI + "OVCCoordenadas.asmx/Consulta_CPMRC",
                data={
                    "Provincia": "",
                    "Municipio": "",
                    "RC": plot_rc.upper(),
                    "SRS": SRS_CODE,
                },
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            xml = response.text
            return LocationXml(xml)
        except HTTPError as http_err:
            logger.exception(f"HTTPError occurred: {http_err}. RC={plot_rc}")
        except Exception as err:
            logger.exception(f"Error occurred: {err}. RC={plot_rc}")

    def get_roads(self, province: str, muncipality: str):
        """
        Get all roads from municipality
        """
        try:
            response = requests.post(
                url=BASE_URI + "OVCCallejero.asmx/ConsultaVia",
                data={
                    "Provincia": province,
                    "Municipio": muncipality,
                    "TipoVia": "",
                    "NombreVia": "",
                },
                timeout=300,
            )
            response.raise_for_status()
            xml = response.text
            return RoadsXml(xml)
        except HTTPError as http_err:
            logger.exception(
                f"HTTPError occurred: {http_err}. Province={province} Municipality={muncipality}"
            )
        except Exception as err:
            logger.exception(
                f"Error occurred: {err}. Province={province} Municipality={muncipality}"
            )
