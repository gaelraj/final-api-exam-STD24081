from fastapi import FastAPI
from starlette.responses import Response
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

@app.get("/health")
def health():
    return Response(content="Ok",status_code=200,media_type="text/plain")

class Characteristic(BaseModel):
    ram_memory: float
    rom_memory: float

class Phone(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic

phones_db: List[Phone] = []

@app.post("/phones")
def create_phones(phones: List[Phone]):
    phones_db.extend(phones)
    return Response(
        content=json.dumps({"message": "Phones added", "count": len(phones)}),
        status_code=201,
        media_type="application/json"
    )

@app.get("/phones")
def get_phones():
    return Response(
        content=json.dumps([phone.dict() for phone in phones_db]),
        status_code=200,
        media_type="application/json"
    )

@app.get("/phones/{id}")
def get_phone_by_id(id: str):
    for phone in phones_db:
        if phone.identifier == id:
            return Response(
                content=json.dumps(phone.dict()),
                status_code=200,
                media_type="application/json"
            )
    return Response(
        content=json.dumps({"error": "Phone with given ID does not exist or not found"}),
        status_code=404,
        media_type="application/json"
    )

@app.put("/phones/{id}/characteristics")
def update_phone_characteristics(id: str, characteristics: Characteristic):
    for phone in phones_db:
        if phone.identifier == id:
            phone.characteristics = characteristics
            return Response(
                content=json.dumps(phone.dict()),
                status_code=200,
                media_type="application/json"
            )
    return Response(
        content=json.dumps({"error": "Phone not found"}),
        status_code=404,
        media_type="application/json"
    )    