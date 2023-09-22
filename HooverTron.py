import sys, serial, os

from PyQt5 import QtCore, QtGui, QtWidgets, QtSerialPort
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow ,QWidget ,QToolBar ,QHBoxLayout, QAction ,QStatusBar ,QLineEdit ,QPushButton ,QTextEdit , QVBoxLayout, QDateEdit
from PyQt5.QtCore import Qt , pyqtSignal
from PyQt5.QtSerialPort import QSerialPortInfo
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import csv
from csv import reader
# import pyi_splash #uncomment this line and execution in main when creating distributable with a splash screen

class AddComport(QMainWindow):

    porttnavn = pyqtSignal(str)

    def __init__(self, parent, menu):
        super().__init__(parent)

        menuComPort = menu.addMenu("COM Port")

        info_list = QSerialPortInfo()
        serial_list = info_list.availablePorts()
        serial_ports = [port.portName() for port in serial_list]
        if (len(serial_ports) > 0):
            antalporte = len(serial_ports)
            antal = 0
            while antal < antalporte:
                button_action = QAction(serial_ports[antal], self)
                txt = serial_ports[antal]
                portinfo = QSerialPortInfo(txt)
                buttoninfotxt = " No Info"
                if portinfo.hasProductIdentifier():
                    buttoninfotxt = ("Product Specification = " + str(portinfo.vendorIdentifier()))
                if portinfo.hasVendorIdentifier():
                    buttoninfotxt = buttoninfotxt + (" Manufacturer ID = " + str(portinfo.productIdentifier()))
                button_action = QAction(txt, self)
                button_action.setStatusTip(buttoninfotxt)
                button_action.triggered.connect(lambda checked, txt=txt: self.valgAfComportClick(txt))
                menuComPort.addAction(button_action)
                antal = antal + 1
        else:
            print("No COM Ports Found")

    def valgAfComportClick(self, port):
        arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
        arduino.close()

        self.porttnavn.emit(port)

    def closeEvent(self, event):
        self.close()


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):

        self.hsS1RForce = [0]
        self.hsS1LForce = [0]
        self.hsS2RForce = [0]
        self.hsS2LForce = [0]
        self.hsS3RForce = [0]
        self.hsS3RAverage = [0]
        self.hsS3LForce = [0]
        self.hsS2RAverage = [0]
        self.openFile = ''

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 900)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 900))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(1200, 900))
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1200, 850))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(1200, 850))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayoutWidget_7 = QtWidgets.QWidget(self.tab_3)
        self.horizontalLayoutWidget_7.setGeometry(QtCore.QRect(-1, -1, 1201, 831))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_12.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout_12.setSpacing(20)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setContentsMargins(0, -1, -1, -1)
        self.formLayout_7.setVerticalSpacing(20)
        self.formLayout_7.setObjectName("formLayout_7")
        self.nameLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        self.nameLabel.setObjectName("nameLabel")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nameLabel)
        self.nameLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameLineEdit)
        self.preferredNameLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        self.preferredNameLabel.setObjectName("preferredNameLabel")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.preferredNameLabel)
        self.preferredNameLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        self.preferredNameLineEdit.setObjectName("preferredNameLineEdit")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.preferredNameLineEdit)
        self.dateOfBirthLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        self.dateOfBirthLabel.setObjectName("dateOfBirthLabel")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.dateOfBirthLabel)
        self.dateOfBirthDateEdit = QtWidgets.QDateEdit(self.horizontalLayoutWidget_7)
        self.dateOfBirthDateEdit.setObjectName("dateOfBirthDateEdit")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.dateOfBirthDateEdit)
        self.sexLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        self.sexLabel.setObjectName("sexLabel")
        self.formLayout_7.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.sexLabel)
        self.sexLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        self.sexLineEdit.setObjectName("sexLineEdit")
        self.formLayout_7.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.sexLineEdit)
        self.dateOfVisitLabel_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        self.dateOfVisitLabel_2.setObjectName("dateOfVisitLabel_2")
        self.formLayout_7.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.dateOfVisitLabel_2)
        self.dateOfVisitDateEdit = QtWidgets.QDateEdit(self.horizontalLayoutWidget_7)
        self.dateOfVisitDateEdit.setObjectName("dateOfVisitDateEdit")
        self.formLayout_7.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.dateOfVisitDateEdit)
        self.reasonForVisitLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        self.reasonForVisitLabel.setObjectName("reasonForVisitLabel")
        self.formLayout_7.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.reasonForVisitLabel)
        self.reasonForVisitLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        self.reasonForVisitLineEdit.setObjectName("reasonForVisitLineEdit")
        self.formLayout_7.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.reasonForVisitLineEdit)
        self.notesLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        self.notesLabel.setObjectName("notesLabel")
        self.formLayout_7.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.notesLabel)
        self.notesLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        self.notesLineEdit.setObjectName("notesLineEdit")
        self.formLayout_7.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.notesLineEdit)
        self.horizontalLayout_12.addLayout(self.formLayout_7)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem)
        self.horizontalLayout_12.setStretch(0, 2)
        self.horizontalLayout_12.setStretch(1, 3)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tab.setFont(font)
        self.tab.setStyleSheet("")
        self.tab.setObjectName("tab")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab)
        self.tabWidget_2.setGeometry(QtCore.QRect(0, 0, 1200, 900))
        self.tabWidget_2.setMinimumSize(QtCore.QSize(1200, 900))
        self.tabWidget_2.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_2.setUsesScrollButtons(False)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setMinimumSize(QtCore.QSize(1200, 800))
        self.tab_4.setObjectName("tab_4")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.tab_4)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 1201, 801))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(200, 450))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images/infographic1.drawio.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(7)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, -1, -1, 20)
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        # adding pyqtgraph to the screen
        self.graphWidget_hs1 = pg.PlotWidget()
        self.graphWidget_hs1.setObjectName("graphWidget_hs1")
        self.graphWidget_hs1.setBackground('w')
        self.graphWidget_hs1.addLegend()
        self.graphWidget_hs1.setLabel('left', "<span style=\"color:gray;font-size:20px\">Force (N)</span>")
        self.graphWidget_hs1.setLabel('bottom', "<span style=\"color:gray;font-size:20px\">Time (deciseconds)</span>")
        pen = pg.mkPen(color=(255,0,0))
        self.hsS1RForceLine = self.graphWidget_hs1.plot(self.hsS1RForce, name = "Extension Sensor", pen=pen)
        pen = pg.mkPen(color=(0,0,255))
        self.hsS1LForceLine = self.graphWidget_hs1.plot(self.hsS1LForce, name = "Flexion Sensor", pen=pen)
        self.verticalLayout_4.addWidget(self.graphWidget_hs1)

        # setup push button for record and clear
        self.horizontalLayout_s1 = QtWidgets.QHBoxLayout()
        self.pushButton_2 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget,
            checkable=True,
            toggled=self.on_toggled
        )
        self.pushButton_2.setObjectName("pushButton_2")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.pushButton_2.setFont(font)
        self.horizontalLayout_s1.addWidget(self.pushButton_2)

        self.pushButton_21 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget,
            checkable=True,
            toggled=self.clear_data
        )
        self.pushButton_21.setObjectName("pushButton_21")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.pushButton_21.setFont(font)
        self.horizontalLayout_s1.addWidget(self.pushButton_21)

        self.verticalLayout_4.addLayout(self.horizontalLayout_s1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.horizontalLayout_3.setStretch(0, 3)
        self.horizontalLayout_3.setStretch(1, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line.setStyleSheet("")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_6.addWidget(self.label_4)
        self.textEdit = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_6.addWidget(self.textEdit)
        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(1, 6)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_7.addWidget(self.label_5)
        self.label_16 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_16.setFont(font)
        self.label_16.setWordWrap(True)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_7.addWidget(self.label_16)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setVerticalSpacing(25)
        self.formLayout.setObjectName("formLayout")
        self.extensionForceLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.extensionForceLabel.setObjectName("extensionForceLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.extensionForceLabel)
        self.extensionForceLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.extensionForceLineEdit.setObjectName("extensionForceLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.extensionForceLineEdit)
        self.flexionForceLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.flexionForceLabel.setObjectName("flexionForceLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.flexionForceLabel)
        self.flexionForceLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.flexionForceLineEdit.setObjectName("flexionForceLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.flexionForceLineEdit)
        self.verticalLayout_7.addLayout(self.formLayout)
        self.verticalLayout_7.setStretch(0, 1)
        self.verticalLayout_7.setStretch(1, 1)
        self.verticalLayout_7.setStretch(2, 5)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.horizontalLayout_4.setStretch(0, 3)
        self.horizontalLayout_4.setStretch(1, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.setStretch(0, 4)
        self.verticalLayout_2.setStretch(2, 3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 3)
        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.tab_5)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 1201, 801))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_5.setContentsMargins(19, 19, 21, 21)
        self.horizontalLayout_5.setSpacing(20)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(200, 450))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("images/infographic2.drawio.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(7)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(20)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setContentsMargins(-1, -1, -1, 20)
        self.verticalLayout_8.setSpacing(20)
        self.verticalLayout_8.setObjectName("verticalLayout_8")

        #adding in graph for the second hoover's sign step
        self.graphWidget_hs2 = pg.PlotWidget()
        self.graphWidget_hs2.setObjectName("graphWidget_hs2")
        self.graphWidget_hs2.setBackground('w')
        self.graphWidget_hs2.addLegend()
        self.graphWidget_hs2.setLabel('left', "<span style=\"color:gray;font-size:20px\">Force (N)</span>")
        self.graphWidget_hs2.setLabel('bottom', "<span style=\"color:gray;font-size:20px\">Time (deciseconds)</span>")
        pen = pg.mkPen(color=(255, 0, 0))
        self.hsS2RForceLine = self.graphWidget_hs2.plot(self.hsS2RForce, name="Extension Sensor", pen=pen)
        pen = pg.mkPen(color=(0,0,0))
        self.hsS2RAverageLine = self.graphWidget_hs2.plot(self.hsS2RAverage, name="Extension Force Average", pen=pen)
        self.verticalLayout_8.addWidget(self.graphWidget_hs2)

        self.horizontalLayout_s2 = QtWidgets.QHBoxLayout()
        self.pushButton_3 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_4,
            checkable=True,
            toggled=self.on_toggled
        )
        self.pushButton_3.setObjectName("pushButton_3")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.pushButton_3.setFont(font)
        self.horizontalLayout_s2.addWidget(self.pushButton_3)

        self.pushButton_31 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_4,
            checkable=True,
            toggled=self.clear_data
        )
        self.pushButton_31.setObjectName("pushButton_31")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.pushButton_31.setFont(font)
        self.horizontalLayout_s2.addWidget(self.pushButton_31)

        self.verticalLayout_8.addLayout(self.horizontalLayout_s2)
        self.horizontalLayout_6.addLayout(self.verticalLayout_8)
        self.horizontalLayout_6.setStretch(0, 3)
        self.horizontalLayout_6.setStretch(1, 2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.line_2 = QtWidgets.QFrame(self.horizontalLayoutWidget_4)
        self.line_2.setStyleSheet("")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(20)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_10.addWidget(self.label_10)
        self.textEdit_2 = QtWidgets.QTextEdit(self.horizontalLayoutWidget_4)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout_10.addWidget(self.textEdit_2)
        self.verticalLayout_10.setStretch(0, 1)
        self.verticalLayout_10.setStretch(1, 6)
        self.horizontalLayout_7.addLayout(self.verticalLayout_10)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_11 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_11.addWidget(self.label_11)
        self.label_17 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_11.addWidget(self.label_17)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setVerticalSpacing(25)
        self.formLayout_2.setObjectName("formLayout_2")
        self.strongLegAverageStrengthLabel_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.strongLegAverageStrengthLabel_2.setFont(font)
        self.strongLegAverageStrengthLabel_2.setObjectName("strongLegAverageStrengthLabel_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.strongLegAverageStrengthLabel_2)
        self.strongLegAverageStrengthLineEdit_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_4)
        self.strongLegAverageStrengthLineEdit_2.setObjectName("strongLegAverageStrengthLineEdit_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.strongLegAverageStrengthLineEdit_2)
        self.strongLegPeakStrengthLabel_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.strongLegPeakStrengthLabel_2.setFont(font)
        self.strongLegPeakStrengthLabel_2.setObjectName("strongLegPeakStrengthLabel_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.strongLegPeakStrengthLabel_2)
        self.strongLegPeakStrengthLineEdit_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_4)
        self.strongLegPeakStrengthLineEdit_2.setObjectName("strongLegPeakStrengthLineEdit_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.strongLegPeakStrengthLineEdit_2)
        self.verticalLayout_11.addLayout(self.formLayout_2)
        self.verticalLayout_11.setStretch(0, 1)
        self.verticalLayout_11.setStretch(1, 1)
        self.verticalLayout_11.setStretch(2, 5)
        self.horizontalLayout_7.addLayout(self.verticalLayout_11)
        self.horizontalLayout_7.setStretch(0, 3)
        self.horizontalLayout_7.setStretch(1, 2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.verticalLayout_3.setStretch(0, 4)
        self.verticalLayout_3.setStretch(2, 3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(1, 3)
        self.tabWidget_2.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.tab_6)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(0, 0, 1201, 801))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_8.setContentsMargins(19, 19, 21, 21)
        self.horizontalLayout_8.setSpacing(20)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(200, 450))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("images/infographic3.drawio.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_8.addWidget(self.label_3)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setSpacing(7)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(20)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setContentsMargins(-1, -1, -1, 20)
        self.verticalLayout_13.setSpacing(20)
        self.verticalLayout_13.setObjectName("verticalLayout_13")

        # graph for hoover's sign step 3. textedit data commented out
        self.graphWidget_hs3 = pg.PlotWidget()
        self.graphWidget_hs3.setObjectName("graphWidget_hs3")
        self.graphWidget_hs3.setBackground('w')
        self.graphWidget_hs3.addLegend()
        self.graphWidget_hs3.setLabel('left', "<span style=\"color:gray;font-size:20px\">Force (N)</span>")
        self.graphWidget_hs3.setLabel('bottom', "<span style=\"color:gray;font-size:20px\">Time (deciseconds)</span>")
        pen = pg.mkPen(color=(255, 0, 0))
        self.hsS3RForceLine = self.graphWidget_hs3.plot(self.hsS3RForce, name="Extension Sensor", pen=pen)
        pen = pg.mkPen(color=(0,0,0))
        self.hsS3RForceAverageLine = self.graphWidget_hs3.plot(self.hsS3RAverage, name = "Extension Force Average", pen=pen)
        pen = pg.mkPen(color=(0, 0, 255))
        self.hsS3LForceLine = self.graphWidget_hs3.plot(self.hsS3LForce, name="Flexion Sensor", pen=pen)
        self.verticalLayout_13.addWidget(self.graphWidget_hs3)

        self.horizontalLayout_s3 = QtWidgets.QHBoxLayout()
        self.pushButton_4 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_5,
            checkable=True,
            toggled=self.on_toggled
        )
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_s3.addWidget(self.pushButton_4)

        self.pushButton_41 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_5,
            checkable=True,
            toggled=self.clear_data
        )
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.pushButton_41.setFont(font)
        self.pushButton_41.setObjectName("pushButton_41")
        self.horizontalLayout_s3.addWidget(self.pushButton_41)

        self.verticalLayout_13.addLayout(self.horizontalLayout_s3)
        self.horizontalLayout_9.addLayout(self.verticalLayout_13)
        self.horizontalLayout_9.setStretch(0, 3)
        self.horizontalLayout_9.setStretch(1, 2)
        self.verticalLayout_12.addLayout(self.horizontalLayout_9)
        self.line_3 = QtWidgets.QFrame(self.horizontalLayoutWidget_5)
        self.line_3.setStyleSheet("")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_12.addWidget(self.line_3)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(20)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_14 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_15.addWidget(self.label_14)
        self.textEdit_6 = QtWidgets.QTextEdit(self.horizontalLayoutWidget_5)
        self.textEdit_6.setObjectName("textEdit_6")
        self.verticalLayout_15.addWidget(self.textEdit_6)
        self.verticalLayout_15.setStretch(0, 1)
        self.verticalLayout_15.setStretch(1, 6)
        self.horizontalLayout_10.addLayout(self.verticalLayout_15)
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_15 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_16.addWidget(self.label_15)
        self.label_18 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_18.setFont(font)
        self.label_18.setWordWrap(True)
        self.label_18.setObjectName("label_18")
        self.verticalLayout_16.addWidget(self.label_18)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setVerticalSpacing(25)
        self.formLayout_3.setObjectName("formLayout_3")
        self.strongLegAverageStrengthLabel_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.strongLegAverageStrengthLabel_3.setFont(font)
        self.strongLegAverageStrengthLabel_3.setWordWrap(True)
        self.strongLegAverageStrengthLabel_3.setObjectName("strongLegAverageStrengthLabel_3")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.strongLegAverageStrengthLabel_3)
        self.strongLegAverageStrengthLineEdit_3 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_5)
        self.strongLegAverageStrengthLineEdit_3.setObjectName("strongLegAverageStrengthLineEdit_3")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.strongLegAverageStrengthLineEdit_3)
        self.strongLegPeakStrengthLabel_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.strongLegPeakStrengthLabel_3.setFont(font)
        self.strongLegPeakStrengthLabel_3.setWordWrap(True)
        self.strongLegPeakStrengthLabel_3.setObjectName("strongLegPeakStrengthLabel_3")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.strongLegPeakStrengthLabel_3)
        self.strongLegPeakStrengthLineEdit_3 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_5)
        self.strongLegPeakStrengthLineEdit_3.setObjectName("strongLegPeakStrengthLineEdit_3")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.strongLegPeakStrengthLineEdit_3)
        self.verticalLayout_16.addLayout(self.formLayout_3)
        self.verticalLayout_16.setStretch(0, 1)
        self.verticalLayout_16.setStretch(1, 1)
        self.verticalLayout_16.setStretch(2, 5)
        self.horizontalLayout_10.addLayout(self.verticalLayout_16)
        self.horizontalLayout_10.setStretch(0, 3)
        self.horizontalLayout_10.setStretch(1, 2)
        self.verticalLayout_12.addLayout(self.horizontalLayout_10)
        self.verticalLayout_12.setStretch(0, 4)
        self.verticalLayout_12.setStretch(2, 3)
        self.horizontalLayout_8.addLayout(self.verticalLayout_12)
        self.horizontalLayout_8.setStretch(0, 2)
        self.horizontalLayout_8.setStretch(1, 3)
        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.horizontalLayoutWidget_6 = QtWidgets.QWidget(self.tab_7)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(-1, -1, 1191, 801))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_11.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout_11.setSpacing(20)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_19 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.verticalLayout.addWidget(self.label_19)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setVerticalSpacing(20)
        self.formLayout_4.setObjectName("formLayout_4")
        self.unaffectedLegFlexionLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        self.unaffectedLegFlexionLabel.setObjectName("unaffectedLegFlexionLabel")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.unaffectedLegFlexionLabel)
        self.unaffectedLegFlexionLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_6)
        self.unaffectedLegFlexionLineEdit.setReadOnly(True)
        self.unaffectedLegFlexionLineEdit.setObjectName("unaffectedLegFlexionLineEdit")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.unaffectedLegFlexionLineEdit)
        self.unaffectedLegExtensionLLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        self.unaffectedLegExtensionLLabel.setObjectName("unaffectedLegExtensionLLabel")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.unaffectedLegExtensionLLabel)
        self.unaffectedLegExtensionLLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_6)
        self.unaffectedLegExtensionLLineEdit.setReadOnly(True)
        self.unaffectedLegExtensionLLineEdit.setObjectName("unaffectedLegExtensionLLineEdit")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.unaffectedLegExtensionLLineEdit)
        self.unaffectedLegFlexionStep3Label = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        self.unaffectedLegFlexionStep3Label.setObjectName("unaffectedLegFlexionStep3Label")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.unaffectedLegFlexionStep3Label)
        self.unaffectedLegFlexionStep3LineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_6)
        self.unaffectedLegFlexionStep3LineEdit.setReadOnly(True)
        self.unaffectedLegFlexionStep3LineEdit.setObjectName("unaffectedLegFlexionStep3LineEdit")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.unaffectedLegFlexionStep3LineEdit)
        self.affectedLegVoluntaryExtensionLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        self.affectedLegVoluntaryExtensionLabel.setObjectName("affectedLegVoluntaryExtensionLabel")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.affectedLegVoluntaryExtensionLabel)
        self.affectedLegVoluntaryExtensionLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_6)
        self.affectedLegVoluntaryExtensionLineEdit.setReadOnly(True)
        self.affectedLegVoluntaryExtensionLineEdit.setObjectName("affectedLegVoluntaryExtensionLineEdit")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.affectedLegVoluntaryExtensionLineEdit)
        self.affectedLegInvoluntaryExtensionLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        self.affectedLegInvoluntaryExtensionLabel.setObjectName("affectedLegInvoluntaryExtensionLabel")
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.affectedLegInvoluntaryExtensionLabel)
        self.affectedLegInvoluntaryExtensionLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_6)
        self.affectedLegInvoluntaryExtensionLineEdit.setReadOnly(True)
        self.affectedLegInvoluntaryExtensionLineEdit.setObjectName("affectedLegInvoluntaryExtensionLineEdit")
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.affectedLegInvoluntaryExtensionLineEdit)
        self.verticalLayout.addLayout(self.formLayout_4)
        self.label_22 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.verticalLayout.addWidget(self.label_22)
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setVerticalSpacing(20)
        self.formLayout_5.setObjectName("formLayout_5")
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setObjectName("formLayout_6")
        self.formLayout_5.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.formLayout_6)
        self.involuntaryVoluntaryRatioAffectedLegLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        self.involuntaryVoluntaryRatioAffectedLegLabel.setObjectName("involuntaryVoluntaryRatioAffectedLegLabel")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.involuntaryVoluntaryRatioAffectedLegLabel)
        self.involuntaryVoluntaryRatioAffectedLegLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_6)
        self.involuntaryVoluntaryRatioAffectedLegLineEdit.setReadOnly(True)
        self.involuntaryVoluntaryRatioAffectedLegLineEdit.setObjectName("involuntaryVoluntaryRatioAffectedLegLineEdit")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.involuntaryVoluntaryRatioAffectedLegLineEdit)
        self.consistencyOfFlexionForceStrongLegLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        self.consistencyOfFlexionForceStrongLegLabel.setObjectName("consistencyOfFlexionForceStrongLegLabel")
        self.formLayout_5.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.consistencyOfFlexionForceStrongLegLabel)
        self.consistencyOfFlexionForceStrongLegLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_6)
        self.consistencyOfFlexionForceStrongLegLineEdit.setReadOnly(True)
        self.consistencyOfFlexionForceStrongLegLineEdit.setObjectName("consistencyOfFlexionForceStrongLegLineEdit")
        self.formLayout_5.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.consistencyOfFlexionForceStrongLegLineEdit)
        self.label_23 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_23)
        self.label_24 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.formLayout_5.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_24)
        self.verticalLayout.addLayout(self.formLayout_5)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 3)
        self.horizontalLayout_11.addLayout(self.verticalLayout)
        self.line_4 = QtWidgets.QFrame(self.horizontalLayoutWidget_6)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_11.addWidget(self.line_4)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_20 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_17.addWidget(self.label_20)

        self.pushButton_5 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_6,
            checkable=True,
            toggled=self.fill_values
        )
        self.pushButton_5.setObjectName("pushButton_5")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_5.setFont(font)
        self.verticalLayout_17.addWidget(self.pushButton_5)

        self.label_21 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        self.label_21.setScaledContents(True)
        self.label_21.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_21.setWordWrap(True)
        self.label_21.setObjectName("label_21")
        self.verticalLayout_17.addWidget(self.label_21)
        self.textEdit_7 = QtWidgets.QTextEdit(self.horizontalLayoutWidget_6)
        self.textEdit_7.setObjectName("textEdit_7")
        self.verticalLayout_17.addWidget(self.textEdit_7)
        self.verticalLayout_17.setStretch(0, 1)
        self.verticalLayout_17.setStretch(1, 4)
        self.verticalLayout_17.setStretch(2, 3)
        self.horizontalLayout_11.addLayout(self.verticalLayout_17)
        self.horizontalLayout_11.setStretch(0, 3)
        self.horizontalLayout_11.setStretch(2, 4)
        self.tabWidget_2.addTab(self.tab_7, "")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        # self.tabWidget.addTab(self.tab_2, "") Uncomment when adding in hip abductor sign test
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuBaud = QtWidgets.QMenu(self.menuEdit)
        self.menuBaud.setObjectName("menuBaud")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setShortcut("Ctrl+N")
        self.actionNew.setObjectName("actionNew")
        self.actionNew.triggered.connect(self.file_new)


        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(self.file_open)


        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.setObjectName("actionSave")
        self.actionSave.triggered.connect(self.file_save)

        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionSave_As.triggered.connect(self.file_new)


        #--------Commented out for the custom port selector----#
        # self.actionPort = QtWidgets.QAction(MainWindow)
        # self.actionPort.setObjectName("actionPort")

        self.actionPort = AddComport(self, self.menuEdit)
        self.actionPort.porttnavn.connect(self.valgAfComport)


        self.action9600 = QtWidgets.QAction(MainWindow)
        self.action9600.setObjectName("action9600")
        self.action42069 = QtWidgets.QAction(MainWindow)
        self.action42069.setObjectName("action42069")
        self.actionGetting_Started = QtWidgets.QAction(MainWindow)
        self.actionGetting_Started.setObjectName("actionGetting_Started")
        self.actionTroubleshooting = QtWidgets.QAction(MainWindow)
        self.actionTroubleshooting.setObjectName("actionTroubleshooting")
        self.actionFAQs = QtWidgets.QAction(MainWindow)
        self.actionFAQs.setObjectName("actionFAQs")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuBaud.addAction(self.action9600)
        # self.menuEdit.addAction(self.actionPort)
        self.menuEdit.addAction(self.menuBaud.menuAction())
        self.menuHelp.addAction(self.actionGetting_Started)
        self.menuHelp.addAction(self.actionTroubleshooting)
        self.menuHelp.addAction(self.actionFAQs)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.serial = QtSerialPort.QSerialPort(
            "COM5",
            baudRate=QtSerialPort.QSerialPort.Baud9600,
            readyRead=self.receive
        )

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.nameLabel.setText(_translate("MainWindow", "Name:"))
        self.preferredNameLabel.setText(_translate("MainWindow", "Preferred name:"))
        self.dateOfBirthLabel.setText(_translate("MainWindow", "Date of birth:"))
        self.sexLabel.setText(_translate("MainWindow", "Sex:"))
        self.dateOfVisitLabel_2.setText(_translate("MainWindow", "Date of visit"))
        self.reasonForVisitLabel.setText(_translate("MainWindow", "Reason for visit:"))
        self.notesLabel.setText(_translate("MainWindow", "Notes:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Patient Information"))
        self.pushButton_2.setText(_translate("MainWindow", "Record"))
        self.pushButton_21.setText(_translate("MainWindow", "Clear Data"))
        self.label_4.setText(_translate("MainWindow", "Notes:"))
