from datetime import UTC, datetime, timedelta

from tests.cases.utils import assert_rdf_type

from rdfoo import prov
from rdfoo.rdf import RDFURIRef


def test_entity_create():
    base_entity = prov.Entity(
        rdf_id="base",
        title="The base entity!",
    )
    entity = prov.Entity(
        rdf_id="entity",
        title="The deriving entity",
        was_derived_from=base_entity,
    )
    assert_rdf_type(entity, "http://www.w3.org/ns/prov#Entity")


def test_entity_from_graph():
    base_entity = prov.Entity(
        rdf_id="base",
        title="The base entity!",
    )
    entity_id = "entity"
    ref_entity = prov.Entity(
        rdf_id=entity_id,
        title="The deriving entity",
        was_derived_from=base_entity,
    )
    graph = ref_entity.to_graph()
    entity = prov.Entity.from_graph(entity_id, graph)
    assert ref_entity == entity


def test_entity_from_graph_with_activity():
    now = datetime.now(UTC)
    base_activity = prov.Activity(
        rdf_id="base",
        title="The base activity!",
        ended_at_time=now - timedelta(seconds=95),
        started_at_time=now - timedelta(seconds=100),
    )
    activity_id = "activity"
    ref_activity = prov.Activity(
        rdf_id=activity_id,
        title="The deriving activity",
        was_derived_from=base_activity,
        ended_at_time=now - timedelta(seconds=85),
        started_at_time=now - timedelta(seconds=90),
    )
    graph = ref_activity.to_graph()
    activity = prov.Activity.from_graph(activity_id, graph)
    assert ref_activity == activity


def test_entity_from_graph_with_attribution():
    entity_id = "entity"
    agent = prov.Agent(rdf_id="https://marineinfo.org/id/person/45562/")
    ref_entity = prov.Entity(rdf_id=entity_id, was_attributed_to=agent)
    graph = ref_entity.to_graph()
    entity = prov.Entity.from_graph(entity_id, graph)
    assert ref_entity == entity


def test_activity_create():
    now = datetime.now(UTC)
    activity = prov.Activity(
        rdf_id="work",
        ended_at_time=now - timedelta(seconds=95),
        started_at_time=now - timedelta(seconds=100),
    )
    assert_rdf_type(activity, "http://www.w3.org/ns/prov#Activity")


def test_activity_from_graph():
    id = "work"
    now = datetime.now(UTC)
    ref_activity = prov.Activity(
        rdf_id=id,
        ended_at_time=now - timedelta(seconds=95),
        started_at_time=now - timedelta(seconds=100),
    )
    graph = ref_activity.to_graph()
    activity = prov.Activity.from_graph(id, graph)
    assert ref_activity == activity


def test_activity_from_graph_with_informed_by():
    activity_id = "work"
    now = datetime.now(UTC)
    informed_activity = prov.Activity(rdf_id="eat")
    ref_activity = prov.Activity(
        rdf_id=activity_id,
        was_informed_by=informed_activity,
        ended_at_time=now - timedelta(seconds=95),
        started_at_time=now - timedelta(seconds=100),
    )
    graph = ref_activity.to_graph()
    activity = prov.Activity.from_graph(activity_id, graph)
    assert ref_activity == activity


def test_activity_from_graph_with_derived_from():
    activity_id = "work"
    now = datetime.now(UTC)
    derived_entity = prov.Entity(rdf_id="thing")
    informed_activity = prov.Activity(rdf_id="eat")
    ref_activity = prov.Activity(
        rdf_id=activity_id,
        was_derived_from=derived_entity,
        was_informed_by=informed_activity,
        ended_at_time=now - timedelta(seconds=95),
        started_at_time=now - timedelta(seconds=100),
    )
    graph = ref_activity.to_graph()
    activity = prov.Activity.from_graph(activity_id, graph)
    assert ref_activity == activity


def test_activity_from_graph_with_association():
    activity_id = "pipeline"
    now = datetime.now(UTC)
    agent = prov.Agent(rdf_id="https://marineinfo.org/id/person/45562/")
    agent_activity = prov.Activity(rdf_id="triggered")
    plan = prov.Plan(rdf_id="script")
    agent_role = prov.Role(rdf_id="owner")
    association = prov.Association(
        rdf_id="association",
        agent=agent,
        had_activity=agent_activity,
        had_plan=plan,
        had_role=agent_role,
    )
    ref_activity = prov.Activity(
        rdf_id=activity_id,
        was_associated_with=agent,
        qualified_association=association,
        ended_at_time=now - timedelta(seconds=95),
        started_at_time=now - timedelta(seconds=100),
    )
    graph = ref_activity.to_graph()
    activity = prov.Activity.from_graph(activity_id, graph)
    assert ref_activity == activity


