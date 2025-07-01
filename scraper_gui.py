import sys
import logging
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
)
from PySide6.QtCore import Qt, QThread, Signal, QObject

import scrape_images
import html_selector_tool


class LogEmitter(QObject):
    new_record = Signal(str, str)


class QTextEditHandler(logging.Handler):
    def __init__(self, emitter: LogEmitter):
        super().__init__()
        self.emitter = emitter

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        color = "red" if record.levelno >= logging.ERROR else "black"
        self.emitter.new_record.emit(msg, color)


class ScrapeThread(QThread):
    finished = Signal()

    def __init__(self, url: str, selector: str, logger: logging.Logger):
        super().__init__()
        self.url = url
        self.selector = selector
        self.logger = logger

    def run(self) -> None:
        scrape_images.scrape_images(self.url, self.logger, self.selector)
        self.finished.emit()


class ScraperGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scraper d'images")
        self.resize(800, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title = QLabel("\U0001F5BC\uFE0F Scraper d\u2019images de produit")
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("font-size:18px;font-weight:bold;")
        layout.addWidget(title)

        params_box = QGroupBox("Param\u00e8tres")
        params_layout = QVBoxLayout()
        params_box.setLayout(params_layout)

        params_layout.addWidget(QLabel("URL du produit :"))
        self.url_input = QLineEdit(scrape_images.PRODUCT_URL)
        params_layout.addWidget(self.url_input)

        params_layout.addWidget(
            QLabel(
                "S\u00e9lecteur CSS personnalis\u00e9 (laisser vide pour la valeur par d\u00e9faut) :"
            )
        )
        self.selector_input = QLineEdit(scrape_images.DEFAULT_SELECTOR)
        params_layout.addWidget(self.selector_input)

        layout.addWidget(params_box)

        btn_layout = QHBoxLayout()
        self.start_button = QPushButton("Scraper maintenant")
        self.css_button = QPushButton("Ouvrir outil CSS")
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.css_button)
        layout.addLayout(btn_layout)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text, stretch=1)

        self.emitter = LogEmitter()
        self.emitter.new_record.connect(self.append_log)

        self.start_button.clicked.connect(self.on_start)
        self.css_button.clicked.connect(lambda: html_selector_tool.launch_tool(self))

        self.thread = None
        self.logger = logging.getLogger("scraper")

    def append_log(self, message: str, color: str) -> None:
        self.log_text.append(f'<span style="color:{color}">{message}</span>')
        sb = self.log_text.verticalScrollBar()
        sb.setValue(sb.maximum())

    def on_start(self) -> None:
        url = self.url_input.text().strip()
        if not url:
            return
        selector = self.selector_input.text().strip() or scrape_images.DEFAULT_SELECTOR
        self.start_button.setEnabled(False)
        self.log_text.clear()

        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()
        self.logger.addHandler(QTextEditHandler(self.emitter))

        self.thread = ScrapeThread(url, selector, self.logger)
        self.thread.finished.connect(lambda: self.start_button.setEnabled(True))
        self.thread.start()


def main() -> None:
    app = QApplication(sys.argv)
    gui = ScraperGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
