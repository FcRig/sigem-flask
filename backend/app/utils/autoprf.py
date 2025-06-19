from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from flask import current_app
from .scraping_utils import carregar_cookies

class AutoPRFClient:
    def __init__(self):
        chromedriver_path = current_app.config.get('CHROMEDRIVER_PATH')
        if not chromedriver_path:
            raise RuntimeError("CHROMEDRIVER_PATH não está definido na configuração.")
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=options)       
        self.cookies_json = ''

    def login(self, cpf: str, password: str, token: str) -> list[dict]:
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

        # Coleta cookies 
        cookies = driver.get_cookies()
        driver.quit()    
        return cookies
    
    def pesquisa_auto_infracao(self, auto_infracao: str) -> None:
        if self.cookies_json:
            carregar_cookies(self.driver, self.cookies_json, "https://auto.prf.gov.br")
        self.driver.find_element(By.CSS_SELECTOR, 'body > app-dashboard > div > app-sidebar > app-sidebar-nav > app-sidebar-nav-items > app-sidebar-nav-dropdown:nth-child(2) > a').click()
        
        