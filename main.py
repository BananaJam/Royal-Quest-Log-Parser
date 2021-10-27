import bs4, sys
import pandas as pd
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PyQt6 import QtCore, QtGui, QtWidgets

table = {}


def open_file():
    global table
    table = {}
    Tk().withdraw()
    filename = askopenfilename()
    print(filename)
    log_html = bs4.BeautifulSoup(
        open(filename, "r").read().encode('cp1251'), "html.parser")

    temp = log_html.find('tr').text.split('\n')
    temp = [a.replace('Вы нанесли ', '') for a in temp]
    temp = [a.replace(' урона', '') for a in temp]
    temp = [a.replace(' Цель: ', '') for a in temp]
    temp = list(filter(('').__ne__, temp))
    mobs = [a.split('.')[1] for a in temp]
    dmg = [int(a.split('.')[0]) for a in temp]

    times_raw = log_html.find_all('tr')
    times_raw = [a['title'] for a in times_raw]
    times = []
    for time in times_raw:
        time = datetime.strptime('10/26 14:50:08', "%m/%d %H:%M:%S")
        time = datetime(datetime.today().year, time.month,
                        time.day, time.hour, time.minute, time.second)
        times.append(time)

    #list = [{'mob': mobs[i], 'dmg' : dmg[i], 'logtime' : times[i]} for i in range(len(mobs))]
    table = pd.DataFrame({'timestamp': times, 'mob': mobs, 'damage': dmg})
    ui.comboBox.clear()
    ui.comboBox.addItems(table['mob'].unique())


def update_table():
    global table
    filtered = table[table.mob == ui.comboBox.currentText()][[
        'timestamp', 'mob', 'damage']]
    start_time = filtered.iloc[0]['timestamp']
    end_time = filtered.iloc[-1]['timestamp']
    total_dmg = sum(
        [a for a in table[table.mob == ui.comboBox.currentText()]['damage']])
    a = (end_time - start_time).seconds
    time = a if a > 0 else 1
    dps = total_dmg / time
    ui.label_5.setText(str(start_time))
    ui.label_6.setText(str(end_time))
    ui.label_7.setText(str(total_dmg))
    ui.label_8.setText(str(dps))
    ui.label_10.setText(str(time))


class Window(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setFixedSize(200, 180)
        MainWindow.setWindowIcon(QtGui.QIcon(sys._MEIPASS + "/logo.png"))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAnimated(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 181, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.activated.connect(update_table)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 40, 60, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 60, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 81, 15))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 120, 60, 15))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(70, 40, 120, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(70, 60, 120, 20))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(90, 100, 100, 20))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(40, 120, 150, 20))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 80, 60, 15))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setObjectName("label_10self.label_10")
        self.label_10.setGeometry(QtCore.QRect(70, 80, 120, 15))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 201, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.triggered.connect(open_file)
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RQLP"))
        self.label.setText(_translate("MainWindow", "Start time:"))
        self.label_2.setText(_translate("MainWindow", "End time:"))
        self.label_3.setText(_translate("MainWindow", "Total damage:"))
        self.label_4.setText(_translate("MainWindow", "DPS:"))
        self.label_9.setText(_translate("MainWindow", "Total time:"))
        self.label_5.setText(_translate("MainWindow", "0"))
        self.label_6.setText(_translate("MainWindow", "0"))
        self.label_7.setText(_translate("MainWindow", "0"))
        self.label_8.setText(_translate("MainWindow", "0"))
        self.label_10.setText(_translate("MainWindow", "0"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
