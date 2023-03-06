# ChatGPT代码说明文件

## 简介

ChatGPT是使用GPT模型实现的聊天机器人的应用程序，可以与用户进行自然对话。本程序是基于Python的PyQt5库构建。

## 模块

### PyQt5

PyQt5库是基于C++的Qt库的Python绑定，提供了丰富的方法和控件，使得开发GUI应用程序更加容易。在我们的应用程序中，我们主要使用了QMainWindow、QWidget、QLineEdit、QTextEdit、QPushButton、QTextBrowser、QVBoxLayout、QHBoxLayout等控件，以及QtCore的QThread、pyqtSignal、Qt等模块。

### openai

openai是目前公认的自然语言处理技术公司之一，它提供了许多先进的自然语言处理API服务。在本程序中，我们主要使用了openai提供的ChatCompletion API服务，通过向API发送请求，从而获得回答。

## 功能

ChatGPT程序提供以下功能：

- 用户输入文本，程序返回对应回答；
- 点击trans按钮，程序提供将以下文本翻译成中文的功能；
- 点击poli按钮，程序提供对以下文本进行修改的功能；
- 点击clear按钮，程序清空聊天记录；
- 点击发送按钮，程序开始自动聊天；
- 点击连续发送按钮，程序会继续进行聊天。

## 使用说明

1. 在api_key.txt文件中输入从openai获取的api。

## 总结

ChatGPT程序是一个主要基于PyQt5库和openai API的聊天机器人应用程序。通过使用GPT模型，程序可以与用户进行自然对话，提供了实现数据处理和用户操作的实际例子。旨在克服ChatGPT使用过程中频繁碰到的拒绝访问问题。