def test_activity_from_graph_with_multiple_association():
    activity_id = "pipeline"
    now = datetime.now(UTC)
    agent1 = prov.Agent(rdf_id="https://marineinfo.org/id/person/45562/")
    agent2 = prov.Agent(rdf_id="https://marineinfo.org/id/person/45563/")
    agent_activity = prov.Activity(rdf_id="triggered")
    plan = prov.Plan(rdf_id="script")
    agent_role = prov.Role(rdf_id="owner")
    association1 = prov.Association(
        rdf_id="association1",
        agent=agent1,
        had_activity=agent_activity,
        had_plan=plan,
        had_role=agent_role,
    )
    association2 = prov.Association(
        rdf_id="association2",
        agent=agent2,
        had_activity=agent_activity,
        had_plan=plan,
        had_role=agent_role,
    )
    ref_activity = prov.Activity(
        rdf_id=activity_id,
        was_associated_with=[agent1, agent2],
        qualified_association=[association1, association2],
        ended_at_time=now - timedelta(seconds=95),
        started_at_time=now - timedelta(seconds=100),
    )
    graph = ref_activity.to_graph()
    activity = prov.Activity.from_graph(activity_id, graph)
    assert ref_activity == activity


def test_activity_from_graph_with_influence():
    activity_id = "sleep"
    eat = prov.Activity(rdf_id="eat")
    rave = prov.Activity(rdf_id="rave")
    ref_activity = prov.Activity(
        rdf_id=activity_id, was_influenced_by=eat, influenced=rave
    )
    graph = ref_activity.to_graph()
    activity = prov.Activity.from_graph(activity_id, graph)
    assert ref_activity == activity


def test_agent_create():
    agent = prov.Agent(
        rdf_id="https://marineinfo.org/id/person/45562/",
        name="Bram Van der Streeck",
        mbox=RDFURIRef(uri="mailto:bram.van.der.streeck@vliz.be"),
    )
    assert_rdf_type(agent, "http://www.w3.org/ns/prov#Agent")


def test_agent_from_graph():
    agent_id = "https://marineinfo.org/id/person/45562/"
    ref_agent = prov.Agent(
        rdf_id=agent_id,
        name="Bram Van der Streeck",
        mbox="bram.van.der.streeck@vliz.be",
    )
    graph = ref_agent.to_graph()
    agent = prov.Agent.from_graph(agent_id, graph)
    assert ref_agent == agent


def test_agent_from_graph_with_mail_uri():
    agent_id = "https://marineinfo.org/id/person/45562/"
    ref_agent = prov.Agent(
        rdf_id=agent_id,
        name="Bram Van der Streeck",
        mbox=RDFURIRef(uri="mailto:bram.van.der.streeck@vliz.be"),
    )
    graph = ref_agent.to_graph()
    agent = prov.Agent.from_graph(agent_id, graph)
    assert ref_agent == agent


def test_agent_from_graph_with_on_behalf():
    org_id = "https://marineinfo.org/id/institute/36/"
    ref_org = prov.Agent(
        rdf_id=org_id,
        name="VLIZ (Vlaams Instituut voor de Zee)",
        mbox=RDFURIRef(uri="mailto:info@vliz.be"),
    )
    agent_id = "https://marineinfo.org/id/person/45562/"
    ref_agent = prov.Agent(
        rdf_id=agent_id,
        name="Bram Van der Streeck",
        mbox=RDFURIRef(uri="mailto:bram.van.der.streeck@vliz.be"),
        acted_on_behalf_of=ref_org,
    )
    graph = ref_agent.to_graph()
    agent = prov.Agent.from_graph(agent_id, graph)
    assert ref_agent == agent


def test_role_create():
    role = prov.Role(
        rdf_id="software_engineer",
        title="Software Engineer",
        description="A software engineer applies a software development process to define, implement, test, manage, and maintain software systems.",
    )
    assert_rdf_type(role, "http://www.w3.org/ns/prov#Role")


def test_role_from_graph():
    role_id = "software_engineer"
    ref_role = prov.Role(
        rdf_id=role_id,
        title="Software Engineer",
    )
    graph = ref_role.to_graph()
    role = prov.Role.from_graph(role_id, graph)
    assert ref_role == role


def test_role_from_graph_with_description():
    role_id = "software_engineer"
    ref_role = prov.Role(
        rdf_id=role_id,
        title="Software Engineer",
        description="A software engineer applies a software development process to define, implement, test, manage, and maintain software systems.",
    )
    graph = ref_role.to_graph()
    role = prov.Role.from_graph(role_id, graph)
    assert ref_role == role


