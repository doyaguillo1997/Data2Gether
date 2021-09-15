import typing as t
import xml.etree.cElementTree as et
from xml.etree.cElementTree import Element

XMLNS = "{http://www.catastro.meh.es/}"


class CadastreXml:
    tree: Element
    has_errors: bool
    is_state = bool

    def __init__(self, sxml: str):
        self.tree = et.fromstring(sxml)
        self.has_errors = (
            self.tree.find("./{0}control/{0}cuerr".format(XMLNS)) is not None
            and int(self.tree.find("./{0}control/{0}cuerr".format(XMLNS)).text) > 0
        )
        if not self.has_errors:
            self.is_estate = (
                int(self.tree.find("./{0}control/{0}cudnp".format(XMLNS)).text) != 1
            )
            self.tree = self.tree.find("./{0}bico".format(XMLNS))

    @classmethod
    def extract_rc(cls, rcdnp_element: Element):
        return "".join(
            [ch.text for ch in rcdnp_element.find(f"./{XMLNS}rc").getchildren()]
        )

    @property
    def class_type(self):
        return self.tree.find("./{0}bi/{0}idbi/{0}cn".format(XMLNS)).text

    @property
    def primary_use(self):
        return self.tree.find("./{0}bi/{0}debi/{0}luso".format(XMLNS)).text

    @property
    def cadastral_reference(self):
        return self.extract_rc(self.tree.find("./{0}bi/{0}idbi".format(XMLNS)))

    @property
    def address(self):
        return self.tree.find("./{0}bi/{0}ldt".format(XMLNS)).text

    @property
    def province(self):
        return self.tree.find("./{0}bi/{0}dt/{0}np".format(XMLNS)).text

    @property
    def municipality(self):
        return self.tree.find("./{0}bi/{0}dt/{0}nm".format(XMLNS)).text

    @property
    def builded_surface(self):
        return int(self.tree.findtext("./{0}bi/{0}debi/{0}sfc".format(XMLNS), "0"))

    @property
    def participation_coefficient(self):
        return float(
            self.tree.findtext("./{0}bi/{0}debi/{0}cpt".format(XMLNS), "100").replace(
                ",", "."
            )
        )

    @property
    def year_built(self):
        return int(self.tree.findtext("./{0}bi/{0}debi/{0}ant".format(XMLNS), "-1"))

    @property
    def postal_code(self):
        return self.tree.findtext(
            "./{0}bi/{0}dt/{0}locs/{0}lous/{0}lourb/{0}dp".format(XMLNS)
        )

    @property
    def distributions(self) -> t.List["DistributionXml"]:
        return [
            DistributionXml(element)
            for element in self.tree.findall("./{0}lcons/{0}cons".format(XMLNS))
        ]

    @property
    def subplots(self) -> t.List["SubplotXml"]:
        return [
            SubplotXml(element)
            for element in self.tree.findall("./{0}lspr/{0}spr".format(XMLNS))
        ]

    def process(self):
        cadastre = self.map_cadastre()
        subplots = self.map_subplots() if self.subplot_tree else []
        distributions = self.map_distributions() if self.distribution_tree else []
        return (cadastre, subplots, distributions)

    def get_rc_list(self):
        return [
            self.extract_rc(rcdnp)
            for rcdnp in self.tree.findall("./{0}lrcdnp/{0}rcdnp".format(XMLNS))
        ]


class DistributionXml:
    tree: Element

    def __init__(self, tree: Element):
        self.tree = tree

    @property
    def princpial_use(self):
        return self.tree.find(f"./{XMLNS}lcd").text

    @property
    def surface(self):
        return self.tree.find("./{0}dfcons/{0}stl".format(XMLNS)).text


class SubplotXml:
    tree: Element

    def __init__(self, tree: Element):
        self.tree = tree

    @property
    def surface(self):
        return int(self.tree.find("./{0}dspr/{0}ssp".format(XMLNS)).text)

    @property
    def subplot_code(self):
        return self.tree.find(f"./{XMLNS}cspr").text

    @property
    def cadastral_qualification(self):
        return self.tree.find("./{0}dspr/{0}ccc".format(XMLNS)).text

    @property
    def cultivation_class(self):
        return self.tree.find("./{0}dspr/{0}dcc".format(XMLNS)).text

    @property
    def productive_intensity(self):
        return self.tree.find("./{0}dspr/{0}ip".format(XMLNS)).text
