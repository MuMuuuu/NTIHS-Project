from PyQt5 import QtWidgets, QtCore, QtGui


class data_set():
    def __init__(self, api_key, mode, field=1, data=None, channel_id=None):
        self.api_key = api_key
        self.field = field
        self.data = data
        self.channel_id = channel_id
        self.mode = mode


class device():
    def __init__(self, status):
        self.status = status.lower()
        if(status.lower() == "on"):
            self.action = "關閉"
        elif(status.lower() == "off"):
            self.action = "開啟"


class UI_main_window(object):
    def setupUi(self, main_window, device):
        main_window.setObjectName("main_window")
        main_window.resize(300, 150)

        self.device_list = QtWidgets.QComboBox(main_window)
        self.device_list.setGeometry(QtCore.QRect(10, 20, 111, 20))
        self.device_list.setEditable(True)
        self.device_list.setObjectName("device_list")

        self.control_device = QtWidgets.QPushButton(main_window)
        self.control_device.setGeometry(QtCore.QRect(140, 70, 71, 31))
        self.control_device.setObjectName("control_device")
        self.control_device.clicked.connect(
            lambda:
                self.load_status(
                    self.control_device
                )
        )

        self.device_status = QtWidgets.QLabel(main_window)
        self.device_status.setGeometry(QtCore.QRect(10, 70, 111, 31))
        self.device_status.setObjectName("device_status")

        self.add_device = QtWidgets.QPushButton(main_window)
        self.add_device.setGeometry(QtCore.QRect(140, 20, 75, 23))
        self.add_device.setObjectName("add_device")
        self.add_device.clicked.connect(
            lambda:
                self.add_device_into_list(
                    self.device_list.currentText()
                )
        )

        self.retranslateUi(main_window, device)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window, device):
        text_trans = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(text_trans("", "凱達格蘭赤腳IOT控制委員會"))
        self.control_device.setText(text_trans("", f"{device.action}裝置"))
        self.device_status.setText(text_trans("", f"裝置狀態：{device.status}"))
        self.add_device.setText(text_trans("", "新增裝置"))

    def load_status(self, device):
        if("開啟" in device.text()):
            text_trans = QtCore.QCoreApplication.translate
            device.setText(text_trans("", "關閉裝置"))
            self.device_status.setText(text_trans("", "裝置狀態：on"))
        else:
            text_trans = QtCore.QCoreApplication.translate
            device.setText(text_trans("", "開啟裝置"))
            self.device_status.setText(text_trans("", "裝置狀態：off"))

    def add_device_into_list(self, device_name):
        for index in range(1, self.device_list.count()):
            if self.device_list.itemText(index) == device_name:
                QtWidgets.QMessageBox.information(self, "蛤", "重複了啦")
                return
        self.device_list.addItem(device_name)
        QtWidgets.QMessageBox.information(self, "Noise", "已成功新增裝置")


class new_qt(QtWidgets.QMainWindow, UI_main_window):
    def __init__(self, device):
        QtWidgets.QMainWindow.__init__(self)
        UI_main_window.__init__(self)
        self.setupUi(self, device)
