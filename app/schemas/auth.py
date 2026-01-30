from pydantic import BaseModel

class RegisterSchema(BaseModel):
    name: str
    email: str
    phone: str
    password: str
