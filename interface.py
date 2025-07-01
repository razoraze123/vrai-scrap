import tkinter as tk
from tkinter import scrolledtext
import threading
import logging

import html_selector_tool

import scrape_images

DEFAULT_SELECTOR = scrape_images.DEFAULT_SELECTOR

class TextHandler(logging.Handler):
    """Redirect logging records to a Tkinter Text widget."""
    def __init__(self, text_widget: tk.Text):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, msg + "\n")
        self.text_widget.configure(state="disabled")
        self.text_widget.yview(tk.END)


def start_scraping(url: str, selector: str, text_widget: tk.Text, button: tk.Button) -> None:
    handler = TextHandler(text_widget)
    logger = logging.getLogger("scraper")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)

    def run() -> None:
        scrape_images.scrape_images(url, logger, selector)
        button.config(state=tk.NORMAL)

    threading.Thread(target=run, daemon=True).start()


def main() -> None:
    root = tk.Tk()
    root.title("Scraper d'images")

    tk.Label(root, text="URL du produit:").pack(padx=5, pady=(5, 0))
    url_entry = tk.Entry(root, width=80)
    url_entry.insert(0, scrape_images.PRODUCT_URL)
    url_entry.pack(padx=5, pady=5)

    tk.Label(
        root,
        text="S\u00e9lecteur CSS personnalis\u00e9 (laisser vide pour la valeur par d\u00e9faut) :",
    ).pack(padx=5, pady=(0, 0))
    selector_entry = tk.Entry(root, width=80)
    selector_entry.insert(0, DEFAULT_SELECTOR)
    selector_entry.pack(padx=5, pady=5)

    start_button = tk.Button(root, text="Scraper les images")
    start_button.pack(pady=(0, 5))

    css_button = tk.Button(root, text="Ouvrir outil CSS", command=lambda: html_selector_tool.launch_tool(root))
    css_button.pack(pady=(0, 5))

    log_text = scrolledtext.ScrolledText(root, state="disabled", width=80, height=20)
    log_text.pack(padx=5, pady=5)

    def on_click() -> None:
        url = url_entry.get().strip()
        if not url:
            return
        selector = selector_entry.get().strip() or DEFAULT_SELECTOR
        start_button.config(state=tk.DISABLED)
        log_text.configure(state="normal")
        log_text.delete("1.0", tk.END)
        log_text.configure(state="disabled")
        start_scraping(url, selector, log_text, start_button)

    start_button.config(command=on_click)

    root.mainloop()


if __name__ == "__main__":
    main()
