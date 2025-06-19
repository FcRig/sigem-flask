from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class AutoPRFClient:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def login(self, cpf: str, password: str, token: str) -> str:
        driver = self.driver
        driver.get('https://sistemas.dprf.gov.br/autoprf/faces/autenticacao/login.jsf')

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'form_login:usuario'))
        ).send_keys(cpf)
        driver.find_element(By.ID, 'form_login:senha').send_keys(password)
        driver.find_element(By.ID, 'form_login:token').send_keys(token)
        driver.find_element(By.ID, 'form_login:entrar').click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        cookies = driver.get_cookies()
        session = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
        return session
