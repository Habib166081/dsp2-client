from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Account(BaseModel):
    """
    Bank account model for DSP2 API.
    Immutable, documented, type-safe, and future-proof.
    """
    id: str = Field(..., description="Unique account identifier")
    type: str = Field(..., description="Account type (e.g., CARD, CACC, etc.)")
    usage: Optional[str] = Field(None, description="Account usage (e.g., PRIV, ORGA, etc.)")
    iban: Optional[str] = Field(None, description="IBAN of the account, if available")
    name: Optional[str] = Field(None, description="Account display name")
    currency: Optional[str] = Field(None, description="Currency code (ISO 4217)")

    model_config = ConfigDict(
        title="AccountSchema",
        frozen=True,
        json_schema_extra={
            "example": {
                "id": "acct_Ms99YLcC2LETpC4KKK7VcjPY",
                "type": "CARD",
                "usage": "PRIV",
                "iban": "FR1420041010050500013M04406",
                "name": "Compte Carte",
                "currency": "USD"
            }
        }
    )
