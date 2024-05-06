#!/usr/bin/env python3
import uuid
from typing import Optional
from pydantic import BaseModel, Field
import datetime

class Flight(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    airline: str = Field(...)
    from_airport: str = Field(...)
    to_airport: str = Field(...)
    day: int = Field(...)
    month: int = Field(...)
    year: int = Field(...)
    date: str= Field(...)
    duration: int = Field(...)
    age: int = Field(...)
    gender: str = Field(...)
    reason: str = Field(...)
    transit: str = Field(...)
    connection: str = Field(...)
    wait: str = Field(...)
    ticket: str = Field(...)
    checked_bags: int = Field(...)
    carry_on: str = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "airline": "American Airlines",
                "from_airport": "SFO" ,
                "to_airport":  "CUN",
                "day": 14,
                "month": 6,
                "year": 2017,
                "date": "2016-02-23 00:00:00",
                "duration": 664,
                "age": 58,
                "gender": "male",
                "reason": "On vacation/Pleasure",
                "stay": "Hotel",
                "transit": "Airport cab",
                "connection": "False",
                "wait": 0,
                "ticket": "Business",
                "checked_bags": 2,
                "carry_on": "True"
            }
        }

