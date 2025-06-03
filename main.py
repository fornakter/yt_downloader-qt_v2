from PyQt5 import QtCore, QtGui, QtWidgets
import yt_dlp
import threading, requests
import os

from PyQt5.QtWidgets import QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(645, 120)
        MainWindow.setMinimumSize(QtCore.QSize(645, 120))
        MainWindow.setMaximumSize(QtCore.QSize(645, 120))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.UrlEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.UrlEdit.setGeometry(QtCore.QRect(10, 10, 511, 27))
        self.UrlEdit.setPlaceholderText("")
        self.UrlEdit.setObjectName("UrlEdit")

        # Go button

        self.goButton = QtWidgets.QPushButton(self.centralwidget)
        self.goButton.setGeometry(QtCore.QRect(540, 10, 94, 27))
        self.goButton.setObjectName("goButton")
        self.goButton.clicked.connect(self.goButtonClick)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 90, 71, 19))
        self.label.setObjectName("label")

        # Status Text

        self.StatusText = QtWidgets.QLabel(self.centralwidget)
        self.StatusText.setGeometry(QtCore.QRect(70, 90, 451, 19))
        self.StatusText.setToolTip("")
        self.StatusText.setObjectName("StatusText")

        # Info Button

        self.InfoButton = QtWidgets.QPushButton(self.centralwidget)
        self.InfoButton.setGeometry(QtCore.QRect(540, 50, 94, 27))
        self.InfoButton.setObjectName("InfoButton")
        self.InfoButton.clicked.connect(self.infoButtonClick)

        # Radio button Audio

        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(20, 50, 117, 25))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")

        # Radio button Video

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(150, 50, 117, 25))
        self.radioButton_2.setObjectName("radioButton_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def infoButtonClick(self):
        msg = QMessageBox()
        msg.setWindowTitle("info")
        msg.setText("\n   Pobieraj filmy i muzykę z YT   \n"
                    "   Autor: Adam Fatyga\n"
                    "   Wersja 0.7\n")

        x = msg.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "yt_dl"))
        self.goButton.setText(_translate("MainWindow", "Go!"))
        self.label.setText(_translate("MainWindow", "Status: "))
        self.StatusText.setText(_translate("MainWindow", "TextLabel"))
        self.InfoButton.setText(_translate("MainWindow", "Info"))
        self.radioButton.setText(_translate("MainWindow", "Audio"))
        self.radioButton_2.setText(_translate("MainWindow", "Video"))


    # Download file
    def download_file(self, output_path='./'):
        if self.check_net():

            # audio
            if self.radioButton.isChecked():
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '256',
                    }],

                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                }
            else:
                print("video")

                # video

                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',  # pobiera najlepszą kombinację wideo+audio
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(self.UrlEdit.text(), download=True)
                    print(f"Downloaded: {info.get('title', 'unknown title')}")
                self.StatusText.setText("Done!")
            except Exception as e:
                self.StatusText.setText(str(e))
            self.goButton.setEnabled(True)



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