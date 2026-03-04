import re
from typing import List, Optional
from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime

# ── Valid enum values ────────────────────────────────────────────────────────
VALID_ROLES = {"Student", "Teacher", "Thinker", "Creator/Builder", "Other"}
VALID_STATUSES = {"pending", "approved", "rejected"}
E164_PATTERN = re.compile(r"^\+[1-9]\d{6,14}$")


# ── Request body ─────────────────────────────────────────────────────────────
class MemberCreate(BaseModel):
    site_id: str
    name: str
    roles: List[str]
    other_role: Optional[str] = None
    purpose: str
    media_links: Optional[str] = None
    excite_reasons: List[str]
    whatsapp_opt_in: bool = False
    whatsapp_number: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v: str) -> str:
        if len(v.strip()) < 2:
            raise ValueError("name must be at least 2 characters")
        return v.strip()

    @field_validator("roles")
    @classmethod
    def roles_valid(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("at least one role is required")
        invalid = set(v) - VALID_ROLES
        if invalid:
            raise ValueError(
                f"invalid role(s): {invalid}. "
                f"Valid values: {VALID_ROLES}"
            )
        return v

    @field_validator("purpose")
    @classmethod
    def purpose_min_length(cls, v: str) -> str:
        if len(v.strip()) < 20:
            raise ValueError("purpose must be at least 20 characters")
        if len(v) > 2000:
            raise ValueError("purpose must not exceed 2000 characters")
        return v.strip()

    @field_validator("excite_reasons")
    @classmethod
    def excite_reasons_not_empty(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("at least one excite reason is required")
        return v

    @model_validator(mode="after")
    def check_other_role_and_whatsapp(self) -> "MemberCreate":
        if "Other" in (self.roles or []) and not self.other_role:
            raise ValueError("other_role is required when roles includes 'Other'")
        if self.whatsapp_opt_in and not self.whatsapp_number:
            raise ValueError("whatsapp_number is required when whatsapp_opt_in is true")
        if self.whatsapp_number and not E164_PATTERN.match(self.whatsapp_number):
            raise ValueError(
                "whatsapp_number must be in E.164 format, e.g. +919876543210"
            )
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "site_id": "purple-movement",
                "name": "Aisha Khan",
                "roles": ["Student", "Creator/Builder"],
                "other_role": None,
                "purpose": "I want to connect with builders who believe in change.",
                "media_links": "https://linkedin.com/in/aisha",
                "excite_reasons": [
                    "Learning from diverse perspectives",
                    "Being part of something bigger"
                ],
                "whatsapp_opt_in": True,
                "whatsapp_number": "+919876543210"
            }
        }
    }


# ── Minimal response after creation ─────────────────────────────────────────
class MemberCreateResponse(BaseModel):
    id: str
    site_id: str
    name: str
    status: str
    joined_at: datetime

    model_config = {"from_attributes": True}


# ── Full member detail (used in list + single-get) ───────────────────────────
class MemberDetail(BaseModel):
    id: str
    site_id: str
    name: str
    roles: List[str]
    other_role: Optional[str]
    purpose: str
    media_links: Optional[str]
    excite_reasons: List[str]
    whatsapp_opt_in: bool
    whatsapp_number: Optional[str]
    status: str
    certificate_id: Optional[str]
    joined_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Paginated list wrapper ───────────────────────────────────────────────────
class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int


class MemberListResponse(BaseModel):
    success: bool = True
    data: List[MemberDetail]
    meta: PaginationMeta


# ── Standard single-item success responses ───────────────────────────────────
class MemberCreateEnvelope(BaseModel):
    success: bool = True
    data: MemberCreateResponse


# ── Count response ───────────────────────────────────────────────────────────
class MemberCountResponse(BaseModel):
    success: bool = True
    data: dict  # {"count": int, "site_id": str | None}
