#!/usr/bin/env python

"""
Generador de datos para proyecto de Bases de Datos No Relacionales
ITESO 
"""
import argparse
import json
import datetime

from random import choice, randint, randrange


airlines = ["American Airlines", "Delta Airlines", "Alaska", "Aeromexico", "Volaris", "Calafia", "British Airways","Qatar Airways", "Virgin Atlantic"]
airports = ["PDX", "GDL", "SJC", "LAX", "JFK", "CUN", "MID", "IAD","BOS", "SFO", "MEX","MTY","OAX", "HND","LCY"]
genders = ["male", "female", "unspecified", "undisclosed"]
reasons = ["On vacation/Pleasure", "Business/Work", "Back Home"]
stays = ["Hotel", "Short-term homestay", "Home", "Friend/Family"]
transits = ["Airport cab", "Car rental", "Mobility as a service", "Public Transportation", "Pickup", "Own car"]
tickets = ["Economy", "Business", "First Class"]
connections = [True, False]
carry_on = [True, False]


def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    rand_date = start_date + datetime.timedelta(days=random_number_of_days)
    return rand_date


def generate_dataset(output_file, rows):
    
    
        jsonFlight=[]
        for k in airports:
            locations={
                "uid":"_:"+k,
                "dgraph.type":"Location",
                "name": k
            }
            jsonFlight.append(locations)
        for i in range(rows):
            airline=choice(airlines)
            from_airport = choice(airports)
            to_airport = choice(airports)
            while from_airport == to_airport:
                to_airport = choice(airports)
            date = random_date(datetime.datetime(2013, 1, 1), datetime.datetime(2023, 4, 25))
            
            passangerNum=randint(10,30)
            plist=[]
            for j in range(passangerNum):
                reason = choice(reasons)
                stay = choice(stays)
                connection = choice(connections)
                wait = randint(30, 720)
                transit = choice(transits)
                if not connection:
                    wait = 0
                else:
                    transit = ""
                if reason == "Back Home":
                    stay = "Home"
                    connection = False
                    wait = 0
                    transit = choice(transits)
                passanger={
                "dgraph.type":"Passanger",
                "age": randint(1,90),
                "gender": choice(genders),
                "reason": reason,
                "stay": stay,
                "transit": transit,
                "connection": connection,
                "wait": wait,
                "ticket": choice(tickets),
                "checked_bags": randint(0, 3),
                "carry_on": choice(carry_on)
                }
                plist.append(passanger)
                
                 
            line = {
                "dgraph.type": "Flight",
                "airline": airline,
                "from_airport":{"uid":"_:"+ from_airport},
                "to_airport":  {"uid":"_:"+ to_airport},
                "day": date.day,
                "month": date.month,
                "year": date.year,
                "date": date.strftime("%Y-%m-%d"),
                "duration": randint(25, 1000),
                "has": plist,
                
               
            }
            jsonFlight.append(line)
        with open(output_file, 'w') as file:
            json.dump(jsonFlight, file, indent=4, default=str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output",
            help="Specify the output filename of your csv, defaults to: flight_passengers.json", default="flight_passengers.json")
    parser.add_argument("-r", "--rows",
            help="Amount of random generated entries for the dataset, defaults to: 100", type=int, default=50)

    args = parser.parse_args()
    
    print(f"Generating {args.rows} for flight passenger dataset")
    generate_dataset(args.output, args.rows)
    print(f"Completed generating dataset in {args.output}")


