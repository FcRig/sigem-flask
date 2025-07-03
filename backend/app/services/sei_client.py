import requests


class SEIClient:
    """Client to handle authentication with the SEI system."""

    LOGIN_URL = (
        "https://sei.prf.gov.br/sip/login.php?sigla_sistema=SEI&sigla_orgao_sistema=PRF"
    )

    def __init__(self, session: requests.Session | None = None):
        self.session = session or requests.Session()

    def login(self, usuario: str, senha: str, token: str) -> None:
        """Perform SEI login with password and second factor token."""

        payload = {
            "txtUsuario": usuario,
            "pwdSenha": senha,
            "selOrgao": "0",
            "Acessar": "",
            "hdnAcao": "2",
        }
        resp = self.session.post(self.LOGIN_URL, data=payload)
        resp.raise_for_status()

        payload2 = {"txtCodigoAcesso": token, "hdnAcao": "3"}
        resp = self.session.post(self.LOGIN_URL, data=payload2)
        resp.raise_for_status()
