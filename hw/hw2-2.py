'''
# Run in desktop neo4j

MERGE (elon:Person {name: "Elon Musk"})

MERGE (spacex:Organization {name: "SpaceX"})
MERGE (tesla:Organization {name: "Tesla"})

MERGE (falcon9:Product {name: "Falcon 9"})

MERGE (california:Location {name: "California"})

// Properties for dates (could be nodes if needed)
MERGE (tesla)-[:FOUNDED_IN_YEAR]->(:Date {year: 2003})
MERGE (falcon9)-[:LAUNCHED_IN_YEAR]->(:Date {year: 2010})

// Relationships
MERGE (elon)-[:CEO_OF]->(spacex)
MERGE (elon)-[:CEO_OF]->(tesla)

MERGE (tesla)-[:FOUNDED_IN_LOCATION]->(california)

MERGE (spacex)-[:LAUNCHED]->(falcon9)


'''
from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://127.0.0.1:7687", auth=("neo4j", "11111111")) # 11111111


def get_ceos(tx):
    query = """
    MATCH (p:Person)-[:CEO_OF]->(o:Organization)
    WHERE o.name IN ["SpaceX", "Tesla"]
    RETURN p.name AS ceo, o.name AS company
    """
    return tx.run(query).data()


# No founded year for SpaceX, location is optional, so location will be return as null
def get_company_foundation_info(tx):
    query = """
    MATCH (o:Organization)-[:FOUNDED_IN_YEAR]->(d:Date)
    OPTIONAL MATCH (o)-[:FOUNDED_IN_LOCATION]->(loc:Location)
    RETURN o.name AS company, d.year AS founded_year, loc.name AS location
    """
    return tx.run(query).data()


def get_spacex_launched_products(tx):
    query = """
    MATCH (o:Organization {name: "SpaceX"})-[:LAUNCHED]->(p:Product)
    OPTIONAL MATCH (p)-[:LAUNCHED_IN_YEAR]->(d:Date)
    RETURN o.name AS organization, p.name AS product, d.year AS launch_year
    """
    return tx.run(query).data()


def get_ceo_companies(tx, person_name):
    query = """
    MATCH (p:Person {name: $person_name})-[:CEO_OF]->(o:Organization)
    RETURN o.name AS company
    """
    return tx.run(query, person_name=person_name).data()


# ---- Run the queries ----
with driver.session() as session:
    print("CEOs of SpaceX and Tesla:")
    ceos = session.execute_read(get_ceos)
    for row in ceos:
        print(row)

    print("\nCompany founding info:")
    info = session.execute_read(get_company_foundation_info)
    for row in info:
        print(row)

    print("\nProducts launched by SpaceX:")
    launches = session.execute_read(get_spacex_launched_products)
    for row in launches:
        print(row)

    name_input = "Elon Musk"
    companies = session.execute_read(get_ceo_companies, name_input)
    print(f"\nCompanies where {name_input} is CEO:")
    for row in companies:
        print("-", row["company"])

# ---- Close the driver ----
driver.close()

