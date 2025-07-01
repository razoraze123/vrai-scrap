import os
import random
import time
from pathlib import Path
import logging
import argparse

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
    """Return <img> elements matching ``selector`` or use a fallback."""
    driver.get(url)
    time.sleep(random.uniform(2, 4))
    wait = WebDriverWait(driver, 10)

    try:
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
    except Exception:
        # If the explicit selector fails we will use the fallback
        pass

    images = driver.find_elements(By.CSS_SELECTOR, selector)
    if images:
        return images

    # Fallback: collect visible <img> nodes and filter by dimensions
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
    imgs = driver.find_elements(By.TAG_NAME, "img")
    filtered = []
    for img in imgs:
        if not img.is_displayed():
            continue
        width = img.size.get("width", 0)
        height = img.size.get("height", 0)
        if width < 300 or height < 300:
            continue
        cls = (img.get_attribute("class") or "").lower()
        parent_cls = ""
        try:
            parent_cls = (
                img.find_element(By.XPATH, "..").get_attribute("class") or ""
            ).lower()
        except Exception:
            pass
        if "thumbnail" in cls or "thumbnail" in parent_cls:
            continue
        filtered.append(img)
    return filtered


def _best_url_from_srcset(srcset: str) -> str | None:
    """Return the URL with the highest resolution from a ``srcset`` string."""

    candidates = []
    for item in srcset.split(','):
        item = item.strip()
        if not item:
            continue
        parts = item.split()
        url = parts[0]
        width = 0
        if len(parts) > 1:
            if parts[1].endswith('w'):
                try:
                    width = int(parts[1][:-1])
                except ValueError:
                    width = 0
        candidates.append((width, url))
    if not candidates:
        return None
    # choose candidate with max width (falls back to first if all widths are 0)
    candidates.sort(key=lambda x: x[0])
    return candidates[-1][1]


def _extract_image_url(
    img,
    index: int,
    logger: logging.Logger | None = None,
) -> str | None:
    """Inspect ``img`` element attributes and return the best image URL."""

    for attr in ("srcset", "data-srcset", "data-lazy"):
        value = img.get_attribute(attr)
        if value:
            url = _best_url_from_srcset(value) if "," in value else value
            if url:
                return url

    src = (
        img.get_attribute("src")
        or img.get_attribute("data-src")
        or img.get_attribute("data-photoswipe-src")
    )
    if not src:
        message = f"\u274C Aucun attribut d'image trouv\u00e9 pour l'\u00e9l\u00e9ment {index}"
        if logger:
            logger.warning(message)
        else:
            print(message)
        return None

    return src


def download_image(
    img,
    index: int,
    session: requests.Session,
    logger: logging.Logger | None = None,
) -> None:
    """Extract the URL from ``img`` and save the file."""

    src = _extract_image_url(img, index, logger)
    if not src:
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
    global IMAGE_DIR

    parser = argparse.ArgumentParser(description="Scrape images from a product page")
    parser.add_argument("url", help="URL de la page produit")
    parser.add_argument(
        "-s",
        "--selector",
        default=DEFAULT_SELECTOR,
        help="Sélecteur CSS pour cibler les images (défaut: %(default)s)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=str(IMAGE_DIR),
        help="Dossier de destination des images",
    )
    args = parser.parse_args()

    IMAGE_DIR = Path(args.output_dir)

    driver = setup_driver()
    try:
        images = fetch_images(driver, args.url, args.selector)
        if not images:
            print(f"Aucun élément trouvé avec le sélecteur : {args.selector}")
            return
        print(f"\U0001F4F8 {len(images)} images trouvées.")
        save_images(images)
    finally:
        driver.quit()
    print(f"\u2705 Toutes les images ont été enregistrées dans le dossier {IMAGE_DIR}")


if __name__ == "__main__":
    main()
