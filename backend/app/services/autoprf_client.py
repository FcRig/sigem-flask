import requests
from datetime import datetime


class AutoPRFClient:
    """Simple client to interact with the AutoPRF HTTP API."""

    BASE_URL = "https://auto.prf.gov.br/api"

    def __init__(self, jwt_token: str | None = None):
        self.jwt_token = jwt_token or ""

    def login(self, cpf: str, password: str, token: str) -> str:
        """ Autentica no sistema AutoPRF e retorna o token JWT da sessão."""   
             
        payload = {
            "ip": "0.0.0.0",
            "usuario": cpf,
            "senha": password,
            "token": token,
        }

        try:
            response = requests.post(f"{self.BASE_URL}/auth/login", json=payload)
            response.raise_for_status()

            jwt = response.text.strip()
            if not jwt or len(jwt) < 20:
                raise ValueError("Token JWT ausente ou inválido.")

            self.jwt_token = jwt
            return jwt

        except requests.HTTPError as e:
            print(f"[AutoPRF] Erro HTTP na autenticação: {e} - Status: {response.status_code}")
            print(f"Resposta do servidor: {response.text}")
            raise

        except Exception as e:
            print(f"[AutoPRF] Erro inesperado no login: {e}")
            raise


    def pesquisa_auto_infracao(self, numero: str) -> dict:
        """Return data about an Auto de Infracao in the same structure used by the frontend."""
        headers = {}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
        # First request retrieves the page information so we can obtain the
        # identifier of the auto de infração
        response = requests.get(
            f"{self.BASE_URL}/auto-infracao/page",
            params={"numero": numero},
            headers=headers,
        )
        response.raise_for_status()
        data = response.json() if response.content else {}
        item = (data.get("items") or [{}])[0]

        auto_id = item.get("id")

        result = {
            "infracao": {},
            "veiculo": {},
            "local": {},
            "medicoes": {},
            "equipamento": {},
            "observacoes": None,
        }

        if not auto_id:
            # If we could not find the identifier we return an empty result
            return result

        # Fetch full details for the auto using its id
        response = requests.get(
            f"{self.BASE_URL}/auto-infracao/{auto_id}",
            headers=headers,
        )
        response.raise_for_status()
        item = response.json() if response.content else {}
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