#         self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
# "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A place for a physician to note down any specific observations when performing the test</p>\n"
# "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "Measurements:"))
        self.label_16.setText(_translate("MainWindow", "Unaffected side hip extension and flexion"))
        self.extensionForceLabel.setText(_translate("MainWindow", "Extension force:"))
        self.flexionForceLabel.setText(_translate("MainWindow", "Flexion force:"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("MainWindow", "Step 1"))
        self.pushButton_3.setText(_translate("MainWindow", "Record"))
        self.pushButton_31.setText(_translate("MainWindow", "Clear Data"))
        self.label_10.setText(_translate("MainWindow", "Notes:"))
#         self.textEdit_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
# "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A place for a physician to note down any specific observations when performing the test</p>\n"
# "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_11.setText(_translate("MainWindow", "Measurements:"))
        self.label_17.setText(_translate("MainWindow", "Affected side hip extension"))
        self.strongLegAverageStrengthLabel_2.setText(_translate("MainWindow", "Force average:"))
        self.strongLegPeakStrengthLabel_2.setText(_translate("MainWindow", "Force peak:"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("MainWindow", "Step 2"))
        self.pushButton_4.setText(_translate("MainWindow", "Record"))
        self.pushButton_41.setText(_translate("MainWindow", "Clear Data"))
        self.label_14.setText(_translate("MainWindow", "Notes:"))
#         self.textEdit_6.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
# "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A place for a physician to note down any specific observations when performing the test</p>\n"
# "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_15.setText(_translate("MainWindow", "Measurements:"))
        self.label_18.setText(_translate("MainWindow", "Affected side involuntary extension and unaffected side flexion"))
        self.strongLegAverageStrengthLabel_3.setText(_translate("MainWindow", "Affected leg involuntary extension:"))
        self.strongLegPeakStrengthLabel_3.setText(_translate("MainWindow", "Unaffected leg flexion:"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), _translate("MainWindow", "Step 3"))
        self.label_19.setText(_translate("MainWindow", "All Measurements:"))
        self.unaffectedLegFlexionLabel.setText(_translate("MainWindow", "Unaffected leg flexion (step 1):"))
        self.unaffectedLegExtensionLLabel.setText(_translate("MainWindow", "Unaffected leg extension:"))
        self.unaffectedLegFlexionStep3Label.setText(_translate("MainWindow", "Unaffected leg flexion (step 3):"))
        self.affectedLegVoluntaryExtensionLabel.setText(_translate("MainWindow", "Affected leg voluntary extension (V):"))
        self.affectedLegInvoluntaryExtensionLabel.setText(_translate("MainWindow", "Affected leg involuntary extension (IV):"))
        self.label_22.setText(_translate("MainWindow", "Calculations:"))
        self.involuntaryVoluntaryRatioAffectedLegLabel.setText(_translate("MainWindow", "Involuntary/voluntary ratio (IVVR), affected leg:"))
        self.consistencyOfFlexionForceStrongLegLabel.setText(_translate("MainWindow", "Consistency of flexion force, strong leg:"))
        self.label_23.setText(_translate("MainWindow", "IVVR = IV/V"))
        self.label_24.setText(_translate("MainWindow", "Expressed as 1:(step 1 / step 3), for validation"))
        self.label_20.setText(_translate("MainWindow", "Results and Analysis:"))
        self.label_21.setText(_translate("MainWindow", "Press \"Calculate Results\" for an analysis of your tests."))
        self.pushButton_5.setText(_translate("MainWindow", "Calculate Results"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), _translate("MainWindow", "Results"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Hoover\'s Sign Test"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuBaud.setTitle(_translate("MainWindow", "Baud"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As..."))
        self.action9600.setText(_translate("MainWindow", "9600"))
        self.action42069.setText(_translate("MainWindow", "42069"))
        self.actionGetting_Started.setText(_translate("MainWindow", "Getting Started"))
        self.actionTroubleshooting.setText(_translate("MainWindow", "Troubleshooting"))
        self.actionFAQs.setText(_translate("MainWindow", "FAQs"))

        self.unaffectedLegFlexionLineEdit.setText(_translate("MainWindow", "0"))
        self.unaffectedLegFlexionStep3LineEdit.setText(_translate("MainWindow", "0"))
        self.unaffectedLegExtensionLLineEdit.setText(_translate("MainWindow", "0"))
        self.affectedLegInvoluntaryExtensionLineEdit.setText(_translate("MainWindow", "0"))
        self.affectedLegVoluntaryExtensionLineEdit.setText(_translate("MainWindow", "0"))


    @QtCore.pyqtSlot()
    def receive(self):
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            words = text.split()
            if self.tabWidget_2.currentIndex() == 0:
                self.hsS1RForce.append(float(words[0]))
                self.hsS1LForce.append(float(words[1]))
                self.hsS1RForceLine.setData(self.hsS1RForce)
                self.hsS1LForceLine.setData(self.hsS1LForce)
            elif self.tabWidget_2.currentIndex() == 1:
                self.hsS2RForce.append(float(words[0]))
                self.hsS2LForce.append(float(words[1]))
                self.hsS2RAverage.append(float(words[2]))
                self.hsS2RForceLine.setData(self.hsS2RForce)
                self.hsS2RAverageLine.setData(self.hsS2RAverage)
            elif self.tabWidget_2.currentIndex() == 2:
                self.hsS3RForce.append(float(words[0]))
                self.hsS3LForce.append(float(words[1]))
                self.hsS3RAverage.append(float(words[2]))
                self.hsS3RForceLine.setData(self.hsS3RForce)
                self.hsS3LForceLine.setData(self.hsS3LForce)
                self.hsS3RForceAverageLine.setData(self.hsS3RAverage)
            else:
                print("Tab index finder not working")

    @QtCore.pyqtSlot(bool)
    def on_toggled(self, checked):
        self.pushButton_4.setText("Stop" if checked else "Record")
        self.pushButton_3.setText("Stop" if checked else "Record")
        self.pushButton_2.setText("Stop" if checked else "Record")
        if checked:
            print(self.serial.portName() + " opened")
            if not self.serial.isOpen():
                if not self.serial.open(QtCore.QIODevice.ReadWrite):
                    self.pushButton_4.setChecked(False)
                    self.pushButton_3.setChecked(False)
                    self.pushButton_2.setChecked(False)
        else:
            print(self.serial.portName() + " closed")
            self.serial.close()
            self.extensionForceLineEdit.setText(str(max(self.hsS1RForce)))
            self.flexionForceLineEdit.setText(str(max(self.hsS1LForce)))
            self.strongLegAverageStrengthLineEdit_2.setText(str(max(self.hsS2RAverage)))
            self.strongLegPeakStrengthLineEdit_2.setText(str(max(self.hsS2RForce)))
            self.strongLegAverageStrengthLineEdit_3.setText(str(max(self.hsS3RForce)))
            self.strongLegPeakStrengthLineEdit_3.setText(str(max(self.hsS3LForce)))

    @QtCore.pyqtSlot(bool)
    def clear_data(self, checked):
        if self.tabWidget_2.currentIndex() == 0:
            self.hsS1RForce = [0]
            self.hsS1LForce = [0]
            self.hsS1RForceLine.setData(self.hsS1RForce)
            self.hsS1LForceLine.setData(self.hsS1LForce)
        elif self.tabWidget_2.currentIndex() == 1:
            self.hsS2RForce = [0]
            self.hsS2LForce = [0]
            self.hsS2RAverage = [0]
            self.hsS2RForceLine.setData(self.hsS2RForce)
            self.hsS2RAverageLine.setData(self.hsS2RAverage)
        elif self.tabWidget_2.currentIndex() == 2:
            self.hsS3RForce = [0]
            self.hsS3LForce = [0]
            self.hsS3RAverage = [0]
            self.hsS3RForceLine.setData(self.hsS3RForce)
            self.hsS3LForceLine.setData(self.hsS3LForce)
            self.hsS3RForceAverageLine.setData(self.hsS3RAverage)
        else:
            print("Tab index finder not working")

    def fill_values(self):
        try:
            self.unaffectedLegFlexionLineEdit.setText(self.flexionForceLineEdit.text())
            self.unaffectedLegExtensionLLineEdit.setText(self.extensionForceLineEdit.text())
            self.unaffectedLegFlexionStep3LineEdit.setText(self.strongLegPeakStrengthLineEdit_3.text())
            self.affectedLegVoluntaryExtensionLineEdit.setText(self.strongLegAverageStrengthLineEdit_2.text())
            self.affectedLegInvoluntaryExtensionLineEdit.setText(self.strongLegAverageStrengthLineEdit_3.text())

            ivvr = (float(self.affectedLegInvoluntaryExtensionLineEdit.text()) /
                    float(self.affectedLegVoluntaryExtensionLineEdit.text()))
            ivvr = str(f'{ivvr:.2f}')
            self.involuntaryVoluntaryRatioAffectedLegLineEdit.setText(ivvr)

            flexionForceConsistency = (float(self.unaffectedLegFlexionLineEdit.text()) /
                                       float(self.unaffectedLegFlexionStep3LineEdit.text()))
            flexionForceConsistency = str(f'{flexionForceConsistency:.2f}')
            self.consistencyOfFlexionForceStrongLegLineEdit.setText("1:" + flexionForceConsistency)

            self.label_21.setText("The ratio between the affected leg\'s voluntary and involuntary flexion was "
                           + ivvr
                           + ". An IVVR of 2.48 with a standard error of 0.61 was determined to be a high confidence "
                           + "measurement for a positive Hoover's Sign.")

        except Exception:
            print("Error: all measured values must be filled in to see results")

    def file_open(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, caption='Open File', directory=os.getcwd() + "\patient data", filter="CSV Files (*.csv)")
        self.openFile = name[0]
        with open(name[0], 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            counter = 0
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                if counter == 0:
                    # assign all "patient information" values to their location
                    self.nameLineEdit.setText(row[1])
                    self.preferredNameLineEdit.setText(row[2])
                    bday = QtCore.QDate.fromString(row[3])
                    self.dateOfBirthDateEdit.setDate(bday)
                    self.sexLineEdit.setText(row[4])
                    vday = QtCore.QDate.fromString(row[5])
                    self.dateOfVisitDateEdit.setDate(vday)
                    self.reasonForVisitLineEdit.setText(row[6])
                    self.notesLineEdit.setText(row[7])
                elif counter == 2 :
                    del row[0]
                    self.hsS1RForce = [float(x) for x in row]
                    self.hsS1RForceLine.setData(self.hsS1RForce)
                elif counter == 4 :
                    del row[0]
                    self.hsS1LForce = [float(x) for x in row]
                    self.hsS1LForceLine.setData(self.hsS1LForce)
                elif counter == 6 :
                    del row[0]
                    self.hsS2RForce = [float(x) for x in row]
                    self.hsS2RForceLine.setData(self.hsS2RForce)
                elif counter == 8 :
                    del row[0]
                    self.hsS2RAverage = [float(x) for x in row]
                    self.hsS2RAverageLine.setData(self.hsS2RAverage)
                elif counter == 10 :
                    del row[0]
                    self.hsS3RForce = [float(x) for x in row]
                    self.hsS3RForceLine.setData(self.hsS3RForce)
                elif counter == 12 :
                    del row[0]
                    self.hsS3RAverage = [float(x) for x in row]
                    self.hsS3RForceAverageLine.setData(self.hsS3RAverage)
                elif counter == 14 :
                    del row[0]
                    self.hsS3LForce = [float(x) for x in row]
                    self.hsS3LForceLine.setData(self.hsS3LForce)
                elif counter == 16 :
                    self.textEdit.setText(row[1])
                    self.textEdit_2.setText(row[2])
                    self.textEdit_6.setText(row[3])
                    self.textEdit_7.setText(row[4])
                counter = counter + 1

        self.extensionForceLineEdit.setText(str(max(self.hsS1RForce)))
        self.flexionForceLineEdit.setText(str(max(self.hsS1LForce)))
        self.strongLegAverageStrengthLineEdit_2.setText(str(max(self.hsS2RAverage)))
        self.strongLegPeakStrengthLineEdit_2.setText(str(max(self.hsS2RForce)))
        self.strongLegAverageStrengthLineEdit_3.setText(str(max(self.hsS3RForce)))
        self.strongLegPeakStrengthLineEdit_3.setText(str(max(self.hsS3LForce)))

        self.fill_values()


    def file_save(self):
        if self.openFile != '' :
            with open(self.openFile, 'w', encoding='UTF8') as f:  # was fileName__
                writer = csv.writer(f)

                # write the header
                writer.writerow(["Patient Information:", self.nameLineEdit.text(), self.preferredNameLineEdit.text(),
                                 self.dateOfBirthDateEdit.date().toString(),
                                 self.sexLineEdit.text(), self.dateOfVisitDateEdit.date().toString(),
                                 self.reasonForVisitLineEdit.text(),
                                 self.notesLineEdit.text()])
                self.hsS1RForce.insert(0, "HS step 1 extension force: ")
                writer.writerow(self.hsS1RForce)
                self.hsS1LForce.insert(0, "HS step 1 flexion force: ")
                writer.writerow(self.hsS1LForce)
                self.hsS2RForce.insert(0, "HS step 2 extension force: ")
                writer.writerow(self.hsS2RForce)
                self.hsS2RAverage.insert(0, "HS step 2 extension force average: ")
                writer.writerow(self.hsS2RAverage)
                self.hsS3RForce.insert(0, "HS step 3 extension force: ")
                writer.writerow(self.hsS3RForce)
                self.hsS3RAverage.insert(0, "HS step 3 extension force average: ")
                writer.writerow(self.hsS3RAverage)
                self.hsS3LForce.insert(0, "HS step 3 flexion force: ")
                writer.writerow(self.hsS3LForce)
                writer.writerow(["Text edit contents: ", self.textEdit.toPlainText(), self.textEdit_2.toPlainText(),
                                 self.textEdit_6.toPlainText(), self.textEdit_7.toPlainText()])
                writer.writerow(["Unaffected leg flexion (step 1):", "Unaffected leg extension:", "Unaffected leg flexion (step 3):",
                                 "Affected leg voluntary extension (V):", "Affected leg involuntary extension (IV):",
                                 "Affected leg involuntary/voluntary ratio (IVVR = IV/V):", "Unaffected leg flexion force consistency:"])
                writer.writerow([self.flexionForceLineEdit.text(),self.extensionForceLineEdit.text(), self.strongLegPeakStrengthLineEdit_3.text(),
                                 self.strongLegAverageStrengthLineEdit_2.text(), self.strongLegAverageStrengthLineEdit_3.text(),
                                 self.involuntaryVoluntaryRatioAffectedLegLineEdit.text(), self.consistencyOfFlexionForceStrongLegLineEdit.text()])
            print("File saved successfully as: " + self.openFile)
        else:
            print("Error! You must create a New File before saving!")

    def file_new(self):
        # bring up file dialog to set new file name
        name = QtWidgets.QFileDialog.getSaveFileName(self, caption="New File", directory=os.getcwd() + "\patient data", filter="CSV Files (*.csv)")
        self.openFile = name[0]
        # Write important values to csv. Line by line seems the only way
        with open(name[0], 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(["Patient Information:", self.nameLineEdit.text(), self.preferredNameLineEdit.text(),
                             self.dateOfBirthDateEdit.date().toString(),
                             self.sexLineEdit.text(), self.dateOfVisitDateEdit.date().toString(),
                             self.reasonForVisitLineEdit.text(),
                             self.notesLineEdit.text()])
            self.hsS1RForce.insert(0, "HS step 1 extension force: ")
            writer.writerow(self.hsS1RForce)
            self.hsS1LForce.insert(0, "HS step 1 flexion force: ")
            writer.writerow(self.hsS1LForce)
            self.hsS2RForce.insert(0, "HS step 2 extension force: ")
            writer.writerow(self.hsS2RForce)
            self.hsS2RAverage.insert(0, "HS step 2 extension force average: ")
            writer.writerow(self.hsS2RAverage)
            self.hsS3RForce.insert(0, "HS step 3 extension force: ")
            writer.writerow(self.hsS3RForce)
            self.hsS3RAverage.insert(0, "HS step 3 extension force average: ")
            writer.writerow(self.hsS3RAverage)
            self.hsS3LForce.insert(0, "HS step 3 flexion force: ")
            writer.writerow(self.hsS3LForce)
            writer.writerow(["Text edit contents: ", self.textEdit.toPlainText(), self.textEdit_2.toPlainText(),
                             self.textEdit_6.toPlainText(), self.textEdit_7.toPlainText()])
            writer.writerow(
                ["Unaffected leg flexion (step 1):", "Unaffected leg extension:", "Unaffected leg flexion (step 3):",
                 "Affected leg voluntary extension (V):", "Affected leg involuntary extension (IV):",
                 "Affected leg involuntary/voluntary ratio (IVVR = IV/V):",
                 "Unaffected leg flexion force consistency:"])
            writer.writerow([self.flexionForceLineEdit.text(), self.extensionForceLineEdit.text(),
                             self.strongLegPeakStrengthLineEdit_3.text(),
                             self.strongLegAverageStrengthLineEdit_2.text(),
                             self.strongLegAverageStrengthLineEdit_3.text(),
                             self.involuntaryVoluntaryRatioAffectedLegLineEdit.text(),
                             self.consistencyOfFlexionForceStrongLegLineEdit.text()])
        print("File saved successfully.")

    def valgAfComport(self, nyport):
        seropen = False
        if self.serial.isOpen():
            seropen = True
            self.serial.close()
        self.serial.setPortName(nyport)
        if seropen:
            self.serial.open(QtCore.QIODevice.ReadWrite)
            if not self.serial.isOpen():
                self.recordButton.setChecked(False)

        print(nyport)

    def closeEvent(self, event):
        self.serial.close()
        print("All connections closed")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # pyi_splash.close()
    sys.exit(app.exec_())
