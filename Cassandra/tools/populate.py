import os

stmt1 = "INSERT INTO heart_attack_procedure_by_rating (facility_Name, city, state, facility_type, rating_overall, cost, quality) VALUES ('{}', '{}', '{}', '{}', {}, {}, '{}');\n"
stmt2 = "INSERT INTO heart_attack_procedure_by_cost (facility_Name, city, state, facility_type, rating_overall, cost, quality) VALUES ('{}', '{}', '{}', '{}', {}, {}, '{}');\n"

CQL_FILE = 'data.cql'
DATA_FILE = 'hospitals_clean.csv'

with open(os.path.dirname(os.path.abspath(__file__)) + '\\' + DATA_FILE, 'r') as data:
    with open(CQL_FILE, 'w') as cql:
        for line in data:
            cql.write(stmt1.format(*line.strip('\n').split(',')))
            cql.write(stmt2.format(*line.strip('\n').split(',')))