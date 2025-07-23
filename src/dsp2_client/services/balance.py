from typing import List, TYPE_CHECKING
from dsp2_client.models.balance import Balance

if TYPE_CHECKING:
    from dsp2_client.core.session import DSP2Session

class BalanceService:
    """
    Service to retrieve account balances from the DSP2 API.
    """

    @staticmethod
    def list_balances(session: "DSP2Session", account_id: str) -> List[Balance]:
        """
        Retrieves all balances for a given account.

        Args:
            session (DSP2Session): An authenticated DSP2Session instance.
            account_id (str): The account identifier.

        Returns:
            List[Balance]: List of balances for the account.
        """
        response = session.get(f"/stet/account/{account_id}/balance")
        json_data = response.json()
        # The API may return either a list or a dict, handle both gracefully
        if isinstance(json_data, list):
            return [Balance.model_validate(bal) for bal in json_data]
        return [Balance.model_validate(json_data)]
