import sys
from request import request
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QLineEdit, QScrollArea, QTextBrowser

app = QApplication()

class PageLabel(QScrollArea):
    def __init__(self):
        super().__init__()

        content = QWidget()
        self.setWidget(content)

        layout = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def setText(self, text):
        self.label.setText(text)

class Browser(QWidget):
    def __init__(self):
        super().__init__()

        topbar = QHBoxLayout()
        back_history = QPushButton('<')
        forward_history = QPushButton('>')
        search_bar  = QLineEdit()
        topbar.addWidget(back_history); topbar.addWidget(forward_history); topbar.addWidget(search_bar)
        topbar_widget = QWidget()
        topbar_widget.setLayout(topbar)

        main_area = QScrollArea()
        headers, content = request('https://example.com')
        text_area = QTextBrowser()
        text_area.setHtml(content)
        # text_area.setTextInteractionFlags(Qt

        layout = QVBoxLayout()
        layout.addWidget(topbar_widget, 1)
        layout.addWidget(text_area, 10)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication

    browser = Browser()
    browser.resize(800, 600)
    browser.show()
    sys.exit(app.exec())
