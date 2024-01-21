from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str


def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.password = password
