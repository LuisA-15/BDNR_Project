#!/usr/bin/env python3
import logging
import os
import random

from cassandra.cluster import Cluster

import model

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('hospitals.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars releated to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'hospitals')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')


def print_menu():
    mm_options = {
        1: "Search hospitals by rating",
        2: "Search hospitals by cost",
        3: "Change quality",
        4: "Exit"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])


def set_quality():
    quality = input('**** Quality to use app: ')
    log.info(f"Quality set to {quality}")
    return quality


def get_instrument_value(instrument):
    instr_mock_sum = sum(bytearray(instrument, encoding='utf-8'))
    return random.uniform(1.0, instr_mock_sum)


def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)

    quality = set_quality()

    while(True):
        print_menu()
        option = int(input('Enter your choice: '))
        if option == 1:
            rating = input("Rating: ")
            model.get_facilities_by_rating(session, quality, rating)
        if option == 2:
            min = input('Min cost: ')
            max = input('Max cost: ')
            model.get_facilities_by_cost_range(session, quality, min, max)
        if option == 3:
            quality = set_quality()
        if option == 4:
            exit(0)


if __name__ == '__main__':
    main()