def test_role_from_graph_with_multiple():
    role_id = "software_engineer"
    ref_role = prov.Role(
        rdf_id=role_id,
        title=["Software Engineer", "Software Ingenieur"],
        description=[
            "A software engineer applies a software development process to define, implement, test, manage, and maintain software systems.",
            "Een software-engineer past een softwareontwikkelingsproces toe om softwaresystemen te definiëren, implementeren, testen, beheren en onderhouden.",
        ],
    )
    graph = ref_role.to_graph()
    role = prov.Role.from_graph(role_id, graph)
    assert ref_role == role


def test_location_create():
    location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
    assert_rdf_type(location, "http://www.w3.org/ns/prov#Location")


def test_instantaneous_event_create():
    location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
    event = prov.InstantaneousEvent(
        rdf_id="event", at_time=datetime.now(UTC), at_location=location
    )
    assert_rdf_type(event, "http://www.w3.org/ns/prov#InstantaneousEvent")


def test_instantaneous_event_from_graph():
    location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
    event_id = "event"
    ref_event = prov.InstantaneousEvent(
        rdf_id=event_id, at_time=datetime.now(UTC), at_location=location
    )
    graph = ref_event.to_graph()
    event = prov.InstantaneousEvent.from_graph(event_id, graph)
    assert ref_event == event


def test_influence_create():
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    role = prov.Role(
        rdf_id="software_engineer",
    )
    influence = prov.Influence(
        rdf_id="influence",
        had_activity=activity,
        had_role=role,
    )
    assert_rdf_type(influence, "http://www.w3.org/ns/prov#Influence")


def test_influence_from_graph():
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    role = prov.Role(
        rdf_id="software_engineer",
    )
    influence_id = "influence"
    ref_influence = prov.Influence(
        rdf_id=influence_id,
        had_activity=activity,
        had_role=role,
    )
    graph = ref_influence.to_graph()
    influence = prov.Influence.from_graph(influence_id, graph)
    assert ref_influence == influence


def test_influence_from_graph_with_influencer():
    agent = prov.Agent(
        rdf_id="https://marineinfo.org/id/person/45562/",
    )
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    role = prov.Role(
        rdf_id="software_engineer",
    )
    influence_id = "influence"
    ref_influence = prov.Influence(
        rdf_id=influence_id,
        influencer=agent,
        had_activity=activity,
        had_role=role,
    )
    graph = ref_influence.to_graph()
    influence = prov.Influence.from_graph(influence_id, graph)
    assert ref_influence == influence


def test_activity_influence_create():
    influence_activity = prov.Activity(rdf_id="eat")
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    role = prov.Role(
        rdf_id="work_completed",
    )
    influence = prov.ActivityInfluence(
        rdf_id="influence",
        activity=influence_activity,
        had_activity=activity,
        had_role=role,
    )
    assert_rdf_type(influence, "http://www.w3.org/ns/prov#ActivityInfluence")


def test_activity_influence_from_graph():
    influence_activity = prov.Activity(rdf_id="eat")
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    role = prov.Role(
        rdf_id="work_completed",
    )
    influence_id = "influence"
    ref_influence = prov.ActivityInfluence(
        rdf_id=influence_id,
        activity=influence_activity,
        had_activity=activity,
        had_role=role,
    )
    graph = ref_influence.to_graph()
    influence = prov.ActivityInfluence.from_graph(influence_id, graph)
    assert ref_influence == influence


def test_agent_influence_create():
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    agent = prov.Agent(
        rdf_id="https://marineinfo.org/id/person/45562/",
        name="Bram Van der Streeck",
    )
    role = prov.Role(
        rdf_id="software_engineer",
    )
    influence = prov.AgentInfluence(
        rdf_id="influence",
        agent=agent,
        had_activity=activity,
        had_role=role,
    )
    assert_rdf_type(influence, "http://www.w3.org/ns/prov#AgentInfluence")


def test_agent_influence_from_graph():
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    agent = prov.Agent(
        rdf_id="https://marineinfo.org/id/person/45562/",
        name="Bram Van der Streeck",
    )
    role = prov.Role(
        rdf_id="software_engineer",
    )
    influence_id = "influence"
    ref_influence = prov.AgentInfluence(
        rdf_id=influence_id,
        agent=agent,
        had_activity=activity,
        had_role=role,
    )
    graph = ref_influence.to_graph()
    influence = prov.AgentInfluence.from_graph(influence_id, graph)
    assert ref_influence == influence


