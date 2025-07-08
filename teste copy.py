import requests
from bs4 import BeautifulSoup

session = requests.Session()

# Cabeçalhos consistentes
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://multa.prf.gov.br/multass2/pages/historico/historicoMultaList.seam"
}

# 1️⃣ LOGIN AUTOMÁTICO COM REDIRECIONAMENTO
login_url = "http://multa.prf.gov.br/multa2/"
payload_login = {"username": "68109911234", "j_username": "68109911234", "j_password": "XXXXX"}
response_login = session.post(login_url, data=payload_login, headers=headers, allow_redirects=False)
response_login.raise_for_status()
print("✅ Login efetuado com sucesso.")

# 2️⃣ GET PARA CAPTURAR O CID SEM REDIRECIONAMENTO
historico_url = "https://multa.prf.gov.br/multass2/pages/historico/inicio.seam"
response_get = session.get(historico_url, headers=headers, allow_redirects=False)
print(response_get.status_code, response_get.headers)
location = response_get.headers.get('Location', '')
cid = location.split("cid=")[-1] if "cid=" in location else None
if not cid:
    raise Exception("❌ Não foi possível extrair o CID automaticamente.")
print(f"✅ CID capturado: {cid}")

# 3️⃣ GET COM CID PARA CAPTURAR VIEWSTATE
list_url = f"https://multa.prf.gov.br/multass2/pages/historico/historicoMultaList.seam?cid={cid}"
headers["Referer"] = list_url
response_cid = session.get(list_url, headers=headers, allow_redirects=False)
print(response_cid.status_code)

soup = BeautifulSoup(response_cid.text, "html.parser")
viewstate_input = soup.find("input", {"name": "javax.faces.ViewState"})
if viewstate_input:
    viewstate_value = viewstate_input.get("value")
    print("✅ ViewState capturado:", viewstate_value)
else:
    print("❌ ViewState não encontrado. Verifique cookies e sessão.")

# Opcional: salvar HTML para análise
temp_file = "pagina_debug.html"
with open(temp_file, "w", encoding="utf-8") as f:
    f.write(response_cid.text)
print(f"🔍 HTML salvo em {temp_file} para inspeção.")
