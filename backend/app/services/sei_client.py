import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
import unicodedata
from datetime import datetime

import time

import undetected_chromedriver as uc

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

        return self.home_html


    def _normalize(self, text: str) -> str:
        return (
            unicodedata.normalize("NFKD", text or "")
            .encode("ASCII", "ignore")
            .decode("ASCII")
            .strip()
            .lower()
        )

    def extract_infra_hash(self, html: str) -> str | None:
        m = re.search(r"infra_hash=([a-f0-9]{20,})", html, re.I)
        return m.group(1) if m else None
    
    def get_link_by_action(self, html: str, action: str) -> str | None:
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all("a", href=True):
            if link.get("link") == action:
                return urljoin(self.BASE_URL, link["href"].replace("&amp;", "&"))
        return None

    def get_current_unit(self) -> str:
        """Return the textual name of the currently selected unit."""
        soup = BeautifulSoup(self.home_html or "", "html.parser")
        link = soup.select_one("#lnkInfraUnidade")
        return link.get_text(strip=True) if link else ""

    def _fetch_units_page(self) -> tuple[list[dict[str, str]], dict[str, str], str]:
        """Fetch the units selection page and return units list, inputs and form action."""

        soup = BeautifulSoup(self.home_html or "", "html.parser")
        link = soup.select_one("#lnkInfraUnidade")    

        if not link:
            return [], {}, ""

        href = link.get("href", "")

        # Se o href for apenas "#", extrair do onclick
        if href == "#" or not href:
            onclick = link.get("onclick", "")
            import re
            match = re.search(r"window\.location\.href='([^']+)'", onclick)
            if match:
                href = match.group(1).replace("&amp;", "&")

        if not href:
            return [], {}, ""

        url = urljoin(self.BASE_URL, href)

        resp = self.session.get(url)
        resp.encoding = "iso-8859-1"
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")              

        table = soup.select_one("#divInfraAreaTabela table")        
        units: list[dict[str, str]] = []
        if table:
            for tr in table.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) >= 2:
                    units.append(
                        {
                            "id": tds[0].get_text(strip=True),
                            "text": tds[1].get_text(strip=True),
                        }
                    )

        form = soup.find("form")
        action = urljoin(self.BASE_URL, form.get("action", "")) if form else ""
        inputs = {
            inp.get("name"): inp.get("value", "")
            for inp in (form.find_all("input") if form else [])
            if inp.get("name")
        }
        return units, inputs, action

    def list_units(self) -> list[dict[str, str]]:
        """Return a list of available units as dicts with id and text."""
        units, _, _ = self._fetch_units_page()
        return units

    def change_unit(self, unit_id: str) -> None:
        """Change current unit to the provided id."""
        units, inputs, action = self._fetch_units_page()
        if not action:
            raise RuntimeError("Unit form not found")
        inputs.update(
            {
                "chkInfraItem": unit_id,
                "hdnInfraItensSelecionados": unit_id,
                "selInfraUnidades": unit_id,
            }
        )
        resp = self.session.post(action, data=inputs)
        resp.raise_for_status()
        self.home_html = resp.text

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
        if not self.home_html:
            raise RuntimeError("Not logged in")

        url = self.get_link_by_action(self.home_html, "procedimento_escolher_tipo")
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
            onclick = link.get("onclick", "")

            m = re.search(r"escolher\((\d+)\)", onclick)
            tipo_id_real = ''
            if m:
                tipo_id_real = m.group(1)
            else:
                tipo_id_real = None

            # print(f"TIPO:::: {tipo_id_real}")
           
            result.append({"id": tipo_id_real, "text": text_val})
        return result

    def create_process(self, type_id: str, type_name: str, description: str) -> requests.Response:

        print("\n========== CREATE PROCESS START ==========")

        if not self.home_html:
            raise RuntimeError("Not logged in")

        print("\n[1] Buscando link de escolha de tipo...")

        action_url = self.get_link_by_action(
            self.home_html, "procedimento_escolher_tipo"
        )

        print("action_url:", action_url)

        if not action_url:
            raise RuntimeError("Action link not found")

        print("\n[2] GET página de tipos...")
        resp = self.session.get(action_url)
        print("GET status:", resp.status_code)
        print("GET url final:", resp.url)

        resp.encoding = "iso-8859-1"

        infra_hash_1 = self.extract_infra_hash(resp.text)
        print("infra_hash extraído do GET tipos:", infra_hash_1)

        link = self.get_link_by_text(resp.text, type_name)
        print("link extraído pelo texto:", link)

        if not link:
            raise RuntimeError("Process type not found")

        print("\n[3] POST procedimento_escolher_tipo...")

        POST = self.session.post(
            "https://sei.prf.gov.br/sei/controlador.php",
            data={
                "acao": "procedimento_escolher_tipo",
                "acao_origem": "procedimento_escolher_tipo",
                "infra_sistema": "100000100",
                "infra_unidade_atual": "110000471",
                "infra_hash": infra_hash_1,
                "id_tipo_procedimento": type_id
            }
        )

        print("POST status:", POST.status_code)
        print("POST url final:", POST.url)
        print("POST history:", POST.history)

        infra_hash_2 = self.extract_infra_hash(POST.text)
        print("infra_hash extraído do POST:", infra_hash_2)

        print("\n[4] GET procedimento_gerar...")

        GET = self.session.get(
            "https://sei.prf.gov.br/sei/controlador.php",
            params={
                "acao": "procedimento_gerar",
                "acao_origem": "procedimento_escolher_tipo",
                "acao_retorno": "procedimento_escolher_tipo",
                "id_tipo_procedimento": type_id,
                "infra_sistema": "100000100",
                "infra_unidade_atual": "110000471",
                "infra_hash": infra_hash_2 or infra_hash_1
            }
        )

        print("GET gerar status:", GET.status_code)
        print("GET gerar url final:", GET.url)
        print("GET gerar history:", GET.history)

        GET.encoding = "iso-8859-1"

        print("\n[5] Procurando formulário de cadastro...")

        soup = BeautifulSoup(GET.text, "html.parser")
        form = soup.select_one("#frmProcedimentoCadastro")

        print("Form encontrado?", bool(form))

        if not form:
            print("\n===== HTML INTEIRO DA RESPOSTA =====\n")
            print(GET.text[:3000])  # evita travar o terminal
            raise RuntimeError("Form not found")

        action = form.get("action")
        print("Form action:", action)

        if not action:
            raise RuntimeError("Form action not found")

        post_url = urljoin(self.BASE_URL, action)
        print("Post URL final:", post_url)

        assunto_default = (
            "727"
            if self._normalize(type_name)
            == self._normalize("Multas: Auto de Infração - Cancelamento")
            else "209"
        )

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
            "hdnAssuntos": assunto_default,
            "hdnSinIndividual": "N",
            "hdnDtaGeracao": datetime.now().strftime("%d/%m/%Y"),
        }

        print("\n[6] Payload final:", payload)

        print("\n[7] POST final de criação...")

        final_resp = self.session.post(post_url, data=payload)

        print("POST final status:", final_resp.status_code)
        print("POST final url:", final_resp.url)
        print("POST final history:", final_resp.history)

        print("\n========== CREATE PROCESS END ==========")

        return final_resp
