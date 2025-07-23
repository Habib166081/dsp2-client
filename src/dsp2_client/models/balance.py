from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Balance(BaseModel):
    """
    Account balance model for DSP2 API.
    Fully validated, type-safe, immutable.
    """
    id: str = Field(..., description="Balance identifier")
    name: Optional[str] = Field(None, description="Balance name")
    amount: float = Field(..., description="Amount available in the balance")
    currency: str = Field(..., description="Currency code (ISO 4217)")
    type: Optional[str] = Field(None, description="Balance type (e.g., CLBD, ...)")

    model_config = ConfigDict(
        title="BalanceSchema",
        frozen=True,
        json_schema_extra={
            "example": {
                "id": "blnc_YUUO26FOwggqOMvyhsr9ojzA",
                "name": "Main Balance",
                "amount": 2500.50,
                "currency": "EUR",
                "type": "CLBD"
            }
        }
    )
