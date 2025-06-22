import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def buscar_dados(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # Exemplo: extrair título da página
    return {"titulo": soup.title.string if soup.title else None}


def carregar_cookies(driver, cookies_json, base_url):
    import json

    cookies = json.loads(cookies_json)
    driver.get(base_url)  # precisa abrir o domínio primeiro

    for cookie in cookies:
        cookie.pop("sameSite", None)  # remove campos problemáticos
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"[cookie erro] {cookie['name']}: {e}")


def init_chrome_driver(chromedriver_path: str, headless: bool = True):
    """Cria instancia padrao do Chrome driver."""
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(chromedriver_path)
    return webdriver.Chrome(service=service, options=options)


def wait_visible_send_keys(driver, by: By, value: str, text: str, timeout: int = 10):
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )
    element.send_keys(text)
    return element


def wait_click(driver, by: By, value: str, timeout: int = 10, js: bool = False):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    if js:
        driver.execute_script("arguments[0].click();", element)
    else:
        element.click()
    return element


def wait_presence(driver, by: By, value: str, timeout: int = 10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def get_js_value(driver, by: By, value: str, timeout: int = 10):
    element = wait_presence(driver, by, value, timeout)
    return driver.execute_script("return arguments[0].value;", element)


def remove_if_present(driver, by: By, value: str, timeout: int = 3):
    try:
        element = wait_presence(driver, by, value, timeout)
        driver.execute_script("arguments[0].remove();", element)
    except Exception:
        pass


def set_local_storage_json(driver, key: str, data: dict):
    import json

    driver.execute_script(
        "localStorage.setItem(arguments[0], JSON.stringify(arguments[1]));",
        key,
        data,
    )


def get_local_storage_token(driver, key: str):
    return driver.execute_script(
        """
        try {
            const raw = localStorage.getItem(arguments[0]);
            if (!raw) return '';
            const parsed = JSON.parse(raw);
            return parsed.token || '';
        } catch(e) {
            return '';
        }
        """,
        key,
    )


def find_cookie_token(driver, keywords=("jwt", "token")):
    for c in driver.get_cookies():
        name = c.get("name", "").lower()
        if any(k in name for k in keywords):
            return c.get("value")
    return ""
