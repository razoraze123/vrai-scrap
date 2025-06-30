import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QLabel,
)
from PySide6.QtCore import QProcess, QProcessEnvironment

from scrape_images import PRODUCT_URL


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scraper d'images")

        self.layout = QVBoxLayout(self)

        self.url_input = QLineEdit()
        self.url_input.setText(PRODUCT_URL)
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

        self.scrape_button.clicked.connect(self.start_scrape)
        self.quit_button.clicked.connect(QApplication.instance().quit)

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.finished.connect(self.process_finished)

    def start_scrape(self):
        url = self.url_input.text().strip()
        if not url:
            self.log_view.append("Aucune URL fournie")
            return

        self.scrape_button.setEnabled(False)
        self.log_view.clear()

        env = QProcessEnvironment.systemEnvironment()
        env.insert("PRODUCT_URL", url)
        self.process.setProcessEnvironment(env)

        python = sys.executable
        self.process.start(python, [os.path.join(os.path.dirname(__file__), "scrape_images.py")])

    def handle_output(self):
        data = self.process.readAllStandardOutput().data().decode("utf-8", errors="ignore")
        if data:
            self.log_view.moveCursor(self.log_view.textCursor().End)
            self.log_view.insertPlainText(data)
            self.log_view.moveCursor(self.log_view.textCursor().End)

    def process_finished(self):
        self.scrape_button.setEnabled(True)
        self.log_view.append("\nScraping termin\u00e9.")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
