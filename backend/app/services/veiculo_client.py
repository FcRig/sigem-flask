import requests

class VeiculoClient:
    """Client to consult vehicle data by plate."""

    BASE_URL = (
        "http://10.0.11.220:8080/MotorConsultas/consulta?matricula=1535421&cpf="
        "68109911234&objeto=VEICULO&campo=PLACA&sistema=22&chave={placa}"
    )

    def consultar_placa(self, placa: str) -> dict:
        """Query the vehicle service for the provided plate."""
        url = self.BASE_URL.format(placa=placa)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
