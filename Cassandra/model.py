#!/usr/bin/env python3
import logging

# Set logger
log = logging.getLogger()


CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

CREATE_HOSPITALS_HEART_ATTACK_PROCEDURE_BY_RATING_TABLE = """
    CREATE TABLE IF NOT EXISTS heart_attack_procedure_by_rating (
        facility_Name TEXT,
        city TEXT,
        state TEXT,
        facility_type TEXT,
        rating_overall INT,
        cost DECIMAL,
        quality TEXT,
        PRIMARY KEY ((quality), rating_overall, facility_name, city)
    ) WITH CLUSTERING ORDER BY (rating_overall DESC, facility_name DESC, city DESC)
"""

CREATE_HOSPITALS_HEART_ATTACK_PROCEDURE_BY_COST_TABLE = """
    CREATE TABLE IF NOT EXISTS heart_attack_procedure_by_cost (
        facility_Name TEXT,
        city TEXT,
        state TEXT,
        facility_type TEXT,
        rating_overall INT,
        cost DECIMAL,
        quality TEXT,
        PRIMARY KEY ((quality), cost, facility_name, city)
    ) WITH CLUSTERING ORDER BY (cost ASC, facility_name DESC, city DESC)
"""


SELECT_FACILITIES_BY_RATING = """
    SELECT facility_name, city, state, facility_type, rating_overall, cost
    FROM heart_attack_procedure_by_rating
    WHERE quality = ? AND rating_overall >= ?
"""

SELECT_FACILITIES_BY_COST = """
    SELECT facility_name, city, state, facility_type, rating_overall, cost
    FROM heart_attack_procedure_by_cost
    WHERE quality = ? AND cost >= ? AND cost =< ?
"""

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))


def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_HOSPITALS_HEART_ATTACK_PROCEDURE_BY_RATING_TABLE)
    session.execute(CREATE_HOSPITALS_HEART_ATTACK_PROCEDURE_BY_COST_TABLE)


def get_facilities_by_rating(session, quality, rating):
    log.info(f'Retrieving facilities with {quality} quality procedure and {rating} overall rating or better')
    stmt = session.prepare(SELECT_FACILITIES_BY_RATING)
    rows = session.execute(stmt, [quality, int(rating)])
    for row in rows:
        print(f'=== Facility: {row.facility_name} ===')
        print(f'- Rating overall: {row.rating_overall}')
        print(f'- Cost: {row.cost}')

    
def get_facilities_by_cost_range(session, quality, min, max):
    log.info(f'Retrieving facilities with {quality} quality procedure and {min} - {max} cost range')
    stmt = session.prepare(SELECT_FACILITIES_BY_COST)
    rows = session.execute(stmt, [quality, int(min), int(max)])
    for row in rows:
        print(f'=== Facility: {row.facility_name} ===')
        print(f'- Cost: {row.cost}')
        print(f'- Rating overall: {row.rating_overall}')


def load_data(session):
    stmt = session.prepare("SOURCE '/tools/data.cql'")
    session.execute(stmt)