import requests

# === Passo 1: POST para https://multa.prf.gov.br/multa2/ para obter cookies ===
session = requests.Session()

# URL inicial para obter cookies
url_login = "https://multa.prf.gov.br/multa2/"

# Fazemos um GET inicial para pegar os cookies (pois /multa2/ geralmente não aceita POST vazio)
response_login = session.get(url_login, allow_redirects=True)
print(f"Status do login (GET inicial): {response_login.status_code}")
print(f"Cookies após login: {session.cookies.get_dict()}")

# === Passo 2: POST para https://multa.prf.gov.br/multass2/pages/historico/historicoMultaList.seam ===

url_pesquisa = "https://multa.prf.gov.br/multass2/pages/historico/historicoMultaList.seam"

# Payload capturado
payload = (
    "consultaHistoricoMulta=consultaHistoricoMulta&"
    "consultaHistoricoMulta:j_id7:j_id11:j_id17=&"
    "consultaHistoricoMulta:j_id7:j_id21:j_id27=T 48.574.296-9&"
    "consultaHistoricoMulta:j_id7:j_id31:j_id37=&"
    "consultaHistoricoMulta:j_id7:botoesNumeroLoteDecoration:j_id43=Pesquisar&"
    "javax.faces.ViewState=j_id15"
)

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# Realiza o POST com o payload, mantendo os cookies da sessão
response_pesquisa = session.post(url_pesquisa, headers=headers, data=payload, allow_redirects=True)

print(f"Status da pesquisa: {response_pesquisa.status_code}")

# Salva o HTML retornado para análise
with open("resultado_pesquisa.html", "w", encoding="utf-8") as f:
    f.write(response_pesquisa.text)

print("Arquivo 'resultado_pesquisa.html' salvo para análise do retorno.")
