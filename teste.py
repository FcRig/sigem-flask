import requests
from bs4 import BeautifulSoup
import re

usuario = "flavio.rigotte"
senha = "xxxxxx"
codigo_acesso = "445679"
nup_processo = "08660.014539/2023-89"

sessao = requests.Session()

# Login passo 1
url_login = "https://sei.prf.gov.br/sip/login.php?sigla_sistema=SEI&sigla_orgao_sistema=PRF"
data_login = {"txtUsuario": usuario, "pwdSenha": senha, "selOrgao": "0", "Acessar": "", "hdnAcao": "2"}
sessao.post(url_login, data=data_login)

# Login passo 2
url_token = "https://sei.prf.gov.br/sip/login.php?sigla_orgao_sistema=PRF&sigla_sistema=SEI"
data_token = {"txtCodigoAcesso": codigo_acesso, "hdnAcao": "3"}
sessao.post(url_token, data=data_token)

# Função para extrair infra_hash do HTML recebido
def extrair_infra_hash(html):
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find(id="lnkInfraUnidade")
    if link and link.has_attr('onclick'):
        match = re.search(r'infra_hash=([a-f0-9]+)', link['onclick'])
        if match:
            return match.group(1)
    return None

# Obtendo o infra_hash atual
tela_inicial = sessao.get("https://sei.prf.gov.br/sei/controlador.php")
infra_hash = extrair_infra_hash(tela_inicial.text)
print(f"infra_hash extraído: {infra_hash}")

# Pesquisa do processo usando protocolo_pesquisa_rapida
url_consulta = "https://sei.prf.gov.br/sei/controlador.php"
params_consulta = {
    "acao": "protocolo_pesquisa_rapida",
    "infra_sistema": "100000100",
    "infra_unidade_atual": "110000471",
    "infra_hash": infra_hash
}
data_consulta = {"txtPesquisaRapida": nup_processo}

resp_consulta = sessao.post(url_consulta, params=params_consulta, data=data_consulta, allow_redirects=False)

if 'Location' in resp_consulta.headers:
    print(f"Redirect para: {resp_consulta.headers['Location']}")
else:
    print("Não houve redirecionamento, verificar o fluxo e o hash.")
