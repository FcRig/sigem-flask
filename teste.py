import requests
from bs4 import BeautifulSoup

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://multa.prf.gov.br/multass2/pages/historico/historicoMultaList.seam"
}

# 1️⃣ LOGIN COM REDIRECIONAMENTO AUTOMÁTICO
login_url = "https://multa.prf.gov.br/multa2/j_security_check"
payload_login = {"username": "68109911234", "j_username": "68109911234", "j_password": "xxxxxxx"}
session.post(login_url, data=payload_login, headers=headers, allow_redirects=True)
print("✅ Login efetuado com sucesso.")

# 2️⃣ DESABILITA REDIRECIONAMENTO PARA CAPTURAR O CID
historico_url = "https://multa.prf.gov.br/multass2/pages/historico/inicio.seam"
response_get = session.get(historico_url, headers=headers, allow_redirects=False)
location = response_get.headers.get('Location', '')
cid = location.split("cid=")[-1] if "cid=" in location else None
if not cid:
    raise Exception("❌ Não foi possível extrair o CID automaticamente.")
print(f"✅ CID encontrado: {cid}")

# 3️⃣ SEGUNDO GET PARA CAPTURAR VIEWSTATE
historico_list_url = "https://multa.prf.gov.br/multass2/pages/historico/historicoMultaList.seam"
response_get_cid = session.get(f"{historico_list_url}?cid={cid}", headers=headers, allow_redirects=False)
soup = BeautifulSoup(response_get_cid.text, "html.parser")
viewstate_input = soup.find("input", {"name": "javax.faces.ViewState"})
if not viewstate_input:
    raise Exception("❌ Não foi possível localizar javax.faces.ViewState no HTML.")
viewstate_value = viewstate_input.get("value")
print(f"✅ ViewState capturado: {viewstate_value}")

# 4️⃣ MONTA O PAYLOAD PARA CONSULTAR AI
numero_ai = "T 57.365.709-2"  # Troque pelo número do AI desejado
payload_post = {
    "consultaHistoricoMulta": "consultaHistoricoMulta",
    "consultaHistoricoMulta:j_id7:j_id11:j_id17": "",
    "consultaHistoricoMulta:j_id7:j_id21:j_id27": numero_ai,
    "consultaHistoricoMulta:j_id7:j_id31:j_id37": "",
    "consultaHistoricoMulta:j_id7:botoesNumeroLoteDecoration:j_id43": "Pesquisar",
    "javax.faces.ViewState": viewstate_value
}

# 5️⃣ ENVIA O POST FINAL PARA CONSULTA
response_post = session.post(f"{historico_list_url}?cid={cid}", data=payload_post, headers=headers, allow_redirects=False)
response_post.raise_for_status()

# 6️⃣ SALVA O HTML RETORNADO PARA ANÁLISE
with open("resultado_consulta.html", "w", encoding="utf-8") as f:
    f.write(response_post.text)

print("✅ Consulta realizada com sucesso e HTML salvo como resultado_consulta.html")
