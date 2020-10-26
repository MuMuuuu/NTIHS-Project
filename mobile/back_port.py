from PyQt5 import QtWidgets, QtCore
from re import match, findall
from sys import exit, argv
from requests import get
from time import sleep

text_trans = QtCore.QCoreApplication.translate
status_to_text = {
    0: {
        "en": "Off",
        "display": "Turn On"
    },
    1: {
        "en": "On",
        "display": "Turn Off "
    }
}


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
        main_window.resize(500, 400)

        self.device_id = None

        self.device_name = QtWidgets.QLabel(main_window)
        self.device_name.setGeometry(QtCore.QRect(70, 20, 110, 30))

        self.device_list = QtWidgets.QComboBox(main_window)
        self.device_list.setGeometry(QtCore.QRect(190, 20, 150, 30))
        self.device_list.setEditable(True)
        self.device_list.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.device_list.lineEdit().setReadOnly(True)
        self.device_list.currentTextChanged.connect(self.load_status)

        self.device_status = QtWidgets.QLabel(main_window)
        self.device_status.setGeometry(QtCore.QRect(70, 70, 110, 30))

        self.control_device = QtWidgets.QPushButton(main_window)
        self.control_device.setGeometry(QtCore.QRect(190, 70, 150, 30))

        self.name_input_desc = QtWidgets.QLabel(main_window)
        self.name_input_desc.setGeometry(QtCore.QRect(70, 200, 150, 30))

        self.name_input = QtWidgets.QTextEdit(main_window)
        self.name_input.setGeometry(QtCore.QRect(190, 200, 150, 30))
        self.name_input.textChanged.connect(
            lambda:
                self.check_str(
                    self.name_input.toPlainText(),
                    self.id_input.toPlainText()
                )
        )

        self.id_input_desc = QtWidgets.QLabel(main_window)
        self.id_input_desc.setGeometry(QtCore.QRect(70, 230, 150, 30))

        self.id_input = QtWidgets.QTextEdit(main_window)
        self.id_input.setGeometry(QtCore.QRect(190, 230, 150, 30))
        self.id_input.textChanged.connect(
            lambda:
                self.check_str(
                    self.name_input.toPlainText(),
                    self.id_input.toPlainText()
                )
        )

        self.add_device = QtWidgets.QPushButton(main_window)
        self.add_device.setGeometry(QtCore.QRect(190, 280, 150, 30))
        self.add_device.clicked.connect(
            lambda:
                self.add_device_into_list(
                    self.name_input.toPlainText(),
                    self.id_input.toPlainText()
                )
        )

        self.name_err_tip = QtWidgets.QLabel(main_window)
        self.name_err_tip.setGeometry(QtCore.QRect(345, 200, 220, 30))
        self.name_err_tip.setStyleSheet('color:red')

        self.id_err_tip = QtWidgets.QLabel(main_window)
        self.id_err_tip.setGeometry(QtCore.QRect(345, 230, 220, 30))
        self.id_err_tip.setStyleSheet('color:red')

        self.add_device.setDisabled(1)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(text_trans("", "Ketagalan Barefoot IOT Control Commission"))
        self.add_device.setText(text_trans("", "New Device"))
        self.device_name.setText(text_trans("", "Device Name"))
        self.control_device.setText(text_trans("", "Status Not Loaded"))
        self.device_status.setText(text_trans("", "Status Not Loaded"))
        self.name_input_desc.setText(text_trans("", "Input Device Name"))
        self.id_input_desc.setText(text_trans("", "Input Device Id"))

    def check_str(self, device_name, device_id):

        self.name_err_tip.setText(text_trans("", name_filter(device_name)))
        self.id_err_tip.setText(text_trans("", id_filter(device_id)))

        if self.name_err_tip.text() == self.id_err_tip.text() == "":
            self.add_device.setEnabled(1)
        else:
            self.add_device.setDisabled(1)

    def load_status(self):

        device_raw = self.device_list.currentText()
        self.device_id = "".join(findall("[0-9]", device_raw.split("(")[1]))

        req_data = data_set('A7K04JUMTJAAKR7B', "read_field", self.device_id)
        req_data.channel_id = '1161366'
        result = send_request(req_data)

        self.control_device.disconnect()
        if match("Illegal", str(result)):
            QtWidgets.QMessageBox.critical(self, "Failed", result)
            self.device_status.setText(text_trans("", "Status Error"))
            self.control_device.setText(text_trans("", "Load Status"))
            self.control_device.clicked.connect(self.load_status)
            return 0
        else:
            self.device_status.setText(text_trans("", f"Device Status {status_to_text[int(result)]['en']}"))
            self.control_device.setText(text_trans("",f"{status_to_text[int(result)]['display']} Device"))
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
            QtWidgets.QMessageBox.warning(self, "Failed", "Data Exploded")
        else:
            QtWidgets.QMessageBox.information(self, "Success","Data Changed Successfully")
            print("Connect \033[1;32;40m Success \033[0;37;40m !")

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


def name_filter(name):
    try:
        assert type(name) == str
    except:
        return ""

    if not match("^[A-Za-z0-9]{4,16}$", name):
        return "Not Match Format"
    else:
        return ""


def id_filter(id):
    try:
        id = eval(id)
    except:
        pass

    if id == "":
        return "Not Match Format"
    elif not (type(id) == int and id >= 1):
        return "Positive Integer Required"
    elif not (4 >= id):
        return "Number Can Not Exceed 4"
    else:
        return ""


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
        "read_field":f"{raw_url}/channels/{channel_id}/fields/{field}.json?api_key={api_key}&results=1",
        "read_feed":f"{raw_url}/channels/{channel_id}/feeds.json?api_key={api_key}&results=1",
        "write":f"{raw_url}/update?api_key={api_key}&field{field}={data}"
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
        return res
