
from PyQt5 import QtWidgets, QtCore
from re import match, findall
from sys import exit, argv
from requests import get

status_to_text = {
    "0": {"en": "off", "tw": "開啟"},
    "1": {"en": "on", "tw": "關閉"}
}


class UI_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(300, 400)

        self.device_name = QtWidgets.QLabel(main_window)
        self.device_name.setGeometry(QtCore.QRect(10, 20, 110, 30))
        self.device_name.setObjectName("device_name")

        self.device_list = QtWidgets.QComboBox(main_window)
        self.device_list.setGeometry(QtCore.QRect(100, 20, 110, 30))
        self.device_list.setObjectName("device_list")
        self.device_list.currentTextChanged.connect(self.load_status)

        self.device_status = QtWidgets.QLabel(main_window)
        self.device_status.setGeometry(QtCore.QRect(10, 70, 110, 30))
        self.device_status.setObjectName("device_status")

        self.control_device = QtWidgets.QPushButton(main_window)
        self.control_device.setGeometry(QtCore.QRect(100, 70, 110, 30))
        self.control_device.setObjectName("control_device")
        self.control_device.clicked.connect(self.change_status)

        self.device_name_input_desc = QtWidgets.QLabel(main_window)
        self.device_name_input_desc.setGeometry(QtCore.QRect(10, 200, 110, 30))
        self.device_name_input_desc.setObjectName("device_name_input_desc")

        self.device_name_input = QtWidgets.QTextEdit(main_window)
        self.device_name_input.setGeometry(QtCore.QRect(100, 200, 110, 30))
        self.device_name_input.setObjectName("device_name_input")

        self.device_id_input_desc = QtWidgets.QLabel(main_window)
        self.device_id_input_desc.setGeometry(QtCore.QRect(10, 230, 110, 30))
        self.device_id_input_desc.setObjectName("device_id_input_desc")

        self.device_id_input = QtWidgets.QTextEdit(main_window)
        self.device_id_input.setGeometry(QtCore.QRect(100, 230, 110, 30))
        self.device_id_input.setObjectName("device_id_input")

        self.add_device = QtWidgets.QPushButton(main_window)
        self.add_device.setGeometry(QtCore.QRect(100, 280, 110, 30))
        self.add_device.setObjectName("add_device")
        self.add_device.clicked.connect(
            lambda:
                self.add_device_into_list(
                    self.device_name_input.toPlainText(),
                    self.device_id_input.toPlainText()
                )
        )

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        text_trans = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(text_trans("", "凱達格蘭赤腳IOT控制委員會"))
        self.add_device.setText(text_trans("", "新增裝置"))
        self.device_name.setText(text_trans("", "裝置名稱"))
        self.control_device.setText(text_trans("", "狀態未讀取"))
        self.device_status.setText(text_trans("", "狀態未讀取"))
        self.device_name_input_desc.setText(text_trans("", "輸入裝置名稱"))
        self.device_id_input_desc.setText(text_trans("", "輸入裝置代碼"))

    def load_status(self):

        device_raw = self.device_list.currentText()
        self.device_id = "".join(findall("[0-9]", device_raw.split("(")[1]))

        req_data = data_set('A7K04JUMTJAAKR7B', "read_field", self.device_id)
        req_data.channel_id = '1161366'
        result = send_request(req_data)

        if(match("Illegal", result)):
            QtWidgets.QMessageBox.information(self, "生番", result)
        else:
            text_trans = QtCore.QCoreApplication.translate
            self.control_device.setText(
                text_trans("", f"{status_to_text[result]['tw']}裝置")
            )
            self.device_status.setText(
                text_trans("", f"裝置狀態：{status_to_text[result]['en']}")
            )
            return result

    def change_status(self):

        current_status = self.load_status()

        req_data = data_set('BPP9MWS1MN6JMAJN', "write", self.device_id)
        req_data.data = not current_status
        result = send_request(req_data)

        self.load_status()

    def add_device_into_list(self, device_name, device_id):
        for index in range(0, self.device_list.count()):

            device_raw = self.device_list.itemText(index)
            device_name_str = device_raw.split("(")[0]
            device_id_str = "".join(findall("[0-9]", device_raw.split("(")[1]))

            if device_name_str == device_name:
                QtWidgets.QMessageBox.information(self, "蛤", "名稱重複了啦")
                return False
            elif device_id_str == device_id:
                QtWidgets.QMessageBox.information(self, "蛤", "代碼重複了啦")
                return False
            elif eval(device_id_str) > 4:
                QtWidgets.QMessageBox.information(self, "對，很破", "目前不支援4以上的代碼")
                return False

        if not filter(device_name):
            QtWidgets.QMessageBox.information(self, "蛤", "打錯了啦")
            return False
        else:
            self.device_list.addItem(f"{device_name}({device_id})")
            QtWidgets.QMessageBox.information(self, "Noice", "已成功新增裝置")


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
        "read_field": f"{raw_url}/channels/{channel_id}/fields/{field}.json?api_key={api_key}&results=1",
        "read_feed": f"{raw_url}/channels/{channel_id}/feeds.json?api_key={api_key}&results=1",
        "write": f"{raw_url}/update?api_key={api_key}&field{field}={data}"
    }

    if url[mode] == None:
        return "Illegal url"

    r = get(url[mode])

    if(mode == "write"):
        res = f"Response : Number {r} result"
    elif(mode == "read_field"):
        res = f"{r.json()['feeds'][0][f'field{field}']}"

    if(r.status_code == 200):
        print("Connect \033[1;32;40m Success \033[0;37;40m !")
        return res
