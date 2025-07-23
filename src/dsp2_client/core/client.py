from typing import List, Optional
from dsp2_client.core.session import DSP2Session
from dsp2_client.services.identity import IdentityService
from dsp2_client.services.account import AccountService
from dsp2_client.services.balance import BalanceService
from dsp2_client.services.transaction import TransactionService
from dsp2_client.models.identity import Identity
from dsp2_client.models.account import Account
from dsp2_client.models.balance import Balance
from dsp2_client.models.transaction import Transaction

class DSP2Client:
    """
    High-level unified interface for DSP2 SDK.
    Encapsulates all services and manages the session lifecycle.
    """

    def __init__(
        self,
        username: str,
        password: str,
        scope: str = "stet ob",
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        log_level: Optional[str] = None,
    ):
        """
        Initialize the DSP2Client and session.

        All parameters are passed to the DSP2Session.
        """
        self._session = DSP2Session(
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url,
            timeout=timeout,
            log_level=log_level,
        )

    def __enter__(self):
        self._session.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.__exit__(exc_type, exc_val, exc_tb)

    def get_identity(self) -> Identity:
        """
        Retrieve the authenticated user's identity.
        """
        return IdentityService.get_identity(self._session)

    def list_accounts(self) -> List[Account]:
        """
        Retrieve all accounts for the authenticated user.
        """
        return AccountService.list_accounts(self._session)

    def get_account(self, account_id: str) -> Account:
        """
        Retrieve a specific account by ID.
        """
        return AccountService.get_account(self._session, account_id)

    def list_balances(self, account_id: str) -> List[Balance]:
        """
        Retrieve all balances for a specific account.
        """
        return BalanceService.list_balances(self._session, account_id)

    def list_transactions(
        self, account_id: str, page: int = 1, count: int = 10
    ) -> List[Transaction]:
        """
        Retrieve paginated transactions for a specific account.
        """
        return TransactionService.list_transactions(self._session, account_id, page, count)
