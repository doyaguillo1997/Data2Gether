import typing as t
import xml.etree.cElementTree as et
from xml.etree.cElementTree import Element

XMLNS = "{http://www.catastro.meh.es/}"


class RoadsXml:
    tree: Element
    has_errors: bool

    def __init__(self, sxml: str):
        self.tree = et.fromstring(sxml)
        self.has_errors = (
            self.tree.find("./{0}control/{0}cuerr".format(XMLNS)) is not None
            and int(self.tree.find("./{0}control/{0}cuerr".format(XMLNS)).text) > 0
        )

    @property
    def roads(self) -> t.List["RoadXml"]:
        return [
            RoadXml(element)
            for element in self.tree.findall("./{0}callejero/{0}calle".format(XMLNS))
        ]


class RoadXml:
    tree: Element

    def __init__(self, tree: Element):
        self.tree = tree

    @property
    def name(self):
        return self.tree.find("./{0}dir/{0}nv".format(XMLNS)).text

    @property
    def type(self):
        return self.tree.find("./{0}dir/{0}tv".format(XMLNS)).text
