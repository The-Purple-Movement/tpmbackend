from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    site_id: str
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "site_id": "tpm-website",
                "rating": 4,
                "message": "The website is clean and easy to navigate. Would love more content on campaigns."
            }
        }


class FeedbackResponse(BaseModel):
    id: int
    site_id: str
    rating: int
    message: str

    class Config:
        from_attributes = True