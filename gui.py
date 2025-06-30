import sys
import logging
import time
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QLabel,
)
from PySide6.QtCore import QObject, QThread, Signal


class LogEmitter(QObject):
    message = Signal(str)


class QtLogHandler(logging.Handler):
    def __init__(self, emitter: LogEmitter):
        super().__init__()
        self.emitter = emitter

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        self.emitter.message.emit(msg)


def scrape(url: str, logger: logging.Logger):
    """Dummy scrape function that logs progress."""
    logger.info("D\u00e9but du scraping pour %s", url)
    for i in range(1, 4):
        time.sleep(1)
        logger.info("\u2705 Etape %d termin\u00e9e", i)
    logger.info("Fin du scraping")


class Worker(QObject):
    finished = Signal()

    def __init__(self, url: str, logger: logging.Logger):
        super().__init__()
        self.url = url
        self.logger = logger

    def run(self):
        try:
            scrape(self.url, self.logger)
        finally:
            self.finished.emit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scraper d'images")

        self.layout = QVBoxLayout(self)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("URL du produit")

        self.scrape_button = QPushButton("Scraper les images")
        self.quit_button = QPushButton("Quitter")

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)

        self.layout.addWidget(QLabel("URL du produit"))
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.scrape_button)
        self.layout.addWidget(self.log_view)
        self.layout.addWidget(self.quit_button)

        self.emitter = LogEmitter()
        self.emitter.message.connect(self.log_view.append)

        self.logger = logging.getLogger("scraper_gui")
        self.logger.setLevel(logging.INFO)
        handler = QtLogHandler(self.emitter)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        # Also log to console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        self.scrape_button.clicked.connect(self.start_scrape)
        self.quit_button.clicked.connect(QApplication.instance().quit)

        self.thread = None

    def start_scrape(self):
        url = self.url_input.text().strip()
        if not url:
            self.logger.warning("Aucune URL fournie")
            return

        self.scrape_button.setEnabled(False)
        self.log_view.clear()

        worker = Worker(url, self.logger)
        thread = QThread(self)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(self.scrape_finished)
        thread.finished.connect(thread.deleteLater)
        thread.start()
        self.thread = thread

    def scrape_finished(self):
        self.scrape_button.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
