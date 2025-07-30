import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
import unicodedata
from datetime import datetime


class SEIClient:
    """Client to handle authentication with the SEI system."""

    BASE_URL = "https://sei.prf.gov.br/sei/"
    LOGIN_URL = (
        "https://sei.prf.gov.br/sip/login.php?sigla_sistema=SEI&sigla_orgao_sistema=PRF"
    )

    def __init__(self, session: requests.Session | None = None):
        self.session = session or requests.Session()
        self.home_html: str | None = None

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
        self.home_html = resp.text        

    def _normalize(self, text: str) -> str:
        return (
            unicodedata.normalize("NFKD", text or "")
            .encode("ASCII", "ignore")
            .decode("ASCII")
            .strip()
            .lower()
        )

    def get_link_by_action(self, html: str, action: str) -> str | None:
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all("a", href=True):
            if link.get("link") == action:                
                return urljoin(self.BASE_URL, link["href"].replace("&amp;", "&"))
        return None

    def get_link_by_text(self, html: str, text: str) -> str | None:
        desired = self._normalize(text)
        soup = BeautifulSoup(html, "html.parser")
        table = soup.select_one("#tblTipoProcedimento")
        if not table:
            return None
        for link in table.find_all("a", href=True):
            if self._normalize(link.get_text()) == desired:
                return urljoin(self.BASE_URL, link["href"].replace("&amp;", "&"))
        return None

    def list_process_types(self) -> list[dict[str, str]]:
        print("Listing process types...")
        if not self.home_html:
            raise RuntimeError("Not logged in")

        url = self.get_link_by_action(self.home_html, "procedimento_escolher_tipo") 
        print(f"Action URL: {url}")
        if not url:
            raise RuntimeError("Action link not found")

        resp = self.session.get(url)
        resp.encoding = "iso-8859-1"
        html = resp.text        
        soup = BeautifulSoup(html, "html.parser")
        table = soup.select_one("#tblTipoProcedimento")
        if not table:
            return []
        result: list[dict[str, str]] = []
        for link in table.find_all("a", href=True):
            text_val = link.get_text(strip=True)
            href = link["href"]
            parsed = urlparse(href)
            q = parse_qs(parsed.query)
            type_id = (q.get("id_tipo_procedimento") or [""])[0]
            result.append({"id": type_id, "text": text_val})
        return result

    def create_process(self, type_id: str, type_name: str, description: str) -> requests.Response:
        if not self.home_html:
            raise RuntimeError("Not logged in")

        # Open type page
        action_url = self.get_link_by_action(self.home_html, "procedimento_escolher_tipo")
        if not action_url:
            raise RuntimeError("Action link not found")

        resp = self.session.get(action_url)
        resp.encoding = "iso-8859-1"
        link = self.get_link_by_text(resp.text, type_name)
        if not link:
            raise RuntimeError("Process type not found")

        resp = self.session.get(link)
        resp.encoding = "iso-8859-1"
        soup = BeautifulSoup(resp.text, "html.parser")
        form = soup.select_one("#frmProcedimentoCadastro")
        if not form:
            raise RuntimeError("Form not found")        

        action = form.get("action")
        if not action:
            raise RuntimeError("Form action not found")
        post_url = urljoin(self.BASE_URL, action)

        payload = {
            "hdnInfraTipoPagina": "1",
            "rdoProtocolo": "A",
            "selTipoProcedimento": type_id,
            "txtDescricao": description,
            "selGrauSigilo": "null",
            "rdoNivelAcesso": "0",
            "hdnFlagProcedimentoCadastro": "2",
            "hdnIdTipoProcedimento": type_id,
            "hdnNomeTipoProcedimento": type_name,
            "hdnAssuntos": "727",
            "hdnSinIndividual": "N",
            "hdnDtaGeracao": datetime.now().strftime("%d/%m/%Y"),
        }

        print(payload)

        return self.session.post(post_url, data=payload)
