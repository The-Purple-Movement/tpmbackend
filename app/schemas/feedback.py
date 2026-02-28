from pydantic import BaseModel, EmailStr

class FeedbackCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Umar",
                "email": "umar@email.com",
                "message": "The website onboarding was smooth!"
            }
        }

class FeedbackResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    message: str

    class Config:
        from_attributes = True