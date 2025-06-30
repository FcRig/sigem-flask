from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from flask import current_app
from time import sleep

class AutoPRFClient:
    def __init__(self, jwt_token: str | None = None):
        chromedriver_path = current_app.config.get('CHROMEDRIVER_PATH')
        if not chromedriver_path:
            raise RuntimeError("CHROMEDRIVER_PATH não está definido na configuração.")
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.jwt_token = jwt_token or ''

    def login(self, cpf: str, password: str, token: str) -> str:
        driver = self.driver
        driver.get('https://auto.prf.gov.br/#/login')

        # Preenche login
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'username'))
        ).send_keys(cpf)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.NAME, 'token').send_keys(token)

        # Tenta remover banner de cookies
        try:
            cookie_span = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, 'cookieconsent:desc'))
            )
            driver.execute_script("arguments[0].remove();", cookie_span)
        except:
            pass  # Ignora se não aparecer

        # Usa JavaScript para clicar no botão, evitando bloqueios por sobreposição
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        driver.execute_script("arguments[0].click();", login_button)

        # Aguarda redirecionamento após login (ajuste conforme comportamento da aplicação)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        sleep(3)                  

        jwt_token = driver.execute_script("""
            try {
                const raw = localStorage.getItem('jwt_sessao');
                if (!raw) return '';
                const parsed = JSON.parse(raw);
                return parsed.token || '';
            } catch (e) {
                return '';
            }
        """)     

        if not jwt_token:
            for c in driver.get_cookies():
                name = c.get('name', '').lower()
                if 'jwt' in name or 'token' in name:
                    jwt_token = c.get('value')
                    break
        
        driver.quit()
        return jwt_token or ''
    
    def pesquisa_auto_infracao(self, auto_infracao: str) -> dict:
        """Busca dados do Auto de Infração e retorna um dicionário estruturado."""
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        if self.jwt_token:
            driver.get("https://auto.prf.gov.br")

            import json
            token_json = json.dumps({"token": self.jwt_token})
            driver.execute_script(f"""
                localStorage.setItem('jwt_sessao', {json.dumps(token_json)});
            """)

            driver.get("https://auto.prf.gov.br/#/autuacao/listar-auto-infracao")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "app-dashboard"))
        )        

        menu_autuacao = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div > div > a"))
        )
        menu_autuacao.click()

        input_ai = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "numero"))
        )
        input_ai.send_keys(auto_infracao)

        input_ai = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        input_ai.click()

        icone_lupa_ai = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.fa.fa-search-plus"))
        )
        icone_lupa_ai.click()

        result = {"infracao": {}, "veiculo": {}, "local": {}}

        input_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ng-select div.ng-value.ng-star-inserted"))
        )
        result["infracao"]["codigo_descricao"] = input_element.text

        input_amparo = wait.until(EC.presence_of_element_located((By.ID, "amparoLegal")))
        result["infracao"]["amparo_legal"] = driver.execute_script("return arguments[0].value;", input_amparo)

        campo_gravidade = wait.until(EC.presence_of_element_located((By.ID, "gravidade")))
        result["infracao"]["gravidade"] = driver.execute_script("return arguments[0].value;", campo_gravidade)

        campo_tipo_infrator = wait.until(EC.presence_of_element_located((By.ID, "tpInfrator")))
        result["infracao"]["tipo_infrator"] = driver.execute_script("return arguments[0].value;", campo_tipo_infrator)

        radio1 = driver.find_element(By.ID, "abordagem1")
        radio2 = driver.find_element(By.ID, "abordagem2")
        if radio1.is_selected():
            result["infracao"]["tipo_abordagem"] = "Com Abordagem"
        elif radio2.is_selected():
            result["infracao"]["tipo_abordagem"] = "Sem Abordagem"

        emplacamento_element = driver.find_element(By.NAME, "emplacamento")
        result["veiculo"]["emplacamento"] = emplacamento_element.get_attribute("value")

        campo_placa = wait.until(EC.presence_of_element_located((By.NAME, "placa")))
        result["veiculo"]["placa"] = driver.execute_script("return arguments[0].value;", campo_placa)

        campo_chassi = wait.until(EC.presence_of_element_located((By.NAME, "chassi")))
        result["veiculo"]["chassi"] = driver.execute_script("return arguments[0].value;", campo_chassi)

        campo_renavam = wait.until(EC.presence_of_element_located((By.NAME, "renavam")))
        result["veiculo"]["renavam"] = driver.execute_script("return arguments[0].value;", campo_renavam)

        pais_element = driver.find_element(By.NAME, "pais")
        result["veiculo"]["pais"] = pais_element.get_attribute("value")

        uf_veiculo_element = driver.find_element(By.NAME, "ufVeiculo")
        result["veiculo"]["uf"] = uf_veiculo_element.get_attribute("value").split(": ")[-1]

        marca_veiculo_element = driver.find_element(By.NAME, "marca")
        result["veiculo"]["marca"] = marca_veiculo_element.get_attribute("value")

        outra_marca_veiculo_element = driver.find_element(By.NAME, "nomeOutraMarca")
        result["veiculo"]["outra_marca"] = outra_marca_veiculo_element.get_attribute("value")

        campo_modelo = wait.until(EC.presence_of_element_located((By.NAME, "modelo")))
        result["veiculo"]["modelo"] = campo_modelo.get_attribute("value")

        cor_veiculo_element = driver.find_element(By.NAME, "cor")
        result["veiculo"]["cor"] = cor_veiculo_element.get_attribute("value").split(": ")[-1]

        especie_veiculo_element = driver.find_element(By.NAME, "especie")
        result["veiculo"]["especie"] = especie_veiculo_element.get_attribute("value").split(": ")[-1]

        tipo_veiculo_element = driver.find_element(By.NAME, "tipo")
        result["veiculo"]["tipo"] = tipo_veiculo_element.get_attribute("value").split(": ")[-1]

        categoria_veiculo_element = driver.find_element(By.NAME, "categoria")
        result["veiculo"]["categoria"] = categoria_veiculo_element.get_attribute("value").split(": ")[-1]

        tipo_documento_element = driver.find_element(By.XPATH, "//label[contains(text(), 'Tipo Documento')]/following::select[1]")
        result["veiculo"]["tipo_documento"] = tipo_documento_element.get_attribute("value").split(": ")[-1]

        numero_documento_element = driver.find_element(By.XPATH, "//label[contains(text(), 'Nº Documento')]/following::input[1]")
        result["veiculo"]["numero_documento"] = numero_documento_element.get_attribute("value")

        nome_element = driver.find_element(By.XPATH, "//label[contains(text(), 'Nome/Razão Social')]/following::input[1]")
        result["veiculo"]["nome_razao_social"] = nome_element.get_attribute("value")

        radios = driver.find_elements(By.NAME, "tipoComposicao")
        for radio in radios:
            if radio.is_selected():
                label = radio.find_element(By.XPATH, "following-sibling::label")
                result["veiculo"]["tipo_composicao"] = label.text
                break

        municipio_element = driver.find_element(By.XPATH, "//label[contains(text(), 'Código/Município/UF')]/following::div[4]")
        result["local"]["codigo_municipio_uf"] = municipio_element.text

        driver.quit()
        return result
