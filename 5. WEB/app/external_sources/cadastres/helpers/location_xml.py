import xml.etree.cElementTree as et
from xml.etree.cElementTree import Element

XMLNS = "{http://www.catastro.meh.es/}"


class LocationXml:
    tree: Element
    has_errors: bool

    def __init__(self, sxml: str):
        self.tree = et.fromstring(sxml)
        self.has_errors = (
            self.tree.find("./{0}control/{0}cuerr".format(XMLNS)) is not None
            and int(self.tree.find("./{0}control/{0}cuerr".format(XMLNS)).text) > 0
        )

    @property
    def latitude(self):
        return float(
            self.tree.find(
                "./{0}coordenadas/{0}coord/{0}geo/{0}ycen".format(XMLNS)
            ).text
        )

    @property
    def longitude(self):
        return float(
            self.tree.find(
                "./{0}coordenadas/{0}coord/{0}geo/{0}xcen".format(XMLNS)
            ).text
        )
