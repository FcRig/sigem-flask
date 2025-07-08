import requests
from bs4 import BeautifulSoup

session = requests.Session()

# Cabeçalhos consistentes
headers ={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "multa.prf.gov.br",
    "Origin": "https://multa.prf.gov.br",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}


# 1️⃣ GET
login_url = "https://multa.prf.gov.br/multa2/"
# headers["Referer"] = "https://multa.prf.gov.br/multa2/"
response_login = session.get(login_url)
print("✅ Primeira requisição.")

# 1️⃣ LOGIN AUTOMÁTICO COM REDIRECIONAMENTO
login_url = "https://multa.prf.gov.br/multa2/j_security_check"
payload_login = {"username": "68109911234", "j_username": "68109911234", "j_password": "Cacoal1981j@"}
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Referer"] = "https://multa.prf.gov.br/multa2/"
response_login = session.post(login_url, data=payload_login, headers=headers, allow_redirects=False)
print("✅ Login efetuado com sucesso.")

# 2️⃣ GET PARA CAPTURAR O CID SEM REDIRECIONAMENTO
historico_url = "https://multa.prf.gov.br/multass2/pages/historico/inicio.seam"
response_get = session.get(historico_url, headers=headers, allow_redirects=False)
location = response_get.headers.get('Location', '')
cid = location.split("cid=")[-1] if "cid=" in location else None
if not cid:
    raise Exception("❌ Não foi possível extrair o CID automaticamente.")
print(f"✅ CID capturado: {cid}")

# 3️⃣ GET COM CID PARA CAPTURAR VIEWSTATE
list_url = f"https://multa.prf.gov.br/multass2/pages/historico/historicoMultaList.seam?cid={cid}"
headers["Referer"] = "https://multa.prf.gov.br/multa2/menu.jsp"
response_cid = session.get(list_url, headers=headers, allow_redirects=False)
print(response_cid.status_code)
print(response_cid.text)
# soup = BeautifulSoup(response_cid.text, "html.parser")


# # viewstate_input = soup.find("input", {"name": "javax.faces.ViewState"})
# # if viewstate_input:
# #     viewstate_value = viewstate_input.get("value")
# #     print("✅ ViewState capturado:", viewstate_value)
# # else:
# #     print("❌ ViewState não encontrado. Verifique cookies e sessão.")

# # # Opcional: salvar HTML para análise
# # temp_file = "pagina_debug.html"
# # with open(temp_file, "w", encoding="utf-8") as f:
# #     f.write(response_cid.text)
# # print(f"🔍 HTML salvo em {temp_file} para inspeção.")
