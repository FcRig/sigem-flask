import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import jwt
from datetime import datetime, timedelta, timezone



driver = Chrome();


url = 'https://sei.prf.gov.br/sei/'
request = requests.get(url)


driver.get(url)
driver.maximize_window()
time.sleep(1)
email = driver.find_element(By.ID, 'txtUsuario')

if email:
    print('a')


email.send_keys('leonardo.andrighetto.estagio')

senha = driver.find_element(By.ID, 'pwdSenha')
senha.send_keys('Leo-2537?',Keys.ENTER)

pesquisar = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#txtPesquisaRapida.form-control")))


pesquisar.send_keys("08660.014539/2023-89", Keys.ENTER)


pa = WebDriverWait(driver, 3).until(
    EC.frame_to_be_available_and_switch_to_it((By.ID, 'ifrVisualizacao'))
)


incluir = WebDriverWait(driver,3).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR,"img[title='Incluir Documento']"))
)

incluir.click()

txtFiltro = email = driver.find_element(By.CSS_SELECTOR, '#txtFiltro')

txtFiltro.send_keys("Despacho")
time.sleep(1)
txtFiltro.send_keys(Keys.TAB)
time.sleep(1)


driver.send_keys(Keys.ENTER)





time.sleep(400)
# soup = BeautifulSoup(request.content,'html.parser')

# pesquisar = driver.get(url).find_element(By.CSS_SELECTOR, '.txtPesquisaRapida')
# espera = WebDriverWait(pesquisar,5)
# espera.until(EC.element_to_be_clickable)
# pesquisar.clik()



# def buscar_dados(url):
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, "html.parser")
#     # Exemplo: extrair título da página
#     return {"titulo": soup.title.string if soup.title else None}


# def get_link_by_action(self, html: str, action: str) -> str | None:
#         soup = BeautifulSoup(html, "html.parser")
#         for link in soup.find_all("a", href=True):
#             if link.get("link") == action:
#                 return urljoin(self.BASE_URL, link["href"].replace("&amp;", "&"))
#         return None