from rdfoo.rdf import RDF, RDFType


def assert_rdf_type(obj: RDF, rdf_type: RDFType) -> None:
    """Assert that an RDF object has the expected RDF type(s)."""
    obj_types: list[str] = (
        obj.rdf_type if isinstance(obj.rdf_type, list) else [obj.rdf_type]
    )
    check_types: list[str] = (
        rdf_type if isinstance(rdf_type, list) else [rdf_type]
    )
    for t in check_types:
        assert t in obj_types, f"RDF type mismatch: {t!r} not in {obj_types!r}"
