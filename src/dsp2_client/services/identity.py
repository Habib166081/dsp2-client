from typing import TYPE_CHECKING
from dsp2_client.models.identity import Identity

if TYPE_CHECKING:
    from dsp2_client.core.session import DSP2Session

class IdentityService:
    """
    Service to retrieve user identity from the DSP2 API.
    """

    @staticmethod
    def get_identity(session: "DSP2Session") -> Identity:
        """
        Fetches the identity of the currently authenticated user.

        Args:
            session (DSP2Session): An authenticated DSP2Session instance.

        Returns:
            Identity: The user identity object.
        """
        response = session.get("/stet/identity")
        return Identity.model_validate(response.json())
