import os
import requests


class SiscomClient:
    """Simple client to interact with the SISCOM service."""

    def __init__(self, endpoint: str | None = None):
        self.endpoint = endpoint or os.getenv("SISCOM_ENDPOINT", "http://example.com/siscom")

    def pesquisar_ai(self, numero: str) -> dict:
        """Search for an Auto de Infracao and return filtered fields."""
        response = requests.get(f"{self.endpoint}/{numero}")
        response.raise_for_status()
        payload = response.json() if response.content else {}

        fields = [
            "numeroAuto",
            "codigoInfracao",
            "descAbreviadaInfracao",
            "placa",
            "renavam",
            "kmInfracao",
            "municipioInfracao",
            "valorInfracao",
        ]
        return {field: payload.get(field) for field in fields}
