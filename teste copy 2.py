import requests
from bs4 import BeautifulSoup

session = requests.Session()

# Cabeçalhos consistentes
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://multa.prf.gov.br/multa2/"
}

# 1️⃣ LOGIN AUTOMÁTICO PARA OBTER COOKIES ATUALIZADOS
login_url = "http://multa.prf.gov.br/multa2/"
payload_login = {"username": "68109911234", "j_username": "68109911234", "j_password": "Cacoal1981j@"}
response_login = session.post(login_url, data=payload_login, headers=headers, allow_redirects=False)
response_login.raise_for_status()
print("✅ Login efetuado com sucesso.")

# 2️⃣ GET PARA CAPTURAR O CID DINAMICAMENTE APÓS LOGIN
inicio_url = "https://multa.prf.gov.br/multass2/pages/historico/inicio.seam"
response_cid = session.get(inicio_url, headers=headers, allow_redirects=False)
location = response_cid.headers.get("Location", "")
cid = location.split("cid=")[-1] if "cid=" in location else None
if not cid:
    raise Exception("❌ Não foi possível capturar o CID dinamicamente.")
print(f"✅ CID capturado: {cid}")

# 3️⃣ GET NA URL DE DETALHE COM CID OBTIDO
headers["Referer"] = f"https://multa.prf.gov.br/multass2/pages/historico/historicoMultaList.seam?cid={cid}"
detalhe_url = f"https://multa.prf.gov.br/multass2/pages/historico/historicoMultaDetalhe.seam?cid={cid}"
response = session.get(detalhe_url, headers=headers, allow_redirects=False)
print("Status:", response.status_code)

if response.status_code == 302:
    print("🔄 Redirecionamento detectado para:", response.headers.get("Location"))
else:
    soup = BeautifulSoup(response.text, "html.parser")
    viewstate_input = soup.find("input", {"name": "javax.faces.ViewState"})
    if viewstate_input:
        print("✅ ViewState capturado:", viewstate_input.get("value"))
    else:
        print("❌ ViewState não encontrado. Salve a página para depuração.")
    with open("pagina_detalhe_debug.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("🔍 HTML salvo em pagina_detalhe_debug.html para inspeção.")
