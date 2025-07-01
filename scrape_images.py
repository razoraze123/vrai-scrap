import os
import random
import time
from pathlib import Path
import logging

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

# Default CSS selector for product images
DEFAULT_SELECTOR = "div[data-media-type='image'] img"


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


def fetch_images(driver: webdriver.Chrome, url: str, selector: str):
    """Return all <img> elements found in the product gallery."""
    driver.get(url)
    time.sleep(random.uniform(2, 4))
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
    return driver.find_elements(By.CSS_SELECTOR, selector)


def download_image(
    img,
    index: int,
    session: requests.Session,
    logger: logging.Logger | None = None,
) -> None:
    """Extract the URL from ``img`` and save the file."""

    src = (
        img.get_attribute("src")
        or img.get_attribute("data-src")
        or img.get_attribute("data-photoswipe-src")
        or None
    )
    if not src:
        message = f"\u274C Aucun attribut d'image trouv\u00e9 pour l'\u00e9l\u00e9ment {index}"
        if logger:
            logger.warning(message)
        else:
            print(message)
        return

    if "{width}" in src:
        message = f"\u26D4\uFE0F Image ignor\u00e9e (placeholder non r\u00e9solu) : {src}"
        if logger:
            logger.warning(message)
        else:
            print(message)
        return

    if src.startswith("//"):
        src = "https:" + src

    if logger:
        logger.info("\u2B07\uFE0F T\u00e9l\u00e9chargement image %d: %s", index, src)
    else:
        print(f"\u2B07\uFE0F T\u00e9l\u00e9chargement image {index}: {src}")

    try:
        response = session.get(src, timeout=30)
        response.raise_for_status()
        ext = os.path.splitext(src.split("?")[0])[1] or ".jpg"
        with open(IMAGE_DIR / f"image_{index}{ext}", "wb") as f:
            f.write(response.content)
    except Exception as e:
        if logger:
            logger.error("\u26A0\uFE0F Erreur t\u00e9l\u00e9chargement %s: %s", src, e)
        else:
            print(f"\u26A0\uFE0F Erreur t\u00e9l\u00e9chargement {src}: {e}")


def save_images(img_elements):
    """Download the images to IMAGE_DIR."""
    IMAGE_DIR.mkdir(exist_ok=True)
    session = requests.Session()
    for idx, img in enumerate(img_elements, 1):
        download_image(img, idx, session)

def scrape_images(
    url: str,
    logger: logging.Logger | None = None,
    selector: str = DEFAULT_SELECTOR,
) -> None:
    """Scrape product images from the given URL and save them locally."""
    if logger is None:
        logger = logging.getLogger(__name__)

    logger.info("D\u00e9but du scraping pour %s", url)
    driver = setup_driver()
    try:
        images = fetch_images(driver, url, selector)
        if not images:
            logger.info("Aucun \u00e9l\u00e9ment trouv\u00e9 avec le s\u00e9lecteur : %s", selector)
            return
        logger.info("\U0001F4C4 %d \u00e9l\u00e9ments trouv\u00e9s.", len(images))

        IMAGE_DIR.mkdir(exist_ok=True)
        session = requests.Session()
        for idx, img in enumerate(images, 1):
            download_image(img, idx, session, logger)
    finally:
        driver.quit()
    logger.info(
        "\u2705 Toutes les images ont \u00e9t\u00e9 enregistr\u00e9es dans le dossier %s",
        IMAGE_DIR,
    )


def main():
    driver = setup_driver()
    try:
        images = fetch_images(driver, PRODUCT_URL, DEFAULT_SELECTOR)
        if not images:
            print(f"Aucun élément trouvé avec le sélecteur : {DEFAULT_SELECTOR}")
            return
        print(f"\U0001F4F8 {len(images)} images trouvées.")
        save_images(images)
    finally:
        driver.quit()
    print(f"\u2705 Toutes les images ont été enregistrées dans le dossier {IMAGE_DIR}")


if __name__ == "__main__":
    main()
