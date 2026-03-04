from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, model_validator


class CategoryEnum(str, Enum):
    individual = "individual"
    organisation = "organisation"
    government = "government"


class WhatDefinesYouEnum(str, Enum):
    activist = "activist"
    student = "student"
    researcher = "researcher"
    professional = "professional"
    volunteer = "volunteer"
    journalist = "journalist"
    policy_maker = "policy_maker"
    other = "other"


class JoinCreate(BaseModel):
    site_id: str
    category: CategoryEnum
    what_defines_you: WhatDefinesYouEnum
    what_to_share: str
    link: Optional[str] = None

    # Anonymous toggle: if True, personal details are not required
    is_anonymous: bool = False

    # Personal details — required only when is_anonymous is False
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    @model_validator(mode="after")
    def check_non_anonymous_details(self) -> "JoinCreate":
        if not self.is_anonymous:
            missing = []
            if not self.name:
                missing.append("name")
            if not self.email:
                missing.append("email")
            if not self.phone:
                missing.append("phone")
            if missing:
                raise ValueError(
                    f"The following fields are required when not anonymous: {', '.join(missing)}"
                )
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "site_id": "tpm-website",
                "category": "individual",
                "what_defines_you": "activist",
                "what_to_share": "I want to share my experience with climate advocacy in my local community.",
                "link": "https://example.com/my-story",
                "is_anonymous": False,
                "name": "Umar Farooq",
                "email": "umar@example.com",
                "phone": "+91 98765 43210"
            }
        }


class JoinResponse(BaseModel):
    id: int
    site_id: str
    category: str
    what_defines_you: str
    what_to_share: str
    link: Optional[str]
    is_anonymous: bool
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]

    class Config:
        from_attributes = True