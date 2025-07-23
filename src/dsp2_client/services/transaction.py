from typing import List, TYPE_CHECKING
from dsp2_client.models.transaction import Transaction

if TYPE_CHECKING:
    from dsp2_client.core.session import DSP2Session

class TransactionService:
    """
    Service to fetch account transactions from the DSP2 API.
    """

    @staticmethod
    def list_transactions(
        session: "DSP2Session", account_id: str, page: int = 1, count: int = 10
    ) -> List[Transaction]:
        """
        Retrieves paginated transactions for a specific account.

        Args:
            session (DSP2Session): An authenticated DSP2Session instance.
            account_id (str): The account identifier.
            page (int): Page number (pagination).
            count (int): Number of items per page.

        Returns:
            List[Transaction]: List of transactions.
        """
        response = session.get(
            f"/stet/account/{account_id}/transaction",
            params={"page": page, "count": count}
        )
        return [Transaction.model_validate(tx) for tx in response.json()]
