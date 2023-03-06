import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QTextEdit, QPushButton, QTextBrowser, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import openai
from PyQt5 import QtGui, QtCore

conversation = [{"role": "system", "content": ""}]

class GPTWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, text, api_key):
        super(GPTWorker, self).__init__()
        self.text = text
        self.api_key = api_key

    def run(self):
        openai.api_key = self.api_key  # 使用MainWindow中的api_key变量
        prompt = self.text

        message = {"role": "user", "content": prompt};

        conversation.append(message)
        token_count = sum([len(msg["content"]) for msg in conversation])
        if token_count > 4096:
            conversation.clear()
            conversation.append(message)

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)
        conversation.append(response.choices[0].message)

        self.finished.emit(response.choices[0].message.content)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.api_key = "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"  # 设置默认值
        with open('api_key.txt') as f:
            self.api_key = f.read().strip()

        self.setGeometry(1400, 200, 432, 700)
        # self.setFixedSize(500, 700)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("ChatGPT")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # 创建垂直布局
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.vertical_layout.setContentsMargins(10, 50, 10, 10)
        self.vertical_layout.setSpacing(10)

        self.text_edit = QTextEdit(self.central_widget)
        self.text_edit.setFont(QtGui.QFont("微软雅黑", 12))
        self.text_edit.setPlaceholderText("在这里输入您的问题")
        self.text_edit.setWordWrapMode(True)
        self.text_edit.setFixedHeight(100)

        self.btn = QPushButton("发送", self.central_widget)
        self.btn.setFont(QtGui.QFont("微软雅黑", 12))
        self.btn.clicked.connect(self.btn_send_request)

        self.btn2 = QPushButton("连续发送", self.central_widget)
        self.btn2.setFont(QtGui.QFont("微软雅黑", 12))
        self.btn2.clicked.connect(self.btn_send_request2)


        self.translate_btn = QPushButton("trans", self.central_widget)
        self.translate_btn.setGeometry(10, 10, 60, 30)
        self.translate_btn.setFont(QtGui.QFont("微软雅黑", 12))
        self.translate_btn.clicked.connect(self.translate_text)

        self.polish_btn = QPushButton("poli", self.central_widget)
        self.polish_btn.setGeometry(80, 10, 60, 30)
        self.polish_btn.setFont(QtGui.QFont("微软雅黑", 12))
        self.polish_btn.clicked.connect(self.polish_text)

        self.clear_btn = QPushButton("clear", self.central_widget)
        self.clear_btn.setGeometry(150, 10, 60, 30)
        self.clear_btn.setFont(QtGui.QFont("微软雅黑", 12))
        self.clear_btn.clicked.connect(self.clear_text)


        self.response_browser = QTextBrowser(self.central_widget)
        self.response_browser.setStyleSheet("font-size: 16px")
        self.response_browser.setFont(QtGui.QFont("微软雅黑", 18))
        self.response_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.response_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.response_browser.setPlaceholderText("等待回复中...")
        self.response_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.response_browser.setFrameShape(QTextBrowser.NoFrame)

        # 将控件添加到垂直布局中

        self.vertical_layout.addWidget(self.text_edit)
        self.vertical_layout.addWidget(self.btn)
        self.vertical_layout.addWidget(self.btn2)
        self.vertical_layout.addWidget(self.response_browser)

        self.worker = None



    def show_response(self, response):
        self.response_browser.setPlainText(response.strip())

    def send_request(self, prompt):
        cursor = self.text_edit.textCursor()  # 获取当前文本光标对象
        cursor.movePosition(QtGui.QTextCursor.Start)  # 将光标移动到文本开头
        self.text_edit.setTextCursor(cursor)  # 将文本光标设置到移动后的位置
        self.text_edit.insertPlainText(prompt)  # 在光标位置插入文本

        text = self.text_edit.toPlainText().strip()
        if not text:
            return

        self.worker = GPTWorker(text, self.api_key)
        self.worker.finished.connect(self.show_response)
        self.worker.start()

        # 显示等待提示
        self.response_browser.setPlainText("等待回复中...")

    def btn_send_request(self):
        conversation.clear()
        self.send_request("")

    def btn_send_request2(self):
        self.send_request("")


    def translate_text(self):
        self.send_request("Translate the following text into Chinese：")

    def polish_text(self):
        self.send_request("Please help me polish the following statements: ")

    def clear_text(self):
        self.text_edit.clear()

    def closeEvent(self, event):
        # 停止并等待线程
        if self.worker and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()

        event.accept()

    def closeEvent(self, event):
        # 关闭窗口
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
