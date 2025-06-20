from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from flask import current_app

class AutoPRFClient:
    def __init__(self, jwt_token: str | None = None):
        chromedriver_path = current_app.config.get('CHROMEDRIVER_PATH')
        if not chromedriver_path:
            raise RuntimeError("CHROMEDRIVER_PATH não está definido na configuração.")
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.jwt_token = jwt_token or ''

    def login(self, cpf: str, password: str, token: str) -> str:
        driver = self.driver
        driver.get('https://auto.prf.gov.br/#/login')

        # Preenche login
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'username'))
        ).send_keys(cpf)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.NAME, 'token').send_keys(token)

        # Tenta remover banner de cookies
        try:
            cookie_span = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, 'cookieconsent:desc'))
            )
            driver.execute_script("arguments[0].remove();", cookie_span)
        except:
            pass  # Ignora se não aparecer

        # Usa JavaScript para clicar no botão, evitando bloqueios por sobreposição
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        driver.execute_script("arguments[0].click();", login_button)

        # Aguarda redirecionamento após login (ajuste conforme comportamento da aplicação)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        # Tenta obter JWT do armazenamento local ou cookies
        jwt_token = driver.execute_script(
            "return window.localStorage.getItem('jwt') || "
            "window.localStorage.getItem('token') || "
            "window.sessionStorage.getItem('jwt') || "
            "window.sessionStorage.getItem('token');"
        )

        if not jwt_token:
            for c in driver.get_cookies():
                name = c.get('name', '').lower()
                if 'jwt' in name or 'token' in name:
                    jwt_token = c.get('value')
                    break

        driver.quit()
        return jwt_token or ''
    
    def pesquisa_auto_infracao(self, auto_infracao: str) -> None:
        if self.jwt_token:
            # Exemplo de uso do JWT para autenticação em futuras requisições
            self.driver.execute_cdp_cmd(
                "Network.setExtraHTTPHeaders",
                {"headers": {"Authorization": f"Bearer {self.jwt_token}"}},
            )
        self.driver.find_element(By.CSS_SELECTOR, 'body > app-dashboard > div > app-sidebar > app-sidebar-nav > app-sidebar-nav-items > app-sidebar-nav-dropdown:nth-child(2) > a').click()
