from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from ui.FightMemPCUI import *
import core
from ui.DataFrameView import DataFrameModel
import sys


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.backend = core.FightMem('data/GRE1450.fmknowledge')
        self.word = 'Error'
        self.pron = 'Knowledge file load error'
        self.mean = 'Knowledge file load error'
        self.syn = 'Knowledge file load error'
        self.ex = 'Knowledge file load error'
        self.note = 'Knowledge file load error'
        self.stat = None
        self.answer_hidden = True

        self.refresh_ui()
        self.setup_callback()
        self.next_word('init')

    def refresh_ui(self):
        self.t_word.setText(self.word)
        self.t_pron.setText(self.pron)
        self.t_mean.setText(self.mean)
        self.t_syn.setText(self.syn)
        self.t_ex.setText(self.ex)
        self.t_note.setText(self.note)
        if self.answer_hidden:
            self.t_mean.hide()
            self.t_syn.hide()
            self.t_ex.hide()
            self.t_note.hide()
        else:
            self.t_mean.show()
            self.t_syn.show()
            self.t_ex.show()
            self.t_note.show()

        if self.b_show_note.checkState():
            self.t_note.show()

        if self.stat is None:
            self.t_stat.setText('')
        else:
            unseen_count = self.stat['unseen_count']
            if self.stat['is_new']:
                self.t_stat.setText(f'Unseen: {unseen_count}')
            else:
                correct_rate = self.stat['rate']
                self.t_stat.setText(f'Correct: {correct_rate}, Unseen: {unseen_count}')
        self.repaint()

    def setup_callback(self):
        self.b_show.clicked.connect(lambda: self.toggle_answer())
        self.b_show_note.stateChanged.connect(self.refresh_ui)

        self.b_yes.clicked.connect(lambda x: self.next_word('yes'))
        self.b_no.clicked.connect(lambda x: self.next_word('no'))
        self.b_to_eb.clicked.connect(lambda x: self.next_word('to_eb'))
        self.b_trash.clicked.connect(lambda x: self.next_word('trash'))
        self.b_fn.installEventFilter(self)

        self.tabWidget.currentChanged.connect(self.page_changed)
        QShortcut(QKeySequence('Ctrl+1'), self).activated.connect(lambda: self.next_word('yes'))
        QShortcut(QKeySequence('Ctrl+2'), self).activated.connect(lambda: self.next_word('no'))
        QShortcut(QKeySequence('Ctrl+3'), self).activated.connect(lambda: self.toggle_answer())
        # QShortcut(QKeySequence('Ctrl+4'), self).activated.connect(lambda: self.next_word('later'))
        # QShortcut(QKeySequence('Ctrl+5'), self).activated.connect(lambda: self.next_word('trash'))

        self.e_eb_thresh.valueChanged.connect(lambda x: self.backend.set_setting(eb_thresh=x))
        self.e_newbie_thresh.valueChanged.connect(lambda x: self.backend.set_setting(newbie_thresh=x))
        self.e_newbie2eb_thresh.valueChanged.connect(lambda x: self.backend.set_setting(newbie2eb_thresh=x))

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                if obj == self.b_fn:
                    self.fn_button('left')
            elif event.button() == QtCore.Qt.RightButton:
                if obj == self.b_fn:
                    self.fn_button('right')
            elif event.button() == QtCore.Qt.MiddleButton:
                if obj == self.b_fn:
                    self.fn_button('middle')
        return QtCore.QObject.event(obj, event)

    def fn_button(self, button):
        """ Handles callback for Fn button """
        assert button in ['left', 'right', 'middle']
        if button == 'left':
            if self.answer_hidden:
                self.toggle_answer()
            else:
                self.next_word('yes')
        elif button == 'right':
            if self.answer_hidden:
                self.toggle_answer()
            else:
                self.next_word('no')
        elif button == 'middle':
            if self.answer_hidden:
                self.toggle_answer()
            else:
                self.next_word('to_eb')

    def page_changed(self, change):
        if change == 1:  # Table page
            self.backend.refresh_db_prediction()
            model = DataFrameModel(self.backend.get_eb())
            self.t_table_eb.setModel(model)
        elif change == 2:
            self.backend.refresh_db_prediction()
            model = DataFrameModel(self.backend.get_new())
            self.t_table_new.setModel(model)
        elif change == 3:
            version_str, eb_thresh, newbie_thresh, newbie2eb_thresh = self.backend.get_setting()
            self.t_version.setText(version_str)
            self.e_eb_thresh.setValue(eb_thresh)
            self.e_newbie_thresh.setValue(newbie_thresh)
            self.e_newbie2eb_thresh.setValue(newbie2eb_thresh)

    def toggle_answer(self, force_to=None):
        if force_to is None:
            if self.answer_hidden:
                self.answer_hidden = False
                self.b_show.setText('Hide')
                self.refresh_ui()
            else:
                self.answer_hidden = True
                self.b_show.setText('Show')
                self.refresh_ui()
        else:
            assert isinstance(force_to, bool)
            self.answer_hidden = force_to
            self.b_show.setText('Show' if force_to else 'Hide')
            self.refresh_ui()

    def next_word(self, result):
        # Post current result to backend
        self.backend.set_quiz_result(result, self.t_note.toPlainText())
        # Get next info from backend
        self.word, self.pron, self.mean, self.syn, self.ex, self.note, self.stat = self.backend.get_next_quiz()
        self.toggle_answer(force_to=True)


if __name__ == "__main__":
    sys.argv += ['--ignore-gpu-blacklist']  # Fix OpenGL Error for QWebEngineView on MacOS
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
