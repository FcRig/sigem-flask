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
    
    def pesquisa_auto_infracao(self, auto_infracao: str) -> None:
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

        # Fechando o banner de cookies
        menu_autuacao = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div > div > a'))
        )
        menu_autuacao.click()        

        # Inserindo o número do AI
        input_ai = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, 'numero'))
        )
        input_ai.send_keys(auto_infracao)

        # Clicando em Pesquisar
        input_ai = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        input_ai.click()

        # Clicando na lupa para visualização
        icone_lupa_ai = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[class="fa fa-search-plus"]'))
        )
        icone_lupa_ai.click()        

        wait = WebDriverWait(driver, 10)
        input_element = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "ng-select div.ng-value.ng-star-inserted"
            ))
        )
        print("Descrição:", input_element.text)

        # Espera o input com id 'amparoLegal' estar presente
        wait = WebDriverWait(driver, 10)
        input_amparo = wait.until(EC.presence_of_element_located((By.ID, "amparoLegal")))

        # Pega o valor do campo via JavaScript (DOM real)
        valor_amparo = driver.execute_script("return arguments[0].value;", input_amparo)
        print("Amparo Legal':", valor_amparo)

        # Espera o input 'gravidade' aparecer no DOM
        wait = WebDriverWait(driver, 10)
        campo_gravidade = wait.until(
            EC.presence_of_element_located((By.ID, "gravidade"))
        )

        # Extrai o valor diretamente do DOM real (via JavaScript)
        valor_gravidade = driver.execute_script("return arguments[0].value;", campo_gravidade)
        print("Gravidade:", valor_gravidade)

        # Espera o input 'Tipo de infrator' aparecer no DOM
        wait = WebDriverWait(driver, 10)
        campo_tipo_infrator = wait.until(
            EC.presence_of_element_located((By.ID, "tpInfrator"))
        )

        # Extrai o valor diretamente do DOM real (via JavaScript)
        valor_tipo_infrator = driver.execute_script("return arguments[0].value;", campo_tipo_infrator)
        print("Tipo de infrator:", valor_tipo_infrator)
        
        # Buscando o tipo de abordagem
        # Encontra os dois inputs
        radio1 = driver.find_element(By.ID, "abordagem1")
        radio2 = driver.find_element(By.ID, "abordagem2")

        # Verifica qual está selecionado
        if radio1.is_selected():
            print("Tipo de abordagem: Com Abordagem")
        elif radio2.is_selected():
            print("Tipo de abordagem: Sem Abordagem")
        else:
            print("Nenhum selecionado.")

        # Emplacamento 
        # Localiza o elemento <select>
        emplacamento_element = driver.find_element(By.NAME, "emplacamento")

        # Pega o valor atual selecionado diretamente do DOM
        emplacamento_value = emplacamento_element.get_attribute("value")
        print("Emplacamento:", emplacamento_value)

        # Espera o input 'Placa' aparecer no DOM
        wait = WebDriverWait(driver, 10)
        campo_placa = wait.until(
            EC.presence_of_element_located((By.NAME, "placa"))
        )

        # Extrai o valor diretamente do DOM real (via JavaScript)
        valor_placa = driver.execute_script("return arguments[0].value;", campo_placa)
        print("Placa:", valor_placa)

        # Espera o input 'Chassi' aparecer no DOM
        wait = WebDriverWait(driver, 10)
        campo_chassi = wait.until(
            EC.presence_of_element_located((By.NAME, "chassi"))
        )

        # Extrai o valor diretamente do DOM real (via JavaScript)
        valor_chassi = driver.execute_script("return arguments[0].value;", campo_chassi)
        print("Chassi:", valor_chassi)

        # Espera o input 'Renavam' aparecer no DOM
        wait = WebDriverWait(driver, 10)
        campo_renavam = wait.until(
            EC.presence_of_element_located((By.NAME, "renavam"))
        )

        # Extrai o valor diretamente do DOM real (via JavaScript)
        valor_renavam = driver.execute_script("return arguments[0].value;", campo_renavam)
        print("Renavam:", valor_renavam)

        # País
        # Localiza o elemento <select>
        pais_element = driver.find_element(By.NAME, "pais")

        # Pega o valor atual selecionado diretamente do DOM
        pais_value = pais_element.get_attribute("value")
        print("pais:", pais_value)
        
        # UF do Veículo
        # Localiza o elemento <select>
        uf_veiculo_element = driver.find_element(By.NAME, "ufVeiculo")

        # Pega o valor atual selecionado diretamente do DOM
        uf_veiculo_value = uf_veiculo_element.get_attribute("value").split(': ')[-1]
        print("UF:", uf_veiculo_value)

        # Marca do Veículo
        # Localiza o elemento <select>
        marca_veiculo_element = driver.find_element(By.NAME, "marca")

        # Pega o valor atual selecionado diretamente do DOM
        marca_veiculo_value = marca_veiculo_element.get_attribute("value")
        print("Marca:", marca_veiculo_value)

        # Outra marca do Veículo
        # Localiza o elemento <select>
        outra_marca_veiculo_element = driver.find_element(By.NAME, "nomeOutraMarca")

        # Pega o valor atual selecionado diretamente do DOM
        outra_marca_veiculo_value = outra_marca_veiculo_element.get_attribute("value")
        print("Outra marca:", outra_marca_veiculo_value)

        # Espera o input 'Modelo' aparecer no DOM
        wait = WebDriverWait(driver, 10)
        campo_modelo = wait.until(
            EC.presence_of_element_located((By.NAME, "modelo"))
        )

        # Extrai o valor diretamente do DOM real (via JavaScript)        
        valor_modelo = campo_modelo.get_attribute('value')
        print("Modelo:", valor_modelo)

        # Cor do Veículo
        # Localiza o elemento <select>
        cor_veiculo_element = driver.find_element(By.NAME, "cor")

        # Pega o valor atual selecionado diretamente do DOM
        cor_veiculo_value = cor_veiculo_element.get_attribute("value").split(': ')[-1]
        print("Cor:", cor_veiculo_value)

        # Espécie do Veículo
        # Localiza o elemento <select>
        especie_veiculo_element = driver.find_element(By.NAME, "especie")

        # Pega o valor atual selecionado diretamente do DOM
        especie_veiculo_value = especie_veiculo_element.get_attribute("value").split(': ')[-1]
        print("Especie:", especie_veiculo_value)

        # Tipo do Veículo
        # Localiza o elemento <select>
        tipo_veiculo_element = driver.find_element(By.NAME, "tipo")

        # Pega o valor atual selecionado diretamente do DOM
        tipo_veiculo_value = tipo_veiculo_element.get_attribute("value").split(': ')[-1]
        print("tipo:", tipo_veiculo_value)
        
        # Categoria do Veículo
        # Localiza o elemento <select>
        categoria_veiculo_element = driver.find_element(By.NAME, "categoria")

        # Pega o valor atual selecionado diretamente do DOM
        categoria_veiculo_value = categoria_veiculo_element.get_attribute("value").split(': ')[-1]
        print("Categoria:", categoria_veiculo_value)       

        # Tipo de documento
        # Localiza o elemento <select>        
        tipo_documento_element = driver.find_element(By.XPATH, "//label[contains(text(), 'Tipo Documento')]/following::select[1]")

        # Pega o valor atual selecionado diretamente do DOM
        tipo_documento_value = tipo_documento_element.get_attribute("value").split(': ')[-1]
        print("Tipo de documento:", tipo_documento_value)

        # Número do documento
        # Localiza o elemento <select>        
        numero_documento_element = driver.find_element(By.XPATH, "//label[contains(text(), 'Nº Documento')]/following::input[1]")

        # Pega o valor atual selecionado diretamente do DOM
        numero_documento_value = numero_documento_element.get_attribute("value")
        print("Número do documento:", numero_documento_value)

        # Nome/Razão Social
        # Localiza o elemento <select>        
        nome_element = driver.find_element(By.XPATH, "//label[contains(text(), 'Nome/Razão Social')]/following::input[1]")

        # Pega o valor atual selecionado diretamente do DOM
        nome_value = nome_element.get_attribute("value")
        print("Nome/Razão Social:", nome_value)
        
        # Buscando o tipo de composição
        # Pega todos os rádios com mesmo name
        radios = driver.find_elements(By.NAME, "tipoComposicao")

        for radio in radios:
            if radio.is_selected():
                # Pega o label associado se quiser
                label = radio.find_element(By.XPATH, "following-sibling::label")
                print("Selecionado:", label.text)
                break        
        
        # Código/Município/UF        
        municipio_element = driver.find_element(By.XPATH, "//label[contains(text(), 'Código/Município/UF')]/following::div[4]")        
        print("Código/Município/UF:", municipio_element.text)  
        
 


        driver.quit()