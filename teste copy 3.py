import requests
from bs4 import BeautifulSoup
import time

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

# 1️⃣ LOGIN PARA CAPTURAR COOKIES
login_url = "http://multa.prf.gov.br/multa2/"
payload_login = {"username": "68109911234", "j_username": "68109911234", "j_password": "Cacoal1981j@"}
response_login = session.post(login_url, data=payload_login, headers=headers)
response_login.raise_for_status()
print("✅ Login efetuado com sucesso.")

# 2️⃣ CAPTURA CID VIA REDIRECIONAMENTO
inicio_url = "https://multa.prf.gov.br/multass2/pages/historico/inicio.seam"
response_cid = session.get(inicio_url, headers=headers, allow_redirects=False)
location = response_cid.headers.get("Location", "")
cid = location.split("cid=")[-1] if "cid=" in location else None
if not cid:
    raise Exception("❌ Não foi possível capturar o CID automaticamente.")
print(f"✅ CID capturado: {cid}")

# 3️⃣ CAPTURA VIEWSTATE ANTES DO POST
list_url = f"https://multa.prf.gov.br/multass2/pages/historico/historicoMultaList.seam?cid={cid}"
headers["Referer"] = f"https://multa.prf.gov.br/multa2/menu.jsp"
response_list = session.get(list_url, headers=headers)
soup = BeautifulSoup(response_list.text, "html.parser")
viewstate_input = soup.find("input", {"name": "javax.faces.ViewState"})
if not viewstate_input:
    raise Exception("❌ ViewState não encontrado antes do POST.")
viewstate_value = viewstate_input.get("value")
print("✅ ViewState capturado:", viewstate_value)

# 4️⃣ POST PARA PESQUISA DO AI
numero_ai = "T 57.365.709-2"  # Troque pelo número desejado
post_url = f"https://multa.prf.gov.br/multass2/pages/historico/historicoMultaList.seam?cid={cid}"
headers["Referer"] = list_url
payload_post = {
    "consultaHistoricoMulta": "consultaHistoricoMulta",
    "consultaHistoricoMulta:j_id7:j_id11:j_id17": "",
    "consultaHistoricoMulta:j_id7:j_id21:j_id27": numero_ai,
    "consultaHistoricoMulta:j_id7:j_id31:j_id37": "",
    "consultaHistoricoMulta:j_id7:botoesNumeroLoteDecoration:j_id43": "Pesquisar",
    "javax.faces.ViewState": viewstate_value
}
response_post = session.post(post_url, headers=headers, data=payload_post, allow_redirects=False)
new_location = response_post.headers.get("Location", "")
if "cid=" in new_location:
    cid = new_location.split("cid=")[-1]
    print(f"✅ Novo CID capturado após POST: {cid}")
else:
    print("⚠️ Nenhum novo CID retornado após POST, usando o anterior.")

# 5️⃣ GET NO DETALHE DA MULTA
detalhe_url = f"https://multa.prf.gov.br/multass2/pages/historico/historicoMultaDetalhe.seam?cid={cid}"
headers["Referer"] = post_url
response_detalhe = session.get(detalhe_url, headers=headers)
with open("detalhe_multa.html", "w", encoding="utf-8") as f:
    f.write(response_detalhe.text)
print("✅ HTML de detalhe salvo como detalhe_multa.html para análise.")
