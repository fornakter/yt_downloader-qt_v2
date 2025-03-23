
from PyQt5 import QtCore, QtGui, QtWidgets
import yt_dlp
import threading, requests


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(645, 119)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Url window
        self.UrlEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.UrlEdit.setGeometry(QtCore.QRect(10, 10, 511, 27))
        self.UrlEdit.setObjectName("UrlEdit")
        self.UrlEdit.setText("https://www.youtube.com/watch?v=0qIVDMvNx2Y")

        # Go button
        self.goButton = QtWidgets.QPushButton(self.centralwidget)
        self.goButton.setGeometry(QtCore.QRect(540, 10, 94, 27))
        self.goButton.setObjectName("goButton")
        self.goButton.clicked.connect(self.goButtonClick)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 60, 71, 19))
        self.label.setObjectName("label")

        # Status label
        self.StatusText = QtWidgets.QLabel(self.centralwidget)
        self.StatusText.setGeometry(QtCore.QRect(70, 60, 71, 19))
        self.StatusText.setObjectName("StatusText")
        self.InfoButton = QtWidgets.QPushButton(self.centralwidget)
        self.InfoButton.setGeometry(QtCore.QRect(540, 50, 94, 27))
        self.InfoButton.setObjectName("InfoButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.goButton.setText(_translate("MainWindow", "Go!"))
        self.label.setText(_translate("MainWindow", "Status: "))
        self.StatusText.setText(_translate("MainWindow", "TextLabel"))
        self.InfoButton.setText(_translate("MainWindow", "Info"))

    # Download file
    def download_file(self):
        if self.check_net():

            try:
                ydl_opts = {
                    'format': 'best',  # Pobierz najlepszą jakość
                    'outtmpl': '%(title)s.%(ext)s',  # Nazwa pliku
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.UrlEdit.text()])
                self.goButton.setEnabled(True)
                self.StatusText.setText("Done!")
            except Exception as e:
                self.StatusText.setText(str(e))

    # Go button action
    def goButtonClick(self):
        self.goButton.setEnabled(False)
        threading.Thread(target=self.download_file).start()
        self.StatusText.setText("Download...")


    # Check internet connection and rise errors
    def check_net(self):
        timeout = 1
        try:
            requests.head("http://www.google.com/", timeout=timeout)
            self.StatusText.setObjectName('Internet works')
            return True
        except requests.ConnectionError:
            self.StatusText.setObjectName('Internet connections problem.')
            return False


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())