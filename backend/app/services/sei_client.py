import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
import unicodedata
from datetime import datetime

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

import undetected_chromedriver as uc

class SEIClient:
    """Client to handle authentication with the SEI system."""

    BASE_URL = "https://sei.prf.gov.br/sei/"
    LOGIN_URL = (
        "https://sei.prf.gov.br/sip/login.php?sigla_sistema=SEI&sigla_orgao_sistema=PRF"
    )

    CHROME = None
    COOKIES = None

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

<<<<<<< Updated upstream
        sei_cookies_jar = self.session.cookies

        chrome = Chrome()
        
        #options = Options()
        #options.add-argument("--headless")
        #chrome = chrome.Options(options=options)

        chrome.get("https://sei.seusistema.gov.br")

        print("\nInjetando cookies de sessão do requests para o Selenium...")

        for cookie_obj in sei_cookies_jar:
            
            # Converte o objeto cookie do requests para o dicionário esperado pelo Selenium
            selenium_cookie = {
                'name': cookie_obj.name,
                'value': cookie_obj.value,
                'domain': cookie_obj.domain,
                'path': cookie_obj.path,
                'secure': cookie_obj.secure,
                # O campo 'expires' deve ser um inteiro (timestamp), se existir
                'expires': int(cookie_obj.expires) if cookie_obj.expires else None
            }

        try:
            chrome.add_cookie(selenium_cookie)
        except Exception as e:

            # Pode haver erro ao injetar cookies sem domínio/path válidos
            print(f"Aviso: Não foi possível injetar o cookie {cookie_obj.name}: {e}")
        print(f"\n\n\n{self.home_html}\n\n\n")

        chrome.get(self.LOGIN_URL.split('?')[0])

        if "login" not in chrome.current_url.lower():
            print("✅ Sessão do SEI injetada e restaurada com sucesso no Selenium!")
        else:
            print("❌ Injeção falhou. Sessão não restaurada.")

        #options = Options()
        #options.add-argument("--headless")
        #chrome = chrome.Options(options=options)

        # chrome.get(SEIClient.LOGIN_URL)
        # print(f"\n\n\nUSUARIO: {usuario}\n\n\n")
        # WebDriverWait(chrome,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#txtUsuario'))).send_keys(usuario)
        # WebDriverWait(chrome,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#pwdSenha'))).send_keys(senha)
        # WebDriverWait(chrome,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sbmAcessar'))).click()
        # WebDriverWait(chrome,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#txtCodigoAcesso'))).send_keys(token)
        # WebDriverWait(chrome,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sbmValidar'))).click()

        SEIClient.CHROME = chrome
        SEIClient.COOKIES = sei_cookies_jar
=======

        print("\n✅ COOKIES DA SESSÃO:")
        for c in self.session.cookies:
            print(c.name, "=", c.value)

>>>>>>> Stashed changes
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

        if not self.home_html:
            raise RuntimeError("Not logged in")

        # Escolhendo o tipo de processo
        action_url = self.get_link_by_action(
            self.home_html, "procedimento_escolher_tipo"
        )
        print(f"\n\nself.home_html:::\n\n {self.home_html}")
        if not action_url:
            raise RuntimeError("Action link not found")
        
        print(f"\n\naction_url:::\n\n {action_url}")

        resp = self.session.get(action_url)
        resp.encoding = "iso-8859-1"
        link = self.get_link_by_text(resp.text, type_name)
        if not link:
            raise RuntimeError("Process type not found")

        # Acessando a página de cadastro do processo
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
        print(f"Post URL: {post_url}")

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

        print(payload)

        return self.session.post(post_url, data=payload)

    def procurarProcesso(self, processo):

        # garante que a session foi restaurada antes de chamar (o controller deve chamar restore_session_from_user)
        # aplica/inicia selenium e cookies

        chrome = SEIClient.CHROME
        cookies = SEIClient.COOKIES

        chrome.get("https://sei.prf.gov.br")

        for cookie in cookies:

            cookie.pop("sameSite", None)
            cookie.pop("expiry", None)
            chrome.add_cookie(cookie)

        if not self.home_html:
            raise RuntimeError("Not logged in")

        chrome = self.selenium_driver
        url = self.selenium_url_base or "https://sei.prf.gov.br/sei/controlador.php?acao=principal"

        try:
            chrome.switch_to.default_content()
            chrome.maximize_window()
            chrome.get(url)
        except Exception:
            return {"msg": "SESSAO_SELENIUM_PERDIDA"}

        # se caiu no login, aborta imediatamente
        cur = chrome.current_url.lower() if chrome.current_url else ""
        if "login" in cur or "sip/login.php" in cur:
            return {"msg": "SESSAO_SELENIUM_PERDIDA"}

        try:
            barraPesquisa = WebDriverWait(chrome, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#txtPesquisaRapida")))

            barraPesquisa.clear()
            barraPesquisa.send_keys(processo)

            bntPesquisar = WebDriverWait(chrome, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#spnInfraUnidade")))

            bntPesquisar.click()

            WebDriverWait(chrome, 5).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrConteudoVisualizacao")))

            novoDoc = WebDriverWait(chrome, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//img[@title="Incluir Documento"]')))

            if novoDoc:
                return {"msg": "PROCESSO_ENCONTRADO"}

        except TimeoutException:
            pass