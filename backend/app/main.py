"""Simple FastAPI backend that serves site metadata and a contact endpoint.
This is separate from Chainlit, which runs its own server for the chat UI.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Join Quran - Demo API")


class ClassItem(BaseModel):
    id: int
    title: str
    level: str


@app.get("/api/site")
def site_data():
    return {
        "title": "Join Quran - Demo",
        "tagline": "Learn Quran in small classes with experienced teachers.",
        "classes": [
            {"id": 1, "title": "Beginner Tajweed", "level": "Beginner"},
            {"id": 2, "title": "Quran Reading", "level": "All Ages"},
            {"id": 3, "title": "Hifz Program", "level": "Advanced"}
        ]
    }


class ContactIn(BaseModel):
    name: str
    email: str
    message: str


@app.post('/api/contact')
def contact(data: ContactIn):
    # In a real app you'd store or email the contact message.
    # Here we just echo back and pretend it succeeded.
    return {"status": "ok", "message": "Received", "data": data}
