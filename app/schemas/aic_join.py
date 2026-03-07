from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, Field, ConfigDict, ValidationInfo
import re
import json

# This is for when a user submits the form. (The In data)
class AICJoinCreate(BaseModel):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: EmailStr
    country: str
    city: str
    organization: str | None = None
    role: str | None = None
    interests: list[str]
    other_interest: list[str] | None = Field(default=None, alias="otherInterest")
    newsletter: bool = True

    @field_validator("interests", "other_interest", mode="before")
    @classmethod
    def parse_to_list(cls, v, info: ValidationInfo):
        if v is None:
            return None
        
        # If it's a string, handle various separators
        if isinstance(v, str):
            # Try splitting by comma or semicolon
            if ',' in v or ';' in v:
                items = [item.strip() for item in re.split(r'[,;]+', v) if item.strip()]
            else:
                # If no comma or semicolon, treat as a single item list if not empty
                items = [v.strip()] if v.strip() else []
            
            # Validation for interests (must not be empty)
            if info.field_name == "interests" and not items:
                raise ValueError("At least one interest must be selected")
            
            return items
            
        # If it's already a list
        if isinstance(v, list):
            # Validation for interests (must not be empty)
            if info.field_name == "interests" and not v:
                raise ValueError("At least one interest must be selected")
            return v
        
        return v

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "first_name": "Arjun",
                "last_name": "MS",
                "email": "arjunms@example.com",
                "country": "India",
                "city": "Palakkad",
                "organization": "Permute",
                "role": "Developer",
                "interests": ["AI Engineering", "AI Research"],
                "otherInterest": "Ethics, AI Research",
                "newsletter": True
            }
        }
    )

# This is for when the API replies back to the frontend after successfully saving. (The Out Data)
class AICJoinResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    country: str
    city: str
    organization: str | None
    role: str | None
    interests: list[str]
    other_interest: list[str] | None
    newsletter: bool
    created_at: datetime

    @field_validator("interests", "other_interest", mode="before")
    @classmethod
    def parse_json(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return v
        return v

    model_config = ConfigDict(from_attributes=True)
