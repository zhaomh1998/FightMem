# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/FightMemPC.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(624, 718)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.t_word = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(50)
        font.setBold(False)
        font.setWeight(50)
        self.t_word.setFont(font)
        self.t_word.setAlignment(QtCore.Qt.AlignCenter)
        self.t_word.setObjectName("t_word")
        self.verticalLayout.addWidget(self.t_word)
        self.t_pron = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(20)
        self.t_pron.setFont(font)
        self.t_pron.setAlignment(QtCore.Qt.AlignCenter)
        self.t_pron.setObjectName("t_pron")
        self.verticalLayout.addWidget(self.t_pron)
        self.t_mean = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Hannotate SC")
        font.setPointSize(20)
        font.setKerning(False)
        self.t_mean.setFont(font)
        self.t_mean.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.t_mean.setWordWrap(True)
        self.t_mean.setObjectName("t_mean")
        self.verticalLayout.addWidget(self.t_mean)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.t_syn = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.t_syn.setFont(font)
        self.t_syn.setAlignment(QtCore.Qt.AlignCenter)
        self.t_syn.setObjectName("t_syn")
        self.verticalLayout.addWidget(self.t_syn)
        self.t_ex = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Hiragino Sans")
        font.setPointSize(17)
        font.setKerning(False)
        self.t_ex.setFont(font)
        self.t_ex.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.t_ex.setWordWrap(True)
        self.t_ex.setObjectName("t_ex")
        self.verticalLayout.addWidget(self.t_ex)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.b_show_note = QtWidgets.QCheckBox(self.centralwidget)
        self.b_show_note.setObjectName("b_show_note")
        self.verticalLayout_2.addWidget(self.b_show_note)
        self.t_note = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Hannotate SC")
        font.setPointSize(20)
        self.t_note.setFont(font)
        self.t_note.setObjectName("t_note")
        self.verticalLayout_2.addWidget(self.t_note)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.b_yes = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        font.setPointSize(24)
        self.b_yes.setFont(font)
        self.b_yes.setStyleSheet("QPushButton\n"
"{\n"
"   color:#009688;\n"
"}")
        self.b_yes.setObjectName("b_yes")
        self.horizontalLayout.addWidget(self.b_yes)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.b_no = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        font.setPointSize(24)
        self.b_no.setFont(font)
        self.b_no.setStyleSheet("QPushButton\n"
"{\n"
"   color:#FF5722;\n"
"}")
        self.b_no.setObjectName("b_no")
        self.horizontalLayout.addWidget(self.b_no)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.b_later = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        font.setPointSize(24)
        self.b_later.setFont(font)
        self.b_later.setStyleSheet("QPushButton\n"
"{\n"
"   color:#9C27B0;\n"
"}")
        self.b_later.setObjectName("b_later")
        self.horizontalLayout.addWidget(self.b_later)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.b_trash = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        font.setPointSize(24)
        self.b_trash.setFont(font)
        self.b_trash.setStyleSheet("QPushButton\n"
"{\n"
"   color:#9E9E9E;\n"
"}")
        self.b_trash.setObjectName("b_trash")
        self.horizontalLayout.addWidget(self.b_trash)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 1)
        self.horizontalLayout.setStretch(5, 1)
        self.horizontalLayout.setStretch(6, 1)
        self.horizontalLayout.setStretch(7, 1)
        self.horizontalLayout.setStretch(8, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.t_word.setText(_translate("MainWindow", "Abandon"))
        self.t_pron.setText(_translate("MainWindow", "[əˈbændən]"))
        self.t_mean.setText(_translate("MainWindow", "(1)v. to leave and never return to  放弃\n"
"(2)v. to give over unrestrainedly 放纵"))
        self.t_syn.setText(_translate("MainWindow", "desert, relinquish"))
        self.t_ex.setText(_translate("MainWindow", "The agency was responding to Republican Gov. Chris Sununu\'s announcement that it was time to abandon the \"ﬂawed project\" and has since called on all parties to agree on a plan that has community support."))
        self.b_show_note.setText(_translate("MainWindow", "Automatically Show Note"))
        self.t_note.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Hannotate SC\'; font-size:20pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sinhala Sangam MN\';\"><br /></p></body></html>"))
        self.b_yes.setText(_translate("MainWindow", " Yes "))
        self.b_no.setText(_translate("MainWindow", " No "))
        self.b_later.setText(_translate("MainWindow", "Later"))
        self.b_trash.setText(_translate("MainWindow", "Trash"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())