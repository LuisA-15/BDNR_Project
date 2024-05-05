import os

stmt = 'INSERT INTO hospitals_heart_attack_procedure (Facility_Name, City, State, Facility_Type, Rating_Overall, Cost, Quality) VALUES ("{}", "{}", "{}", "{}", {}, {}, "{}");\n'

CQL_FILE = 'data.cql'
DATA_FILE = 'hospitals_clean.csv'

with open(os.path.dirname(os.path.abspath(__file__)) + '\\' + DATA_FILE, 'r') as data:
    with open(CQL_FILE, 'w') as cql:
        for line in data:
            cql.write(stmt.format(*line.strip('\n').split(',')))