#!/usr/bin/env python3
import datetime
import json
import pydgraph
def set_schema(client):
    schema = """
    type Passanger {
        age
        gender
        reason
        stay
        ticket
        transit
        connection
        waitTime
        checked_bags
        carry_on
    }
    type Flight {
        aeroline
        to_airport
        from_airport
        day 
        month 
        year
        date
        has
    }
    type Location {
        name
    }
    name: string @index(exact) .
    aeroline: string @index(exact) .
    to_airport: uid @reverse @count .
    from_airport: uid .
    day: int .
    month: int .
    year: int .
    date: datetime .
    has: [uid] @reverse @count .
    age: int .
    gender: string @index(exact) .
    reason: string @index(term) .
    stay: string @index(exact) . 
    ticket: string @index(exact) .
    transit: string .
    connection: string .
    waitTime: int .
    checked_bags: int .
    carry_on: string .
    """
    return client.alter(pydgraph.Operation(schema=schema))


def create_data(client):
    # Create a new transaction.
    with open(r"C:\Users\samab\bases_no_relacionales\BDNR_Project\DGraph\flight_passengers.json", 'r') as file:
        data_list = json.load(file)
    txn = client.txn()
    try:
        response = txn.mutate(set_obj=data_list)

        # Commit transaction.
        commit_response = txn.commit()
        print(f"Commit Response: {commit_response}")

        print(f"UIDs: {response.uids}")
    finally:
        # Clean up. 
        # Calling this after txn.commit() is a no-op and hence safe.
        txn.discard()


def delete_person(client, name):
    # Create a new transaction.
    txn = client.txn()
    try:
        query1 = """query search_person($a: string) {
            all(func: eq(name, $a)) {
               uid
            }
        }"""
        variables1 = {'$a': name}
        res1 = client.txn(read_only=True).query(query1, variables=variables1)
        ppl1 = json.loads(res1.json)
        for person in ppl1['all']:
            print("UID: " + person['uid'])
            txn.mutate(del_obj=person)
            print(f"{name} deleted")
        commit_response = txn.commit()
        print(commit_response)
    finally:
        txn.discard()


def airoline_info(client, name):
    query = """query airoline_info($a: string) {
        all(func:type(Location)){
 			destiny: name
  		flights:~to_airport @filter(eq(airline,$a)){
				date
        airline
        BusinessTicket: count(has @filter(eq(ticket,"Business")))
        FirstTicket: count(has @filter(eq(ticket,"First Class")))
        EconomyTicket: count(has @filter(eq(ticket,"Economy")))
        GenderFemale: count(has @filter(eq(gender,"female"))) 
        GenderMale: count(has @filter(eq(gender,"male"))) 
        
      }  
    
    }
    }"""

    variables = {'$a': name}
    res = client.txn(read_only=True).query(query, variables=variables)
    ppl = json.loads(res.json)

    # Print results.
    print(f"Number of fligths named {name}: {len(ppl['all'])}")
    print(f"Data associated with {name}:\n{json.dumps(ppl, indent=2)}")


def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))
