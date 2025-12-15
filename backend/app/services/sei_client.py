from typing import Any, Dict
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

    
    def encode_payload_sei(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        encoded = {}

        for key, value in payload.items():
            if value is None:
                encoded[key] = value
                continue

            # só converte strings "humanas"
            if isinstance(value, str):
                try:
                    encoded[key] = value.encode("iso-8859-1")
                except UnicodeEncodeError:
                    # se não der (emoji, etc), manda como está
                    encoded[key] = value
            else:
                encoded[key] = value

        return encoded


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

    def create_process(self, type_name: str, description: str) -> requests.Response:

        if not self.home_html:
            raise RuntimeError("Not logged in")

        soup = BeautifulSoup(self.home_html, "html.parser")

        url = ""

        for link in soup.find_all("a", href = True):
            if link.get("link") == "procedimento_escolher_tipo":
                url = urljoin(self.BASE_URL, link["href"])

        resp = self.session.get(url)

        home_html = resp.text

        soup = BeautifulSoup(home_html, "html.parser")

        # PRECISO CAPTURAR O HASH DENTRO DO FORM ONDE ESTÁ A TABELA DO FORMULÁRIO.

        form = soup.find("form", id='frmProcedimentoEscolherTipo') # puxa a form

        action = form.get('action') #action da form

        action_url = urljoin(self.BASE_URL, action) # cria a url da ACTION

        parsed = urlparse(action) # SEPARA A URL OBTIDA DA ACTION em partes.

        params = parse_qs(parsed.query) # CAPTURA somente a query da url e a insere
        #em um dicionário separando cada parãmetro da query.

        infra_hash = params["infra_hash"][0] # isola o infrahash do dicionario
                                        # no índice 0, pois cada valor do dicionário é uma lista.
                                                                        
        table = soup.select_one("#tblTipoProcedimento")

        inputs = table.find("input", title = type_name)

        id = inputs.get("value")

        payload = {'acao':'procedimento_escolher_tipo',
                'acao_origem':'procedimento_escolher_tipo',
                'infra_sistema':'100000100',
                'infra_unidade_atual':'110000471',
                'infra_hash': infra_hash,
                'hdnIdTipoProcedimento': id
                }
        
        resp = self.session.post(action_url, data=payload)

        # 3. Extrair o novo infra_hash do redirect
        parsed = urlparse(resp.url)
        params = parse_qs(parsed.query)
        novo_hash = params["infra_hash"][0]

        # 4. Agora essa página já é o formulário do processo NOVO
        soup = BeautifulSoup(resp.text, "html.parser")

        action = soup.find("form",id='frmProcedimentoCadastro').get("action")
        action_url = urljoin(self.BASE_URL, action)


        select = soup.find('select', id ='selAssuntos')

        option = select.find("option")

        hdnAssuntos = option.get("value")

        payload = {'infra_hash': novo_hash,
                'hdnInfraTipoPagina':'1',
                'rdoProtocolo':'A',
                'selTipoProcedimento':id,
                'txtDescricao' : description,           
                'selTipoPrioridade':'null',
                'selGrauSigilo':'null',
                'rdoNivelAcesso':'0',
                'selHipoteseLegal':'null',
                'hdnFlagProcedimentoCadastro':'2',
                'hdnIdTipoProcedimento':id,
                'hdnAssuntos': hdnAssuntos,
                'hdnSinIndividual':'N',
                'hdnDtaGeracao': datetime.now().strftime("%d/%m/%Y")
                }


        payload = self.encode_payload_sei(payload=payload)

        return self.session.post(action_url, data=payload)