from PyQt5 import QtWidgets, QtCore
from re import match, findall
from sys import exit, argv
from requests import get
from time import sleep

text_trans = QtCore.QCoreApplication.translate
status_to_text = {0: {"en": "off", "tw": "開啟"}, 1: {"en": "on", "tw": "關閉"}}


class data_receiver(QtCore.QThread):
    def __init__(self):
        super(data_receiver, self).__init__()

    def run(self, window, original_data, breaklimit):
        while int(window.load_status()) == original_data:
            if breaklimit == 0:
                return None
            else:
                breaklimit -= 1
                sleep(5)
        return True


class UI_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(400, 400)

        self.device_id = None

        self.device_name = QtWidgets.QLabel(main_window)
        self.device_name.setGeometry(QtCore.QRect(10, 20, 110, 30))

        self.device_list = QtWidgets.QComboBox(main_window)
        self.device_list.setGeometry(QtCore.QRect(100, 20, 110, 30))
        self.device_list.currentTextChanged.connect(self.load_status)

        self.device_status = QtWidgets.QLabel(main_window)
        self.device_status.setGeometry(QtCore.QRect(10, 70, 110, 30))

        self.control_device = QtWidgets.QPushButton(main_window)
        self.control_device.setGeometry(QtCore.QRect(100, 70, 110, 30))

        self.name_input_desc = QtWidgets.QLabel(main_window)
        self.name_input_desc.setGeometry(QtCore.QRect(10, 200, 110, 30))

        self.name_input = QtWidgets.QTextEdit(main_window)
        self.name_input.setGeometry(QtCore.QRect(100, 200, 110, 30))
        self.name_input.textChanged.connect(
          lambda:
                self.check_str(
                    self.name_input.toPlainText(),
                    self.id_input.toPlainText()
                )
        )

        self.id_input_desc = QtWidgets.QLabel(main_window)
        self.id_input_desc.setGeometry(QtCore.QRect(10, 230, 110, 30))

        self.id_input = QtWidgets.QTextEdit(main_window)
        self.id_input.setGeometry(QtCore.QRect(100, 230, 110, 30))
        self.id_input.textChanged.connect(
          lambda:
                self.check_str(
                    self.name_input.toPlainText(),
                    self.id_input.toPlainText()
                )
        )

        self.add_device = QtWidgets.QPushButton(main_window)
        self.add_device.setGeometry(QtCore.QRect(100, 280, 110, 30))
        self.add_device.clicked.connect(
            lambda:
                self.add_device_into_list(
                    self.name_input.toPlainText(),
                    self.id_input.toPlainText()
                )
        )

        self.name_err_tip = QtWidgets.QLabel(main_window)
        self.name_err_tip.setGeometry(QtCore.QRect(220, 200, 220, 30))
        self.name_err_tip.setStyleSheet('color:red')

        self.id_err_tip = QtWidgets.QLabel(main_window)
        self.id_err_tip.setGeometry(QtCore.QRect(220, 230, 220, 30))
        self.id_err_tip.setStyleSheet('color:red')

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(text_trans("", "凱達格蘭赤腳IOT控制委員會"))
        self.add_device.setText(text_trans("", "新增裝置"))
        self.device_name.setText(text_trans("", "裝置名稱"))
        self.name_input_desc.setText(text_trans("", "輸入裝置名稱"))
        self.id_input_desc.setText(text_trans("", "輸入裝置代碼"))

    def check_str(self, device_name, device_id):

        try:
            device_id = eval(device_id)
        except:
            pass

        self.add_device.setDisabled(1)

        if (not filter(device_name)):
            self.name_err_tip.setText(text_trans("", "Not Match Format"))
        else:
            self.name_err_tip.clear()

        if device_id == "":
            self.id_err_tip.setText(text_trans("", "Not Match Format"))
        elif not (type(device_id) == int and device_id >= 1):
            self.id_err_tip.setText(
                text_trans("", "Positive Integer Required"))
        elif not (4 >= device_id):
            self.id_err_tip.setText(text_trans("", "Number Can Not Exceed 4"))
        else:
            self.id_err_tip.clear()

        if self.name_err_tip.text() == self.id_err_tip.text() == "":
            self.add_device.setEnabled(1)

    def load_status(self):

        device_raw = self.device_list.currentText()
        self.device_id = "".join(findall("[0-9]", device_raw.split("(")[1]))

        req_data = data_set('A7K04JUMTJAAKR7B', "read_field", self.device_id)
        req_data.channel_id = '1161366'
        result = send_request(req_data)

        self.control_device.disconnect()
        if match("Illegal", str(result)):
            QtWidgets.QMessageBox.critical(self, "Failed", result)
            self.device_status.setText(text_trans("", "裝置狀態讀取錯誤"))
            self.control_device.setText(text_trans("", "讀取狀態"))
            self.control_device.clicked.connect(self.load_status)
            return 0
        else:
            self.device_status.setText(
                text_trans("", f"裝置狀態：{status_to_text[int(result)]['en']}"))
            self.control_device.setText(
                text_trans("", f"{status_to_text[int(result)]['tw']}裝置"))
            self.control_device.clicked.connect(self.change_status)
            return result

    def change_status(self):

        current_status = int(self.load_status())

        req_data = data_set('BPP9MWS1MN6JMAJN', "write", self.device_id)
        req_data.data = int(not current_status)
        send_request(req_data)

        receiver = data_receiver()
        result = receiver.run(self, current_status, 15)

        if result == None:
            QtWidgets.QMessageBox.warning(self, "Failed", "資料爆炸")
        else:
            QtWidgets.QMessageBox.information(self, "Success", "資料更改成功")
            self.load_status()

    def add_device_into_list(self, device_name, device_id):
        for index in range(0, self.device_list.count()):

            device_raw = self.device_list.itemText(index)
            device_name_str = device_raw.split("(")[0]
            device_id_str = "".join(findall("[0-9]", device_raw.split("(")[1]))

            if device_name_str == device_name:
                QtWidgets.QMessageBox.warning(self, "Damn", "Repeated Name")
                self.clear_input()
                return False
            elif device_id_str == device_id:
                QtWidgets.QMessageBox.warning(self, "Damn", "Repeated Id")
                self.clear_input()
                return False

        self.device_list.addItem(f"{device_name}({device_id})")
        self.clear_input()
        QtWidgets.QMessageBox.information(self, "Noice","Success To Add New Device")

    def clear_input(self):
        self.name_input.clear()
        self.id_input.clear()
        self.name_err_tip.clear()
        self.id_err_tip.clear()


