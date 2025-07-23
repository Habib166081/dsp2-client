from typing import List, TYPE_CHECKING
from dsp2_client.models.account import Account

if TYPE_CHECKING:
    from dsp2_client.core.session import DSP2Session

class AccountService:
    """
    Service to interact with bank accounts via the DSP2 API.
    """

    @staticmethod
    def list_accounts(session: "DSP2Session") -> List[Account]:
        """
        Retrieves all accounts associated with the current user.

        Args:
            session (DSP2Session): An authenticated DSP2Session instance.

        Returns:
            List[Account]: List of user accounts.
        """
        response = session.get("/stet/account")
        return [Account.model_validate(acc) for acc in response.json()]

    @staticmethod
    def get_account(session: "DSP2Session", account_id: str) -> Account:
        """
        Retrieves the details of a single account.

        Args:
            session (DSP2Session): An authenticated DSP2Session instance.
            account_id (str): The account identifier.

        Returns:
            Account: The account object.
        """
        response = session.get(f"/stet/account/{account_id}")
        return Account.model_validate(response.json())
