#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Flight

router = APIRouter()

@router.post("/", response_description="Post a flight", status_code=status.HTTP_201_CREATED, response_model=Flight)
def create_book(request: Request, fligth: Flight = Body(...)):
    fligth = jsonable_encoder(fligth)
    new_fligth = request.app.database["flight"].insert_one(fligth)
    created_fligth = request.app.database["flight"].find_one(
        {"_id": new_fligth.inserted_id}
    )

    return created_fligth


@router.get("/", response_description="Get all flight", response_model=List)
def list_books(request: Request, to_airport: str, month: int=0 ):
    if month ==0:
        aggrega = [
        {
            "$match":{
                 "transit": {"$in": ["Car rental"]},
                 "to_airport": to_airport,
                 "connection": "False",
                 "age":{"$gte": 21},
                 "reason": {"$nin":["Back Home"]},
                 
            }
        },
        {
           
            "$group": {
                "_id": "$month", 
                "More car rental": {"$sum": 1}
            }
            
        },
        { "$sort" : { "More car rental" : -1 } },
        { "$limit" : 1 }
        
        
    ]
    else:  
        aggrega = [
            {
                "$match":{
                    "transit": {"$in": ["Car rental"]},
                    "to_airport": to_airport,
                    "month": month,
                    "connection": "False",
                    "age":{"$gte": 21},
                    "reason": {"$nin":["Back Home"]},
                    
                }
            },
            { "$project" : 
                { "_id" : 0, 
                "gender": 1, 
                "age": 1,
                "reason":1,
                "to_airport":1
                } }
        ]
    Flights=list(request.app.database["flight"].aggregate(aggrega))
    return Flights


@router.get("/{id}", response_description="Get a single book by id", response_model=Flight)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

