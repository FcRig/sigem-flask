# Integração e refatoração inspirada no projeto JS para SIGEM em Python
# Criação de classe ProcessoSEI para iniciar processo de forma reutilizável e em lote

import requests
from bs4 import BeautifulSoup
import urllib.parse
import unicodedata
import sys
from urllib.parse import urlparse, parse_qs, urlencode

class ProcessoSEI:
    def __init__(self, username, password, token):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
        self.username = username
        self.password = password
        self.token = token
        self.pagina_inicial = ''

    def login(self):
        BASE_URL = 'https://sei.prf.gov.br'
        LOGIN_URL = BASE_URL + '/sip/login.php?sigla_orgao_sistema=PRF&sigla_sistema=SEI'

        r = self.session.get(LOGIN_URL)

        payload = {
            'txtUsuario': self.username,
            'pwdSenha': self.password,
            'hdnAcao': '2',
            'selOrgao': '0',
            'Acessar': 'Acessar'
        }
        headers = {
            'Referer': LOGIN_URL,
            'Origin': 'https://sei.prf.gov.br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'Connection': 'keep-alive'
        }
        r = self.session.post(LOGIN_URL, data=payload, headers=headers, allow_redirects=True)

        soup = BeautifulSoup(r.text, 'html.parser')
        form = soup.find('form')
        if not form or 'txtCodigoAcesso' not in str(form):
            with open('falha_login_sem_formulario.html', 'w', encoding='utf-8') as f:
                f.write(r.text)
            raise Exception('Formulário de autenticação de dois fatores não encontrado.')

        action = form.get('action')
        token_url = urllib.parse.urljoin(BASE_URL + '/sip/', action)

        payload_token = {
            'txtCodigoAcesso': self.token,
            'hdnAcao': '3'
        }
        r = self.session.post(token_url, data=payload_token, headers={'Referer': token_url})

        if 'Controle de Processos' not in r.text and 'infra_hash' not in r.text:
            with open('falha_login.html', 'w', encoding='utf-8') as f:
                f.write(r.text)
            raise Exception('Falha no login. HTML salvo para análise.')
        else:
            print('[ok] Login realizado com sucesso.')
            self.pagina_inicial = r.text

    def pegar_link_por_acao(self, html, acao_desejada):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            if link.get('link') == acao_desejada:
                return 'https://sei.prf.gov.br/sei/' + link['href'].replace('&amp;', '&')
        return None

    def normalizar(self, texto):
        return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').strip().lower()

    def pegar_link_por_texto(self, html, texto_desejado):
        texto_desejado_norm = self.normalizar(texto_desejado)
        soup = BeautifulSoup(html, 'html.parser')
        for td in soup.find_all('td'):
            for link in td.find_all('a', href=True):
                texto_link = self.normalizar(link.text)
                print('Verificando:', texto_link.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
                if texto_link == texto_desejado_norm:
                    return 'https://sei.prf.gov.br/sei/' + link['href'].replace('&amp;', '&')
        with open('html_tipo_processo.html', 'w', encoding='utf-8') as f:
            f.write(html)
        raise Exception(f"Tipo de processo não encontrado: '{texto_desejado}'")

    def iniciar_processo(self, tipo_processo_texto, especificacao):
        self.login()
        url_iniciar = self.pegar_link_por_acao(self.pagina_inicial, 'procedimento_escolher_tipo')
        if not url_iniciar:
            raise Exception('Link para iniciar processo não encontrado')

        r = self.session.get(url_iniciar)
        r.encoding = 'iso-8859-1'
        url_tipo_processo = self.pegar_link_por_texto(r.text, tipo_processo_texto)
        if not url_tipo_processo:
            raise Exception('Tipo de processo não encontrado')

        r = self.session.get(url_tipo_processo)
        soup = BeautifulSoup(r.text, 'html.parser')
        form = soup.find('form')

        parsed = urlparse(url_tipo_processo)
        query_params = parse_qs(parsed.query)
        query_params = {k: v[0] for k, v in query_params.items()}
        post_url = 'https://sei.prf.gov.br/sei/controlador.php?' + urlencode(query_params)

        payload = {tag.get('name'): tag.get('value', '') for tag in form.find_all('input') if tag.get('name')}

        print('\nCampos do formulário encontrados:')
        for tag in form.find_all('input'):
            name = tag.get('name')
            value = tag.get('value', '')
            if name:
                print(f"  - {name} = {value}")

        """ if not payload.get('hdnAssuntos'):
            payload['hdnAssuntos'] = '727§313 - CANCELAMENTO' """

        payload.update({
            'txtDescricao': especificacao,
            'rdoProtocolo': 'A',
            'rdoNivelAcesso': '0',
            'hdnFlagProcedimentoCadastro': '2',
            'hdnSinIndividual': 'N',
            'hdnDtaGeracao': '11/07/2025',
            'sbmSalvar': 'Salvar',
            'hdnIdUnidade': '110000471',
            'hdnIdTipoProcedimento': query_params.get('id_tipo_procedimento', ''),
            'hdnInfraUnidadeAtual': query_params.get('infra_unidade_atual', ''),
            'hdnIdAssunto': '727',
            'hdnIdSerie': '',
            'hdnIdClassificacao': '',
            'hdnSiglaDocumentoPrincipal': ''
        })

        headers_post = {
            'Referer': url_tipo_processo,
            'Origin': 'https://sei.prf.gov.br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'Connection': 'keep-alive'
        }

        r = self.session.post(post_url, data=payload, headers=headers_post)

        if 'ifrVisualizacao' in r.text:
            print('[ok] Processo criado com sucesso.')
        else:
            with open('falha_criar_processo.html', 'w', encoding='utf-8') as f:
                f.write(r.text)

            soup = BeautifulSoup(r.text, 'html.parser')
            erros = []
            for seletor in ['.infraErro', '.mensagemErro', '#divInfraMensagem', '#txaInfraMsg']:
                elem = soup.select_one(seletor)
                if elem and elem.text.strip():
                    erros.append(elem.text.strip())

            if erros:
                raise Exception(f'Falha ao criar processo. Erros detectados: {erros}')
            else:
                raise Exception('Falha ao criar processo. HTML salvo para análise.')

if __name__ == '__main__':
    proc = ProcessoSEI('flavio.rigotte', 'Cacoal1981j@', '696464')
    proc.iniciar_processo('Multas: Auto de Infração - Cancelamento', 'Cancelamento de multa indevida')
