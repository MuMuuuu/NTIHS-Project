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

        self.comboBox = QtWidgets.QComboBox(main_window)
        self.comboBox.setGeometry(QtCore.QRect(10, 20, 111, 20))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")

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


class new_qt(QtWidgets.QMainWindow, UI_main_window):
    def __init__(self, device):
        QtWidgets.QMainWindow.__init__(self)
        UI_main_window.__init__(self)
        self.setupUi(self, device)
