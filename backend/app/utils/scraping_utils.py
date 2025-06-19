import requests
from bs4 import BeautifulSoup
import json

def buscar_dados(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    # Exemplo: extrair título da página
    return {'titulo': soup.title.string if soup.title else None}

def carregar_cookies(driver, cookies_json, url):
    cookies = json.loads(cookies_json)
    driver.get(url)  # precisa carregar o domínio antes
    for cookie in cookies:
        # Remove campos inválidos se necessário
        cookie.pop('sameSite', None)
        driver.add_cookie(cookie)
