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



        # Bouton pour lancer le scraping depuis la nouvelle page
        widgets.btn_launch_scraping.clicked.connect(self.run_scraper)

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
        widgets.label.setText("Scraping Image")
        widgets.log_browser.setFixedHeight(200)
        widgets.log_browser.setStyleSheet(
            "background-color: #333333; color: #dddddd; font-family: Consolas, Courier;"
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
            # On crée un logger temporaire qui envoie les messages dans log_browser
            import logging

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

            # On appelle le moteur avec les champs dynamiques
            import scrape_images
            scrape_images.scrape_images(url, selector=selector, logger=logger)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du scraping : {e}")

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
