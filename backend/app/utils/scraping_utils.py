import requests
from bs4 import BeautifulSoup

def buscar_dados(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    # Exemplo: extrair título da página
    return {'titulo': soup.title.string if soup.title else None}

def carregar_cookies(driver, cookies_json, base_url):
    import json
    cookies = json.loads(cookies_json)
    driver.get(base_url)  # precisa abrir o domínio primeiro

    for cookie in cookies:
        cookie.pop('sameSite', None)  # remove campos problemáticos
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"[cookie erro] {cookie['name']}: {e}")