class new_qt(QtWidgets.QMainWindow, UI_main_window):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        UI_main_window.__init__(self)
        self.setupUi(self)


class data_set():
    def __init__(self, api_key, mode, field=1, data=None, channel_id=None):
        self.api_key = api_key
        self.field = field
        self.data = data
        self.channel_id = channel_id
        self.mode = mode


def filter(string):
    try:
        assert type(string) == str
    except:
        return None

    if not match("[A-Za-z0-9]{4,16}", string):
        return False
    else:
        return True


def setup_window():
    app = QtWidgets.QApplication(argv)
    window = new_qt()
    window.show()
    exit(app.exec_())


def send_request(req_data):

    api_key = req_data.api_key
    if api_key == None:
        return "Illegal api_key"

    mode = req_data.mode
    if mode == None:
        return "Illegal mode"

    field = req_data.field
    data = req_data.data
    channel_id = req_data.channel_id

    raw_url = "https://api.thingspeak.com"
    url = {
        "read_field":
        f"{raw_url}/channels/{channel_id}/fields/{field}.json?api_key={api_key}&results=1",
        "read_feed":
        f"{raw_url}/channels/{channel_id}/feeds.json?api_key={api_key}&results=1",
        "write":
        f"{raw_url}/update?api_key={api_key}&field{field}={data}"
    }

    if url[mode] == None:
        return "Illegal url"

    r = get(url[mode])

    if (mode == "write"):
        res = f"Number {r.json()}"
        if res == 0:
            sleep(5)
            send_request(req_data)
        else:
            print(f"write result = send {data} : {res}")
    elif (mode == "read_field"):
        res = ""
        res_temp = r.json()['feeds']

        if res_temp == None:
            return "Illegal Feed"
        else:
            res = res_temp[0][f'field{field}']

        if res == None:
            return "Illegal Result Type"
        else:
            print(f"load result = field{field} : {res}")

    if (r.status_code == 200):
        print("Connect \033[1;32;40m Success \033[0;37;40m !")
        return res
