from PyQt5 import QtWidgets, QtCore
from re import match, findall
from sys import exit, argv
from time import sleep
from queue import Queue
import paho.mqtt.client as mqtt


class UI_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(500, 400)

        self.device_id = None
        self.client = mqtt_client(self.device_id)
        self.server_ip = "219.68.154.148"
        self.port = 1883
        self.text_trans = QtCore.QCoreApplication.translate
        self.status_to_text = {
            0: {
                "en": "Off",
                "display": "Turn On"
            },
            1: {
                "en": "On",
                "display": "Turn Off "
            }
        }

        self.device_name = QtWidgets.QLabel(main_window)
        self.device_name.setGeometry(QtCore.QRect(70, 20, 110, 30))

        self.device_list = QtWidgets.QComboBox(main_window)
        self.device_list.setGeometry(QtCore.QRect(190, 20, 150, 30))
        self.device_list.setEditable(True)
        self.device_list.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.device_list.lineEdit().setReadOnly(True)
        self.device_list.currentTextChanged.connect(self.linking)

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
        main_window.setWindowTitle(self.text_trans(
            "", "Ketagalan Barefoot IOT Control Commission"))
        self.add_device.setText(self.text_trans("", "New Device"))
        self.device_name.setText(self.text_trans("", "Device Name"))
        self.control_device.setText(self.text_trans("", "Status Not Loaded"))
        self.device_status.setText(self.text_trans("", "Status Not Loaded"))
        self.name_input_desc.setText(self.text_trans("", "Input Device Name"))
        self.id_input_desc.setText(self.text_trans("", "Input Device Id"))

    def check_str(self, device_name, device_id):

        self.name_err_tip.setText(
            self.text_trans("", name_filter(device_name)))
        self.id_err_tip.setText(self.text_trans("", id_filter(device_id)))

        if self.name_err_tip.text() == self.id_err_tip.text() == "":
            self.add_device.setEnabled(1)
        else:
            self.add_device.setDisabled(1)

    def linking(self):

        self.client.loop_stop()

        device_raw = self.device_list.currentText()
        self.device_id = "".join(findall("[0-9]", device_raw.split("(")[1]))

        self.client.current_listening = f"{self.device_id}_feedback"

        self.client.connect(self.server_ip, self.port, 30)
        self.client.loop_start()

        self.client.subscribe(f"{self.device_id}_feedback")

        result = int(self.client.res_temp.get())

        print(f"Now {result}")

        self.set_control_button(result)

    def change_status(self):

        current_status = int(self.client.res_temp.get())

        self.client.publish(f"{self.device_id}_writein",
                            int(not current_status))

        print(f"original {current_status}")

        result = None
        breaklimit = 15
        while int(self.client.res_temp.get()) == current_status:
            if breaklimit == 0:
                break
            print(f"whatnow {self.client.res_temp.get()}")
            breaklimit -= 1
            sleep(0.5)

        if breaklimit != 0:
            result = int(self.client.res_temp.get())

        if result == None:
            self.set_control_button("Illegal")
            QtWidgets.QMessageBox.warning(self, "Failed", "Data Exploded")
        else:
            self.set_control_button(result)
            QtWidgets.QMessageBox.information(
                self, "Success", "Data Changed Successfully")
            print("Connect \033[1;32;40m Success \033[0;37;40m !")

    def set_control_button(self, result):
        self.control_device.disconnect()
        if match("Illegal", str(result)):
            QtWidgets.QMessageBox.critical(self, "Failed", result)
            self.device_status.setText(self.text_trans("", "Status Error"))
            self.control_device.setText(self.text_trans("", "Load Status"))
            self.control_device.clicked.connect(self.linking)
        else:
            self.device_status.setText(self.text_trans(
                "", f"Device Status {self.status_to_text[int(result)]['en']}"))
            self.control_device.setText(self.text_trans(
                "", f"{self.status_to_text[int(result)]['display']} Device"))
            self.control_device.clicked.connect(self.change_status)

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
        QtWidgets.QMessageBox.information(
            self, "Noice", "Success To Add New Device")

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


class mqtt_client(mqtt.Client):
    def on_connect_callback(self, client, userdata, flags, rc):
        print(f"Connected：{rc}")

    def on_message_callback(self, client, userdata, message):
        if self.current_listening == message.topic:
            msg = message.payload.decode("utf-8")
            print(f"Received：{msg}")
            self.res_temp.put(msg)

    def on_publish_callback(self, client, userdata, mid):
        print(f"Published：{mid}")

    def on_subscribe_callback(self, client, userdata, mid, granted_qos):
        print(f"Subscribed：{mid}")

    def __init__(self, id):
        mqtt.Client.__init__(self)
        self.current_listening = f"{id}_feedback"
        self.res_temp = Queue()
        self.on_connect = self.on_connect_callback
        self.on_message = self.on_message_callback
        self.on_publish = self.on_publish_callback
        self.on_subscribe = self.on_subscribe_callback


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


if __name__ == "__main__":
    setup_window()
