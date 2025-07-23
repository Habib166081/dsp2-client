from dsp2_client.services.identity import IdentityService
from dsp2_client.models.identity import Identity


def test_get_identity_returns_valid_identity(monkeypatch):
    # Prépare un faux session avec méthode get qui retourne une "fake" réponse API
    class FakeSession:
        def get(self, path):
            assert path == "/stet/identity"

            class FakeResponse:
                def json(self):
                    return {
                        "id": "user_TLMLiOYdrPdO7YYuuLdK9Dvw",
                        "prefix": "MIST",
                        "first_name": "Maurice",
                        "last_name": "Dupuis",
                        "date_of_birth": "1970-05-06"
                    }

            return FakeResponse()

    session = FakeSession()
    identity = IdentityService.get_identity(session)
    assert isinstance(identity, Identity)
    assert identity.first_name == "Maurice"
    assert identity.id.startswith("user_")
