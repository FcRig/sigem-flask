from selenium.webdriver.common.by import By
from flask import current_app
from time import sleep

from ..utils.scraping_utils import (
    init_chrome_driver,
    wait_visible_send_keys,
    wait_click,
    wait_presence,
    get_js_value,
    remove_if_present,
    set_local_storage_json,
    get_local_storage_token,
    find_cookie_token,
)


class AutoPRFClient:
    def __init__(self, jwt_token: str | None = None):
        chromedriver_path = current_app.config.get("CHROMEDRIVER_PATH")
        if not chromedriver_path:
            raise RuntimeError("CHROMEDRIVER_PATH não está definido na configuração.")
        self.driver = init_chrome_driver(chromedriver_path)
        self.jwt_token = jwt_token or ""

    def login(self, cpf: str, password: str, token: str) -> str:
        driver = self.driver
        driver.get("https://auto.prf.gov.br/#/login")

        # Preenche login
        wait_visible_send_keys(driver, By.NAME, "username", cpf)
        wait_visible_send_keys(driver, By.NAME, "password", password)
        wait_visible_send_keys(driver, By.NAME, "token", token)

        remove_if_present(driver, By.ID, "cookieconsent:desc")

        # Usa JavaScript para clicar no botão, evitando bloqueios por sobreposição
        wait_click(driver, By.CSS_SELECTOR, 'button[type="submit"]', js=True)

        # Aguarda redirecionamento após login (ajuste conforme comportamento da aplicação)
        wait_presence(driver, By.TAG_NAME, "body")

        sleep(3)

        jwt_token = get_local_storage_token(driver, "jwt_sessao")
        if not jwt_token:
            jwt_token = find_cookie_token(driver)

        driver.quit()
        return jwt_token or ""

    def pesquisa_auto_infracao(self, auto_infracao: str) -> dict:
        """Busca dados do Auto de Infração e retorna um dicionário estruturado."""
        driver = self.driver

        if self.jwt_token:
            driver.get("https://auto.prf.gov.br")
            set_local_storage_json(driver, "jwt_sessao", {"token": self.jwt_token})
            driver.get("https://auto.prf.gov.br/#/autuacao/listar-auto-infracao")

        wait_presence(driver, By.TAG_NAME, "app-dashboard", timeout=20)

        wait_click(driver, By.CSS_SELECTOR, "body > div > div > a")
        wait_visible_send_keys(driver, By.NAME, "numero", auto_infracao)
        wait_click(driver, By.CSS_SELECTOR, "button[type='submit']")
        wait_click(driver, By.CSS_SELECTOR, 'span[class="fa fa-search-plus"]')

        result = {"infracao": {}, "veiculo": {}, "local": {}}

        input_element = wait_presence(
            driver, By.CSS_SELECTOR, "ng-select div.ng-value.ng-star-inserted"
        )
        result["infracao"]["codigo_descricao"] = input_element.text

        result["infracao"]["amparo_legal"] = get_js_value(driver, By.ID, "amparoLegal")
        result["infracao"]["gravidade"] = get_js_value(driver, By.ID, "gravidade")
        result["infracao"]["tipo_infrator"] = get_js_value(driver, By.ID, "tpInfrator")

        radio1 = driver.find_element(By.ID, "abordagem1")
        radio2 = driver.find_element(By.ID, "abordagem2")
        if radio1.is_selected():
            result["infracao"]["tipo_abordagem"] = "Com Abordagem"
        elif radio2.is_selected():
            result["infracao"]["tipo_abordagem"] = "Sem Abordagem"

        emplacamento_element = driver.find_element(By.NAME, "emplacamento")
        result["veiculo"]["emplacamento"] = emplacamento_element.get_attribute("value")

        result["veiculo"]["placa"] = get_js_value(driver, By.NAME, "placa")
        result["veiculo"]["chassi"] = get_js_value(driver, By.NAME, "chassi")
        result["veiculo"]["renavam"] = get_js_value(driver, By.NAME, "renavam")

        pais_element = driver.find_element(By.NAME, "pais")
        result["veiculo"]["pais"] = pais_element.get_attribute("value")

        uf_veiculo_element = driver.find_element(By.NAME, "ufVeiculo")
        result["veiculo"]["uf"] = uf_veiculo_element.get_attribute("value").split(": ")[
            -1
        ]

        marca_veiculo_element = driver.find_element(By.NAME, "marca")
        result["veiculo"]["marca"] = marca_veiculo_element.get_attribute("value")

        outra_marca_veiculo_element = driver.find_element(By.NAME, "nomeOutraMarca")
        result["veiculo"]["outra_marca"] = outra_marca_veiculo_element.get_attribute(
            "value"
        )

        result["veiculo"]["modelo"] = wait_presence(
            driver, By.NAME, "modelo"
        ).get_attribute("value")

        cor_veiculo_element = driver.find_element(By.NAME, "cor")
        result["veiculo"]["cor"] = cor_veiculo_element.get_attribute("value").split(
            ": "
        )[-1]

        especie_veiculo_element = driver.find_element(By.NAME, "especie")
        result["veiculo"]["especie"] = especie_veiculo_element.get_attribute(
            "value"
        ).split(": ")[-1]

        tipo_veiculo_element = driver.find_element(By.NAME, "tipo")
        result["veiculo"]["tipo"] = tipo_veiculo_element.get_attribute("value").split(
            ": "
        )[-1]

        categoria_veiculo_element = driver.find_element(By.NAME, "categoria")
        result["veiculo"]["categoria"] = categoria_veiculo_element.get_attribute(
            "value"
        ).split(": ")[-1]

        tipo_documento_element = driver.find_element(
            By.XPATH, "//label[contains(text(), 'Tipo Documento')]/following::select[1]"
        )
        result["veiculo"]["tipo_documento"] = tipo_documento_element.get_attribute(
            "value"
        ).split(": ")[-1]

        numero_documento_element = driver.find_element(
            By.XPATH, "//label[contains(text(), 'Nº Documento')]/following::input[1]"
        )
        result["veiculo"]["numero_documento"] = numero_documento_element.get_attribute(
            "value"
        )

        nome_element = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Nome/Razão Social')]/following::input[1]",
        )
        result["veiculo"]["nome_razao_social"] = nome_element.get_attribute("value")

        radios = driver.find_elements(By.NAME, "tipoComposicao")
        for radio in radios:
            if radio.is_selected():
                label = radio.find_element(By.XPATH, "following-sibling::label")
                result["veiculo"]["tipo_composicao"] = label.text
                break

        municipio_element = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Código/Município/UF')]/following::div[4]",
        )
        result["local"]["codigo_municipio_uf"] = municipio_element

       

        


        driver.quit()
        return result
