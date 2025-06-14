import requests
from bs4 import BeautifulSoup

def buscar_dados(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    # Exemplo: extrair título da página
    return {'titulo': soup.title.string if soup.title else None}
