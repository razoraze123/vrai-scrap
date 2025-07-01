# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform
from PySide6.QtWidgets import QMessageBox
import scrape_images

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        # —— Renommage des boutons ——
        widgets.btn_home.setText("À venir")
        widgets.btn_widgets.setText("À venir")
        widgets.btn_new.setText("Scraping Image")
        widgets.btn_save.setText("Paramètres")



        # Boutons de l'onglet Scraping Image
        widgets.btn_launch_scraping.clicked.connect(self.run_scraper)
        widgets.btn_reset_fields.clicked.connect(self.reset_fields)

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "PyDracula - Modern GUI"
        description = "PyDracula APP - Theme with colors based on Dracula for Python."
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Configure scraping page widgets
        widgets.label.setText("\ud83d\udcf7 Scraping Image")
        title_font = widgets.label.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        widgets.label.setFont(title_font)
        widgets.label.setStyleSheet("color: #c678dd;")

        widgets.log_browser.setMinimumHeight(80)
        widgets.log_browser.setMaximumHeight(400)
        widgets.log_browser.setFixedHeight(200)
        widgets.log_browser.setStyleSheet(
            "background-color: #1e1e1e; color: #cccccc; font-family: Consolas, monospace; border-radius: 4px;"
        )

        widgets.btn_launch_scraping.setCursor(Qt.PointingHandCursor)
        widgets.btn_launch_scraping.setStyleSheet(
            "QPushButton {background-color:#6272a4; padding:6px 12px; border-radius:6px;}"
            "QPushButton:hover {background-color:#6f7fb8;}"
        )
        widgets.btn_reset_fields.setCursor(Qt.PointingHandCursor)
        widgets.btn_reset_fields.setStyleSheet(
            "QPushButton {background-color:#44475a; padding:6px 12px; border-radius:6px;}"
            "QPushButton:hover {background-color:#51546e;}"
        )

        # Create settings page (4th tab)
        settings_page = QWidget()
        widgets.settings_page = settings_page
        settings_layout = QVBoxLayout(settings_page)
        widgets.font_selector = QFontComboBox(settings_page)
        widgets.color_selector = QComboBox(settings_page)
        widgets.color_selector.addItems(["white", "lightgray", "yellow", "green", "red"])
        widgets.height_slider = QSlider(Qt.Horizontal, settings_page)
        widgets.height_slider.setRange(80, 400)
        widgets.height_slider.setValue(200)
        settings_layout.addWidget(widgets.font_selector)
        settings_layout.addWidget(widgets.color_selector)
        settings_layout.addWidget(widgets.height_slider)
        widgets.stackedWidget.addWidget(settings_page)

        def apply_font(font):
            widgets.log_browser.setFont(font)

        def apply_color(name):
            current_font = widgets.log_browser.font().family()
            widgets.log_browser.setStyleSheet(
                f"background-color: #333333; color: {name}; font-family: {current_font};"
            )

        def apply_height(value):
            widgets.log_browser.setFixedHeight(value)

        widgets.font_selector.currentFontChanged.connect(apply_font)
        widgets.color_selector.currentTextChanged.connect(apply_color)
        widgets.height_slider.valueChanged.connect(apply_height)

        # Apply initial settings
        apply_color("white")

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE (Scraping)
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW SETTINGS PAGE
        if btnName == "btn_save":
            widgets.stackedWidget.setCurrentWidget(widgets.settings_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    def run_scraper(self):
        url = widgets.lineEdit_url.text().strip()
        selector = widgets.lineEdit_selector.text().strip()

        if not url:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir une URL valide.")
            return
        if not selector:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir un sélecteur CSS.")
            return

        try:
            # Logger envoyant les messages dans log_browser
            import logging
            import time
            from pathlib import Path

            class QTextEditLogger(logging.Handler):
                def __init__(self, text_edit):
                    super().__init__()
                    self.text_edit = text_edit

                def emit(self, record):
                    msg = self.format(record)
                    self.text_edit.append(msg)

            logger = logging.getLogger("ScrapingLogger")
            logger.setLevel(logging.INFO)
            logger.handlers.clear()

            log_handler = QTextEditLogger(widgets.log_browser)
            log_handler.setFormatter(logging.Formatter("%(message)s"))
            logger.addHandler(log_handler)

            before = len(list(Path("images").glob("*")))
            start = time.time()

            import scrape_images
            scrape_images.scrape_images(url, selector=selector, logger=logger)

            elapsed = time.time() - start
            after = len(list(Path("images").glob("*")))
            downloaded = max(0, after - before)
            logger.info("\U0001F5BC %d images téléchargées", downloaded)
            logger.info("Durée : %.2fs", elapsed)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du scraping : {e}")

    def reset_fields(self):
        widgets.lineEdit_url.clear()
        widgets.lineEdit_selector.clear()
        widgets.log_browser.clear()

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
