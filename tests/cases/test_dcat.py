from rdflib import Literal
from tests.cases.utils import assert_rdf_type

from rdfoo import dcat
from rdfoo.rdf import RDFURIRef


def test_create_catalogue():
    obj = dcat.Catalogue()
    assert_rdf_type(obj, "http://www.w3.org/ns/dcat#Catalog")


def test_create_catalogued_resource():
    obj = dcat.CataloguedResource()
    assert_rdf_type(obj, "http://www.w3.org/ns/dcat#Resource")


def test_create_dataset():
    obj = dcat.Dataset()
    assert_rdf_type(obj, "http://www.w3.org/ns/dcat#Dataset")


def test_create_distribution():
    obj = dcat.Distribution()
    assert_rdf_type(obj, "http://www.w3.org/ns/dcat#Distribution")


def test_create_period_of_time():
    obj = dcat.PeriodOfTime()
    assert_rdf_type(obj, "http://purl.org/dc/terms/PeriodOfTime")


def test_create_location():
    obj = dcat.Location()
    assert_rdf_type(obj, "http://purl.org/dc/terms/Location")


def test_from_graph_000():
    # no identifier should lead to a blank node.
    title = "unidentified catalogue"
    catalogue0 = dcat.Catalogue(title=title)
    graph = catalogue0.to_graph()
    # the blank node cannot be pointed to by id, so we have to find it by its properties.
    subj = list(graph.subjects(None, Literal(title)))[0]
    catalogue1 = dcat.Catalogue.from_graph(subj, graph)
    assert catalogue0 == catalogue1


def test_from_graph_001():
    id = "urn:test:TestDCAT:test_from_graph_001:catalogue"
    catalogue0 = dcat.Catalogue(rdf_id=id, title="catalogue")
    graph = catalogue0.to_graph()
    catalogue1 = dcat.Catalogue.from_graph(id, graph)
    assert catalogue0 == catalogue1


def test_from_graph_002():
    id = "urn:test:TestDCAT:test_from_graph_002:catalogued_resource"
    catalogued_resource0 = dcat.CataloguedResource(
        rdf_id=id,
        title="catalogued resource",
    )
    graph = catalogued_resource0.to_graph()
    catalogued_resource1 = dcat.CataloguedResource.from_graph(id, graph)
    assert catalogued_resource0 == catalogued_resource1


def test_from_graph_003():
    id = "urn:test:TestDCAT:test_from_graph_003:dataset"
    dataset0 = dcat.Dataset(
        rdf_id=id,
        title="dataset",
    )
    graph = dataset0.to_graph()
    dataset1 = dcat.Dataset.from_graph(id, graph)
    assert dataset0 == dataset1


def test_data_service():
    id = "urn:test:data_service"
    ref_data_service = dcat.DataService(
        rdf_id=id, title="dataservice", endpoint_url="https://example.com"
    )
    graph = ref_data_service.to_graph()
    data_service = dcat.DataService.from_graph(id, graph)
    assert data_service == ref_data_service


def test_catalog_with_data_service():
    id = "urn:test:catalog"
    data_service = dcat.DataService(
        rdf_id="urn:test:data_service",
        title="dataservice",
        endpoint_url="https://example.com",
    )
    ref_catalog = dcat.Catalogue(
        rdf_id=id,
        title="Catalogue",
        service=[data_service],
    )
    graph = ref_catalog.to_graph()
    catalog = dcat.Catalogue.from_graph(id, graph)
    assert catalog == ref_catalog


def test_from_graph_004():
    id = "urn:test:TestDCAT:test_from_graph_004:dataset"
    dataset0 = dcat.Dataset(
        rdf_id=id,
        title="dataset",
        distribution=[
            dcat.Distribution(
                access_url="https://example.com/",
            )
        ],
    )
    graph = dataset0.to_graph()
    dataset1 = dcat.Dataset.from_graph(id, graph)
    assert dataset0 == dataset1


def test_distribution_with_data_service():
    id = "urn:test:catalog"
    data_service = dcat.DataService(
        rdf_id="urn:test:data_service",
        title="dataservice",
        endpoint_url="https://example.com",
    )
    ref_distribution = dcat.Distribution(
        rdf_id=id,
        title="Catalogue",
        access_service=[data_service],
    )
    graph = ref_distribution.to_graph()
    distribution = dcat.Distribution.from_graph(id, graph)
    assert distribution == ref_distribution


def test_distribution_format():
    dataset_id = "urn:test:dataset"
    ref_dataset = dcat.Dataset(
        rdf_id=dataset_id,
        title="dataset",
        distribution=[
            dcat.Distribution(
                access_url="https://example.com/sample.nc",
                conforms_to=RDFURIRef(
                    uri="https://cfconventions.org/Data/cf-conventions/cf-conventions-1.11/cf-conventions.html"
                ),
                format="application/netcdf",
            )
        ],
    )
    graph = ref_dataset.to_graph()
    dataset = dcat.Dataset.from_graph(dataset_id, graph)
    assert ref_dataset == dataset


def test_catalog():
    id = "urn:test:catalog"
    sub_catalog = dcat.Catalogue(
        rdf_id="urn:test:sub_catalog", title="Sub catalogue"
    )
    ref_catalog = dcat.Catalogue(
        rdf_id=id, title="Catalogue", catalog=[sub_catalog]
    )
    graph = ref_catalog.to_graph()
    catalog = dcat.Catalogue.from_graph(id, graph)
    assert ref_catalog == catalog
