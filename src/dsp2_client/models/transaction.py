from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    """
    Transaction model for DSP2 API.
    Full type validation, immutability, ready for extension.
    """
    id: str = Field(..., description="Transaction identifier")
    label: Optional[str] = Field(None, description="Transaction label or description")
    amount: float = Field(..., description="Transaction amount")
    crdt_dbit_indicator: Optional[str] = Field(None, description="Credit/Debit indicator (CRDT/DBIT)")
    status: Optional[str] = Field(None, description="Transaction status (e.g., BOOK, ...)")
    currency: Optional[str] = Field(None, description="Currency code (ISO 4217)")
    date_operation: Optional[datetime] = Field(None, description="Transaction operation date")
    date_processed: Optional[datetime] = Field(None, description="Transaction processed date")

    model_config = ConfigDict(
        title="TransactionSchema",
        frozen=True,
        json_schema_extra={
            "example": {
                "id": "tran_tzotgyExrpHajnVJTyRrxqUj",
                "label": "Payment at Supermarket",
                "amount": 45.10,
                "crdt_dbit_indicator": "DBIT",
                "status": "BOOK",
                "currency": "EUR",
                "date_operation": "2025-07-23T09:16:48.293Z",
                "date_processed": "2025-07-23T09:17:10.100Z"
            }
        }
    )
