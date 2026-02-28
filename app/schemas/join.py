from pydantic import BaseModel, EmailStr

class JoinCreate(BaseModel):
    name: str
    email: EmailStr
    role: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Umar",
                "email": "umar@email.com",
                "role": "Developer"
            }
        }

class JoinResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True