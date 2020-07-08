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
        MainWindow.resize(793, 904)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_learn = QtWidgets.QWidget()
        self.tab_learn.setObjectName("tab_learn")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_learn)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.t_word = QtWidgets.QLabel(self.tab_learn)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(50)
        font.setBold(False)
        font.setWeight(50)
        self.t_word.setFont(font)
        self.t_word.setAlignment(QtCore.Qt.AlignCenter)
        self.t_word.setObjectName("t_word")
        self.verticalLayout.addWidget(self.t_word)
        self.t_pron = QtWidgets.QLabel(self.tab_learn)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(20)
        self.t_pron.setFont(font)
        self.t_pron.setAlignment(QtCore.Qt.AlignCenter)
        self.t_pron.setObjectName("t_pron")
        self.verticalLayout.addWidget(self.t_pron)
        self.t_mean = QtWidgets.QLabel(self.tab_learn)
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
        self.t_syn = QtWidgets.QLabel(self.tab_learn)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.t_syn.setFont(font)
        self.t_syn.setAlignment(QtCore.Qt.AlignCenter)
        self.t_syn.setObjectName("t_syn")
        self.verticalLayout.addWidget(self.t_syn)
        self.t_ex = QtWidgets.QLabel(self.tab_learn)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(17)
        self.t_ex.setFont(font)
        self.t_ex.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.t_ex.setWordWrap(True)
        self.t_ex.setObjectName("t_ex")
        self.verticalLayout.addWidget(self.t_ex)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.b_triangle = QtWidgets.QLabel(self.tab_learn)
        self.b_triangle.setMaximumSize(QtCore.QSize(60, 60))
        self.b_triangle.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.b_triangle.setPixmap(QtGui.QPixmap("ui/triangle_empty.png"))
        self.b_triangle.setScaledContents(True)
        self.b_triangle.setObjectName("b_triangle")
        self.horizontalLayout_8.addWidget(self.b_triangle)
        self.b_star = QtWidgets.QLabel(self.tab_learn)
        self.b_star.setMaximumSize(QtCore.QSize(60, 60))
        self.b_star.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.b_star.setPixmap(QtGui.QPixmap("ui/star_empty.png"))
        self.b_star.setScaledContents(True)
        self.b_star.setObjectName("b_star")
        self.horizontalLayout_8.addWidget(self.b_star)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.b_show_note = QtWidgets.QCheckBox(self.tab_learn)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.b_show_note.setFont(font)
        self.b_show_note.setObjectName("b_show_note")
        self.horizontalLayout_2.addWidget(self.b_show_note)
        self.t_stat = QtWidgets.QLabel(self.tab_learn)
        self.t_stat.setObjectName("t_stat")
        self.horizontalLayout_2.addWidget(self.t_stat)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.t_note = QtWidgets.QTextEdit(self.tab_learn)
        font = QtGui.QFont()
        font.setFamily("Hannotate SC")
        font.setPointSize(20)
        self.t_note.setFont(font)
        self.t_note.setObjectName("t_note")
        self.verticalLayout_2.addWidget(self.t_note)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.b_yes = QtWidgets.QPushButton(self.tab_learn)
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
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.b_no = QtWidgets.QPushButton(self.tab_learn)
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
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.b_show = QtWidgets.QPushButton(self.tab_learn)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        font.setPointSize(24)
        self.b_show.setFont(font)
        self.b_show.setStyleSheet("QPushButton\n"
"{\n"
"   color:#3F51B5;\n"
"}")
        self.b_show.setObjectName("b_show")
        self.horizontalLayout.addWidget(self.b_show)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.b_to_eb = QtWidgets.QPushButton(self.tab_learn)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        font.setPointSize(24)
        self.b_to_eb.setFont(font)
        self.b_to_eb.setStyleSheet("QPushButton\n"
"{\n"
"   color:#9C27B0;\n"
"}")
        self.b_to_eb.setObjectName("b_to_eb")
        self.horizontalLayout.addWidget(self.b_to_eb)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.b_trash = QtWidgets.QPushButton(self.tab_learn)
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
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.b_fn = QtWidgets.QPushButton(self.tab_learn)
        font = QtGui.QFont()
        font.setFamily("Menlo")
        font.setPointSize(24)
        self.b_fn.setFont(font)
        self.b_fn.setStyleSheet("QPushButton\n"
"{\n"
"   color:#018786;\n"
"}")
        self.b_fn.setObjectName("b_fn")
        self.horizontalLayout.addWidget(self.b_fn)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 1)
        self.horizontalLayout.setStretch(5, 1)
        self.horizontalLayout.setStretch(6, 1)
        self.horizontalLayout.setStretch(7, 1)
        self.horizontalLayout.setStretch(8, 1)
        self.horizontalLayout.setStretch(9, 1)
        self.horizontalLayout.setStretch(10, 1)
        self.horizontalLayout.setStretch(11, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_learn, "")
        self.tab_eb = QtWidgets.QWidget()
        self.tab_eb.setObjectName("tab_eb")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_eb)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.b_hide_eb = QtWidgets.QCheckBox(self.tab_eb)
        self.b_hide_eb.setObjectName("b_hide_eb")
        self.verticalLayout_6.addWidget(self.b_hide_eb)
        self.t_table_eb = QtWidgets.QTableView(self.tab_eb)
        self.t_table_eb.setObjectName("t_table_eb")
        self.verticalLayout_6.addWidget(self.t_table_eb)
        self.gridLayout_3.addLayout(self.verticalLayout_6, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_eb, "")
        self.tab_newbie = QtWidgets.QWidget()
        self.tab_newbie.setObjectName("tab_newbie")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_newbie)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.b_hide_new = QtWidgets.QCheckBox(self.tab_newbie)
        self.b_hide_new.setObjectName("b_hide_new")
        self.verticalLayout_7.addWidget(self.b_hide_new)
        self.t_table_new = QtWidgets.QTableView(self.tab_newbie)
        self.t_table_new.setObjectName("t_table_new")
        self.verticalLayout_7.addWidget(self.t_table_new)
        self.gridLayout_4.addLayout(self.verticalLayout_7, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_newbie, "")
        self.tab_trashed = QtWidgets.QWidget()
        self.tab_trashed.setObjectName("tab_trashed")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_trashed)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.b_hide_trash = QtWidgets.QCheckBox(self.tab_trashed)
        self.b_hide_trash.setObjectName("b_hide_trash")
        self.verticalLayout_5.addWidget(self.b_hide_trash)
        self.t_table_trash = QtWidgets.QTableView(self.tab_trashed)
        self.t_table_trash.setObjectName("t_table_trash")
        self.verticalLayout_5.addWidget(self.t_table_trash)
        self.gridLayout_5.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_trashed, "")
        self.tab_explore = QtWidgets.QWidget()
        self.tab_explore.setObjectName("tab_explore")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_explore)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.b_hide_explore = QtWidgets.QCheckBox(self.tab_explore)
        self.b_hide_explore.setObjectName("b_hide_explore")
        self.verticalLayout_8.addWidget(self.b_hide_explore)
        self.t_table_explore = QtWidgets.QTableView(self.tab_explore)
        self.t_table_explore.setObjectName("t_table_explore")
        self.verticalLayout_8.addWidget(self.t_table_explore)
        self.gridLayout_6.addLayout(self.verticalLayout_8, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_explore, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.b_hide_star = QtWidgets.QCheckBox(self.tab)
        self.b_hide_star.setObjectName("b_hide_star")
        self.verticalLayout_9.addWidget(self.b_hide_star)
        self.t_table_star = QtWidgets.QTableView(self.tab)
        self.t_table_star.setObjectName("t_table_star")
        self.verticalLayout_9.addWidget(self.t_table_star)
        self.gridLayout_7.addLayout(self.verticalLayout_9, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.b_hide_triangle = QtWidgets.QCheckBox(self.tab_2)
        self.b_hide_triangle.setObjectName("b_hide_triangle")
        self.verticalLayout_10.addWidget(self.b_hide_triangle)
        self.t_table_triangle = QtWidgets.QTableView(self.tab_2)
        self.t_table_triangle.setObjectName("t_table_triangle")
        self.verticalLayout_10.addWidget(self.t_table_triangle)
        self.gridLayout_8.addLayout(self.verticalLayout_10, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_setting = QtWidgets.QWidget()
        self.tab_setting.setObjectName("tab_setting")
        self.layoutWidget = QtWidgets.QWidget(self.tab_setting)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 267, 160))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.t_version = QtWidgets.QLabel(self.layoutWidget)
        self.t_version.setAlignment(QtCore.Qt.AlignCenter)
        self.t_version.setObjectName("t_version")
        self.verticalLayout_4.addWidget(self.t_version)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.e_eb_thresh = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.e_eb_thresh.setMaximum(0.99)
        self.e_eb_thresh.setSingleStep(0.01)
        self.e_eb_thresh.setObjectName("e_eb_thresh")
        self.horizontalLayout_4.addWidget(self.e_eb_thresh)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.e_newbie_thresh = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.e_newbie_thresh.setMaximum(0.99)
        self.e_newbie_thresh.setSingleStep(0.01)
        self.e_newbie_thresh.setProperty("value", 0.0)
        self.e_newbie_thresh.setObjectName("e_newbie_thresh")
        self.horizontalLayout_3.addWidget(self.e_newbie_thresh)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.e_newbie2eb_thresh = QtWidgets.QSpinBox(self.layoutWidget)
        self.e_newbie2eb_thresh.setMinimum(1)
        self.e_newbie2eb_thresh.setObjectName("e_newbie2eb_thresh")
        self.horizontalLayout_5.addWidget(self.e_newbie2eb_thresh)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.e_mode = QtWidgets.QComboBox(self.layoutWidget)
        self.e_mode.setObjectName("e_mode")
        self.e_mode.addItem("")
        self.e_mode.addItem("")
        self.e_mode.addItem("")
        self.e_mode.addItem("")
        self.e_mode.addItem("")
        self.horizontalLayout_6.addWidget(self.e_mode)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.tabWidget.addTab(self.tab_setting, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
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
        self.b_show_note.setText(_translate("MainWindow", "Always show note"))
        self.t_stat.setText(_translate("MainWindow", "statistics"))
        self.t_note.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Hannotate SC\'; font-size:20pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sinhala Sangam MN\';\"><br /></p></body></html>"))
        self.b_yes.setText(_translate("MainWindow", " Yes "))
        self.b_no.setText(_translate("MainWindow", " No "))
        self.b_show.setText(_translate("MainWindow", "Show"))
        self.b_to_eb.setText(_translate("MainWindow", "ToEb"))
        self.b_trash.setText(_translate("MainWindow", "Trash"))
        self.b_fn.setText(_translate("MainWindow", " Fn "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_learn), _translate("MainWindow", "Learn"))
        self.b_hide_eb.setText(_translate("MainWindow", "Hide Solution"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_eb), _translate("MainWindow", "Ebbinghaus Table"))
        self.b_hide_new.setText(_translate("MainWindow", "Hide Solution"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_newbie), _translate("MainWindow", "Newbie Table"))
        self.b_hide_trash.setText(_translate("MainWindow", "Hide Solution"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_trashed), _translate("MainWindow", "Trashed"))
        self.b_hide_explore.setText(_translate("MainWindow", "Hide Solution"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_explore), _translate("MainWindow", "Explore"))
        self.b_hide_star.setText(_translate("MainWindow", "Hide Solution"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "★"))
        self.b_hide_triangle.setText(_translate("MainWindow", "Hide Solution"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "▲"))
        self.t_version.setText(_translate("MainWindow", "Version Info"))
        self.label.setText(_translate("MainWindow", "Eb Quiz Threshold         "))
        self.label_2.setText(_translate("MainWindow", "Newbie Quiz Threshold "))
        self.label_3.setText(_translate("MainWindow", "Newbie to Eb Threshold"))
        self.label_4.setText(_translate("MainWindow", "Learning Mode"))
        self.e_mode.setItemText(0, _translate("MainWindow", "Normal"))
        self.e_mode.setItemText(1, _translate("MainWindow", "Eb Table Only"))
        self.e_mode.setItemText(2, _translate("MainWindow", "Newbie Table Only"))
        self.e_mode.setItemText(3, _translate("MainWindow", "Starred"))
        self.e_mode.setItemText(4, _translate("MainWindow", "Triangled"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_setting), _translate("MainWindow", "Setting"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
