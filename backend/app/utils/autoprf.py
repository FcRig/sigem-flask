from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from flask import current_app
from time import sleep

class AutoPRFClient:
    def __init__(self, jwt_token: str | None = None):
        chromedriver_path = current_app.config.get('CHROMEDRIVER_PATH')
        if not chromedriver_path:
            raise RuntimeError("CHROMEDRIVER_PATH não está definido na configuração.")
        options = Options()
        # options.add_argument('--headless')
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

        sleep(3)                  

        jwt_token = driver.execute_script("""
            try {
                const raw = localStorage.getItem('jwt_sessao');
                if (!raw) return '';
                const parsed = JSON.parse(raw);
                return parsed.token || '';
            } catch (e) {
                return '';
            }
        """)     

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
            self.driver.get("https://auto.prf.gov.br")

            import json
            token_json = json.dumps({"token": self.jwt_token})
            self.driver.execute_script(f"""
                localStorage.setItem('jwt_sessao', {json.dumps(token_json)});
            """)

            self.driver.get("https://auto.prf.gov.br/#/dashboard")

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "app-dashboard"))
        )            

        menu = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Autuação')]"))
        )
        menu.click()