def test_entity_influence_create():
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    entity = prov.Entity(
        rdf_id="thing",
    )
    role = prov.Role(
        rdf_id="thingifier",
    )
    influence = prov.EntityInfluence(
        rdf_id="influence",
        entity=entity,
        had_activity=activity,
        had_role=role,
    )
    assert_rdf_type(influence, "http://www.w3.org/ns/prov#EntityInfluence")


def test_entity_influence_from_graph():
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    entity = prov.Entity(
        rdf_id="thing",
    )
    role = prov.Role(
        rdf_id="thingifier",
    )
    influence_id = "influence"
    ref_influence = prov.EntityInfluence(
        rdf_id=influence_id,
        entity=entity,
        had_activity=activity,
        had_role=role,
    )
    graph = ref_influence.to_graph()
    influence = prov.EntityInfluence.from_graph(influence_id, graph)
    assert ref_influence == influence


def test_association_create():
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    agent = prov.Agent(
        rdf_id="https://marineinfo.org/id/person/45562/",
        name="Bram Van der Streeck",
    )
    role = prov.Role(
        rdf_id="software_engineer",
    )
    association = prov.Association(
        rdf_id="bram_software_engineer",
        had_activity=activity,
        agent=agent,
        had_role=role,
    )
    assert_rdf_type(association, "http://www.w3.org/ns/prov#Association")


def test_association_from_graph():
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    agent = prov.Agent(
        rdf_id="https://marineinfo.org/id/person/45562/",
        name="Bram Van der Streeck",
    )
    role = prov.Role(
        rdf_id="software_engineer",
    )
    association_id = "bram_software_engineer"
    ref_association = prov.Association(
        rdf_id=association_id,
        had_activity=activity,
        agent=agent,
        had_role=role,
    )
    graph = ref_association.to_graph()
    association = prov.Association.from_graph(association_id, graph)
    assert ref_association == association


def test_association_from_graph_with_plan():
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    agent = prov.Agent(
        rdf_id="https://marineinfo.org/id/person/45562/",
        name="Bram Van der Streeck",
    )
    plan = prov.Plan(
        rdf_id="my_plan",
    )
    role = prov.Role(
        rdf_id="software_engineer",
    )
    association_id = "bram_software_engineer"
    ref_association = prov.Association(
        rdf_id=association_id,
        had_activity=activity,
        agent=agent,
        had_plan=plan,
        had_role=role,
    )
    graph = ref_association.to_graph()
    association = prov.Association.from_graph(association_id, graph)
    assert ref_association == association


def test_generation_create():
    influence_activity = prov.Activity(rdf_id="eat")
    location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    role = prov.Role(
        rdf_id="work_completed",
    )
    generation = prov.Generation(
        rdf_id="generation",
        activity=influence_activity,
        had_activity=activity,
        had_role=role,
        at_location=location,
        at_time=datetime.now(UTC),
    )
    assert_rdf_type(generation, "http://www.w3.org/ns/prov#Generation")


def test_generation_from_graph():
    influence_activity = prov.Activity(rdf_id="eat")
    location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    role = prov.Role(
        rdf_id="work_completed",
    )
    generation_id = "generation"
    ref_generation = prov.Generation(
        rdf_id=generation_id,
        activity=influence_activity,
        had_activity=activity,
        had_role=role,
        at_location=location,
        at_time=datetime.now(UTC),
    )
    graph = ref_generation.to_graph()
    generation = prov.Generation.from_graph(generation_id, graph)
    assert ref_generation == generation


def test_usage_create():
    influence_entity = prov.Entity(rdf_id="entity")
    location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    role = prov.Role(
        rdf_id="work_completed",
    )
    usage = prov.Usage(
        rdf_id="usage",
        entity=influence_entity,
        had_activity=activity,
        had_role=role,
        at_location=location,
        at_time=datetime.now(UTC),
    )
    assert_rdf_type(usage, "http://www.w3.org/ns/prov#Usage")


def test_usage_from_graph():
    influence_entity = prov.Entity(rdf_id="entity")
    location = prov.Location(rdf_id="http://marineregions.org/mrgid/57661")
    activity = prov.Activity(
        rdf_id="work",
        started_at_time=datetime.now(UTC),
        ended_at_time=datetime.now(UTC),
    )
    role = prov.Role(
        rdf_id="work_completed",
    )
    usage_id = "usage"
    ref_usage = prov.Usage(
        rdf_id=usage_id,
        entity=influence_entity,
        had_activity=activity,
        had_role=role,
        at_location=location,
        at_time=datetime.now(UTC),
    )
    graph = ref_usage.to_graph()
    usage = prov.Usage.from_graph(usage_id, graph)
    assert ref_usage == usage
