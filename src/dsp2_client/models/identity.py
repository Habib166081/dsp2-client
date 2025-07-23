from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Identity(BaseModel):
    """
    User identity model for DSP2 API.

    Designed for safety, clarity, and future extension.
    Fields are type-enforced, documented, and auto-completable.
    """
    id: str = Field(..., description="Unique identifier of the user (e.g., user_TLMLiOYdrPdO7YYuuLdK9Dvw)")
    prefix: Optional[str] = Field(None, description="User's prefix or title (e.g., MIST, DOCT, etc.)")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    date_of_birth: Optional[str] = Field(
        None, description="User's birth date in ISO format (YYYY-MM-DD)")

    model_config = ConfigDict(
        title="UserIdentitySchema",
        frozen=True,
        json_schema_extra={
            "example": {
                "id": "user_TLMLiOYdrPdO7YYuuLdK9Dvw",
                "prefix": "MIST",
                "first_name": "Maurice",
                "last_name": "Dupuis",
                "date_of_birth": "1970-05-06"
            }
        }
    )
