import requests
from datetime import datetime


class AutoPRFClient:
    """Simple client to interact with the AutoPRF HTTP API."""

    BASE_URL = "https://auto.prf.gov.br/api"

    def __init__(self, jwt_token: str | None = None):
        self.jwt_token = jwt_token or ""

    def login(self, cpf: str, password: str, token: str) -> str:
        """Authenticate on AutoPRF and return the session JWT."""
        payload = {
            "ip": "0.0.0.0",
            "usuario": cpf,
            "senha": password,
            "token": token,
        }
        response = requests.post(f"{self.BASE_URL}/auth/login", json=payload)
        response.raise_for_status()
        data = response.json() if response.content else {}
        jwt = data.get("token") or data.get("jwt") or ""
        self.jwt_token = jwt
        return jwt

    def pesquisa_auto_infracao(self, numero: str) -> dict:
        """Return data about an Auto de Infracao in the same structure used by the frontend."""
        headers = {}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
        response = requests.get(
            f"{self.BASE_URL}/auto-infracao/page",
            params={"numero": numero},
            headers=headers,
        )
        response.raise_for_status()
        data = response.json() if response.content else {}
        item = (data.get("items") or [{}])[0]

        result = {
            "infracao": {},
            "veiculo": {},
            "local": {},
            "medicoes": {},
            "equipamento": {},
            "observacoes": None,
        }

        if not item:
            return result

        # Informacoes da infracao
        codigo = item.get("codigoInfracao")
        descricao = item.get("descricaoInfracao")
        if codigo or descricao:
            result["infracao"]["codigo_descricao"] = f"{codigo} - {descricao}" if codigo else descricao
        result["infracao"]["amparo_legal"] = item.get("amparoLegal")
        result["infracao"]["tipo_abordagem"] = (
            "Com Abordagem" if item.get("comAbordagem") else "Sem Abordagem"
        )

        # Veiculo
        result["veiculo"]["emplacamento"] = item.get("tipoEmplacamento")
        result["veiculo"]["placa"] = item.get("placa")
        result["veiculo"]["renavam"] = item.get("renavam")
        result["veiculo"]["chassi"] = item.get("chassi")
        result["veiculo"]["uf"] = item.get("uf")

        # Localizacao
        result["local"]["codigo_municipio_uf"] = item.get("nomeMunicipio")
        result["local"]["rodovia"] = item.get("rodoviaSigla")
        km = item.get("km")
        result["local"]["km"] = str(km) if km is not None else None
        result["local"]["sentido"] = item.get("sentido")
        if item.get("dataHora"):
            dt = datetime.fromisoformat(item["dataHora"])
            result["local"]["data_hora"] = dt.strftime("%d/%m/%Y %H:%M:%S")

        result["observacoes"] = item.get("observacao")
        return result
