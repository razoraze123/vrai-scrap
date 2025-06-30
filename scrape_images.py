import os
import random
import time
from pathlib import Path

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

IMAGE_DIR = Path("images")
PRODUCT_URL = os.environ.get(
    "PRODUCT_URL",
    "https://bob-crew.com/products/bob-ficelle-outdoor?variant=47696674062682",
)


def setup_driver() -> webdriver.Chrome:
    """Configure and return a Chrome WebDriver in stealth mode."""

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/113.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"},
    )
    return driver


def fetch_images(driver: webdriver.Chrome, url: str):
    """Return all <img> elements found in the product gallery."""
    driver.get(url)
    time.sleep(random.uniform(2, 4))
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div[data-media-type='image'] img")
        )
    )
    return driver.find_elements(By.CSS_SELECTOR, "div[data-media-type='image'] img")


def save_images(img_elements):
    """Download the images to IMAGE_DIR."""
    IMAGE_DIR.mkdir(exist_ok=True)
    session = requests.Session()
    for idx, img in enumerate(img_elements, 1):
        src = img.get_attribute("src")
        if not src:
            continue
        if src.startswith("//"):
            src = "https:" + src
        print(f"\u2B07\uFE0F Téléchargement image {idx}: {src}")
        try:
            response = session.get(src, timeout=30)
            response.raise_for_status()
            ext = os.path.splitext(src.split("?")[0])[1] or ".jpg"
            with open(IMAGE_DIR / f"image_{idx}{ext}", "wb") as f:
                f.write(response.content)
        except Exception as e:
            print(f"\u26A0\uFE0F Erreur téléchargement {src}: {e}")


def main():
    driver = setup_driver()
    try:
        images = fetch_images(driver, PRODUCT_URL)
        print(f"\U0001F4F8 {len(images)} images trouvées.")
        save_images(images)
    finally:
        driver.quit()
    print(f"\u2705 Toutes les images ont été enregistrées dans le dossier {IMAGE_DIR}")


if __name__ == "__main__":
    main()
