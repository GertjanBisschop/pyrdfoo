from tests.cases.utils import assert_rdf_type

from rdfoo import dcatap
from rdfoo.rdf import uri


def test_create_catalogue():
    obj = dcatap.Catalogue(
        title="Test Catalogue",
        description="A test catalogue.",
        publisher=uri("https://marineinfo.org/id/institute/36"),
    )
    assert_rdf_type(obj, "http://www.w3.org/ns/dcat#Catalog")


def test_create_catalogued_resource():
    obj = dcatap.CataloguedResource()
    assert_rdf_type(obj, "http://www.w3.org/ns/dcat#Resource")


def test_create_dataset():
    obj = dcatap.Dataset(
        title="Test Dataset",
        description="A test dataset.",
    )
    assert_rdf_type(obj, "http://www.w3.org/ns/dcat#Dataset")


def test_create_distribution():
    obj = dcatap.Distribution()
    assert_rdf_type(obj, "http://www.w3.org/ns/dcat#Distribution")


def test_create_period_of_time():
    obj = dcatap.PeriodOfTime()
    assert_rdf_type(obj, "http://purl.org/dc/terms/PeriodOfTime")


def test_create_location():
    obj = dcatap.Location()
    assert_rdf_type(obj, "http://purl.org/dc/terms/Location")


def test_from_graph_001():
    id = "urn:test:TestDCATAP:test_from_graph_001:catalogue"
    catalogue0 = dcatap.Catalogue(
        rdf_id=id,
        title="catalogue",
        publisher=uri("urn:test:TestDCATAP:test_from_graph_001:publisher"),
        description="A test catalogue.",
    )
    graph = catalogue0.to_graph()
    catalogue1 = dcatap.Catalogue.from_graph(id, graph)
    assert catalogue0 == catalogue1


def test_from_graph_002():
    id = "urn:test:TestDCATAP:test_from_graph_002:catalogued_resource"
    catalogued_resource0 = dcatap.CataloguedResource(
        rdf_id=id,
        title="catalogued resource",
    )
    graph = catalogued_resource0.to_graph()
    catalogued_resource1 = dcatap.CataloguedResource.from_graph(id, graph)
    assert catalogued_resource0 == catalogued_resource1


def test_from_graph_003():
    id = "urn:test:TestDCATAP:test_from_graph_003:dataset"
    dataset0 = dcatap.Dataset(
        rdf_id=id,
        title="dataset",
        description="A test dataset.",
    )
    graph = dataset0.to_graph()
    dataset1 = dcatap.Dataset.from_graph(id, graph)
    assert dataset0 == dataset1


def test_from_graph_004():
    id = "urn:test:TestDCATAP:test_from_graph_004:dataset"
    dataset0 = dcatap.Dataset(
        rdf_id=id,
        title="dataset",
        description="A test dataset.",
        distribution=[
            dcatap.Distribution(
                access_url="https://example.com/",
            )
        ],
    )
    graph = dataset0.to_graph()
    dataset1 = dcatap.Dataset.from_graph(id, graph)
    assert dataset0 == dataset1
