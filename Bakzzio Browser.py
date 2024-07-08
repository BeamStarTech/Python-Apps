import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QPushButton, QLineEdit, QSizePolicy, QAction, QToolBar, QStyle, QMenu, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser_tabs = QTabWidget()
        self.browser_tabs.setTabsClosable(True)
        self.browser_tabs.tabCloseRequested.connect(self.close_tab)

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL and press Enter")
        self.url_input.returnPressed.connect(self.load_url)

        self.add_tab_button = QPushButton("New Tab")
        self.add_tab_button.clicked.connect(self.add_new_tab)

        self.central_layout.addWidget(self.url_input)
        self.central_layout.addWidget(self.add_tab_button)
        self.central_layout.addWidget(self.browser_tabs)

        self.setCentralWidget(self.central_widget)

        self.setWindowTitle("Bakzzio")
        self.setGeometry(100, 100, 800, 600)

        self.init_toolbar()
        self.add_new_tab()

    def init_toolbar(self):
        self.nav_toolbar = QToolBar()
        self.addToolBar(self.nav_toolbar)

        home_action = QAction("Home", self)
        home_action.triggered.connect(self.navigate_home)
        self.nav_toolbar.addAction(home_action)

        back_action = QAction("Back", self)
        back_action.triggered.connect(self.navigate_back)
        self.nav_toolbar.addAction(back_action)

        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(self.navigate_forward)
        self.nav_toolbar.addAction(forward_action)

        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(self.reload_page)
        self.nav_toolbar.addAction(reload_action)

        # Theme toggle button
        self.theme_action = QAction("Toggle Theme", self)
        self.theme_action.triggered.connect(self.toggle_theme)
        self.theme_action.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMenuButton))
        self.nav_toolbar.addAction(self.theme_action)

        # Initialize with a light theme
        self.is_dark_theme = False

    def toggle_theme(self):
        # Toggle between light and dark themes
        self.is_dark_theme = not self.is_dark_theme

        # You can customize the theme colors here
        if self.is_dark_theme:
            # Dark theme colors
            self.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF;")
        else:
            # Light theme colors
            self.setStyleSheet("background-color: #FFFFFF; color: #000000;")

    def add_new_tab(self):
        browser = QWebEngineView()
        browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        browser.setMinimumSize(800, 600)
        browser.urlChanged.connect(self.update_urlbar)
        browser.loadFinished.connect(self.hide_progress)
        
        # Add a download requested signal handler
        browser.page().profile().downloadRequested.connect(self.handle_download)

        tab_index = self.browser_tabs.addTab(browser, "Loading...")
        self.browser_tabs.setCurrentIndex(tab_index)

        browser.load(QUrl("http://www.google.com"))

    def close_tab(self, index):
        self.browser_tabs.removeTab(index)

    def load_url(self):
        current_tab_index = self.browser_tabs.currentIndex()
        current_browser = self.browser_tabs.widget(current_tab_index)
        url = self.url_input.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        current_browser.setUrl(QUrl(url))

    def navigate_home(self):
        current_tab_index = self.browser_tabs.currentIndex()
        current_browser = self.browser_tabs.widget(current_tab_index)
        current_browser.setUrl(QUrl("http://www.google.com"))

    def navigate_back(self):
        current_tab_index = self.browser_tabs.currentIndex()
        current_browser = self.browser_tabs.widget(current_tab_index)
        current_browser.back()

    def navigate_forward(self):
        current_tab_index = self.browser_tabs.currentIndex()
        current_browser = self.browser_tabs.widget(current_tab_index)
        current_browser.forward()

    def reload_page(self):
        current_tab_index = self.browser_tabs.currentIndex()
        current_browser = self.browser_tabs.widget(current_tab_index)
        current_browser.reload()

    def update_urlbar(self, q):
        current_tab_index = self.browser_tabs.currentIndex()
        self.url_input.setText(q.toString())

    def hide_progress(self):
        current_tab_index = self.browser_tabs.currentIndex()
        current_browser = self.browser_tabs.widget(current_tab_index)
        current_browser.page().runJavaScript("document.title", self.update_tab_title)

    def update_tab_title(self, result):
        current_tab_index = self.browser_tabs.currentIndex()
        self.browser_tabs.setTabText(current_tab_index, result)

    def handle_download(self, item):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", item.path(), options=options)
        if file_name:
            item.setPath(file_name)
            item.accept()

def main():
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
