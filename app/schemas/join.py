from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, field_validator, model_validator


class CategoryEnum(str, Enum):
    individual = "individual"
    organisation = "organisation"
    government = "government"


class WhatDefinesYouEnum(str, Enum):
    # Individual
    student = "Student"
    creator_entrepreneur = "Creator / Entrepreneur"
    enthusiast_professional = "Enthusiast / Professional mentoring, volunteering, or supporting initiatives"

    # Government
    government_body = "Government Body – Local, state, or national departments supporting initiatives"
    policy_maker = "Policy Maker"
    government_affiliated_institution = "Government Affiliated Institution"
    public_sector = "Public Sector – State-run companies and enterprises contributing to programs"

    # Organisation
    nonprofit_ngo = "Nonprofit / NGO: Supporting social and community initiatives"
    startup_company = "Startup / Company: Building and scaling impactful solutions"
    educational_training_institution = "Educational / Training Institution: Enabling learning and skill development"
    research_innovation_lab = "Research / Innovation Lab: Driving research and practical solutions"

    # Catch-all
    other = "Other"


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

    @field_validator("what_defines_you", mode="before")
    @classmethod
    def normalize_what_defines_you(cls, value):
        # Strip trailing/leading whitespace the frontend may include
        if isinstance(value, str):
            stripped = value.strip()
            # Exact match first
            for member in WhatDefinesYouEnum:
                if member.value == stripped:
                    return stripped
            # Case-insensitive fallback
            lower = stripped.lower()
            for member in WhatDefinesYouEnum:
                if member.value.lower() == lower:
                    return member.value
            return stripped  # let Pydantic raise the enum error
        return value

    @field_validator("email", "name", "phone", mode="before")
    @classmethod
    def empty_str_to_none(cls, value):
        # Coerce empty strings to None so EmailStr validation doesn't fire on blank anonymous fields
        if isinstance(value, str) and value.strip() == "":
            return None
        return value

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
                "what_defines_you": "Creator / Entrepreneur",
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