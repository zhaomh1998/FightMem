import sys
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtCore import QFileInfo, QTimer
from ui.FightMemPCUI import *
from ui.DataFrameView import DataFrameModel
import core
import parameter


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
        self.triangle = False
        self.star = False
        self.active_table = None
        self.hp_bar_timer = None

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
            assert isinstance(self.stat, str)
            self.t_stat.setText(self.stat)

        if self.star:
            self.b_star.setPixmap(QtGui.QPixmap('ui/star_filled.png'))
        else:
            self.b_star.setPixmap(QtGui.QPixmap('ui/star_empty.png'))
        if self.triangle:
            self.b_triangle.setPixmap(QtGui.QPixmap('ui/triangle_filled.png'))
        else:
            self.b_triangle.setPixmap(QtGui.QPixmap('ui/triangle_empty.png'))

        self.hp_bar.setMaximum(parameter.HP_FULL)
        self.repaint()

    def setup_callback(self):
        self.b_show.clicked.connect(lambda: self.toggle_answer())
        self.b_show_note.stateChanged.connect(self.refresh_ui)

        self.b_long.clicked.connect(lambda x: self.next_word('long'))
        self.b_bury.clicked.connect(lambda x: self.next_word('bury'))
        self.b_to_eb.clicked.connect(lambda x: self.next_word('to_eb'))
        self.b_trash.clicked.connect(lambda x: self.next_word('trash'))
        self.b_fn.installEventFilter(self)

        self.tabWidget.currentChanged.connect(self.page_changed)
        QShortcut(QKeySequence('Ctrl+1'), self).activated.connect(lambda: self.next_word('long'))
        QShortcut(QKeySequence('Ctrl+2'), self).activated.connect(lambda: self.next_word('bury'))
        QShortcut(QKeySequence('Ctrl+3'), self).activated.connect(lambda: self.toggle_answer())
        # QShortcut(QKeySequence('Ctrl+4'), self).activated.connect(lambda: self.next_word('later'))
        # QShortcut(QKeySequence('Ctrl+5'), self).activated.connect(lambda: self.next_word('trash'))

        self.e_eb_thresh.valueChanged.connect(lambda x: self.backend.set_setting(eb_thresh=x))
        self.e_newbie_thresh.valueChanged.connect(lambda x: self.backend.set_setting(newbie_thresh=x))
        self.e_newbie2eb_thresh.valueChanged.connect(lambda x: self.backend.set_setting(newbie2eb_thresh=x))
        self.e_gsheet_id.textChanged.connect(lambda: self.backend.set_setting(gsheet_id=self.e_gsheet_id.toPlainText()))
        self.t_table_learn.clicked.connect(self.table_learn_cb)
        self.b_sync_gsheet.clicked.connect(self.backend.sync_gs)

        for table in [self.t_table_learn, self.t_table_eb, self.t_table_new, self.t_table_trash, self.t_table_explore,
                      self.t_table_star, self.t_table_triangle]:
            table.doubleClicked.connect(self.query_knowledge)

        self.b_triangle.mousePressEvent = self.triangle_cb
        self.b_star.mousePressEvent = self.star_cb

        for hide_button in [self.b_hide_learn_sln, self.b_hide_learn_hs,
                            self.b_hide_eb, self.b_hide_new, self.b_hide_trash, self.b_hide_explore,
                            self.b_hide_star, self.b_hide_triangle]:
            hide_button.stateChanged.connect(lambda x: self.page_changed(self.tabWidget.currentIndex()))

        # HP Bar
        self.hp_bar_timer = QTimer()
        self.hp_bar_timer.timeout.connect(self.update_hp_bar)
        self.hp_bar_timer.start(100)

    def update_hp_bar(self):
        hp = self.backend.get_hp()
        self.hp_bar.setValue(hp)

    def triangle_cb(self, event):
        self.triangle = not self.triangle
        self.refresh_ui()

    def star_cb(self, event):
        self.star = not self.star
        self.refresh_ui()

    def table_learn_cb(self, item):
        row, col = item.row(), item.column()
        if col in [1, 2, 3]:
            word = self.active_table.iloc[row, 0]
            self.query_knowledge(word, switch_to_tab=-1)  # Get word selected in backend
            if col == 1:  # Yes
                self.next_word('yes')
            elif col == 2:
                self.next_word('no')
            elif col == 3:
                self.next_word('trash')
            else:
                raise RuntimeWarning('Unexpected column click!')

            self.page_changed(self.tabWidget.currentIndex())  # Refresh page
            self.repaint()

    def query_knowledge(self, item, switch_to_tab=0):
        """
        Query a knowledge
        :param item: If passed as str, directly search. Else if it's a QModelIndex, only query if it's at col=0
        :param switch_to_tab: Switch to which tab after query. -1 to not switch
        """
        if isinstance(item, str):
            word = item
        else:
            if item.column() != 0:
                return
            word = item.data()

        # TODO: Refactor to have get_knowledge and get_next coming from same query API
        self.word, self.pron, self.mean, self.syn, self.ex,\
            self.note, self.star, self.triangle, self.stat = self.backend.get_knowledge(word)
        if switch_to_tab >= 0:
            self.tabWidget.setCurrentIndex(switch_to_tab)
        self.toggle_answer(force_to=False)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.MouseButtonDblClick:
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
        if change == 1:  # Table Learn
            self.backend.refresh_db_prediction()
            self.active_table = self.backend.get_learn_df(hide_sln=self.b_hide_learn_sln.checkState(),
                                                          hide_high_score=self.b_hide_learn_hs.checkState())
            model = DataFrameModel(self.active_table)
            self.t_table_learn.setModel(model)
        if change == 2:  # Table page
            self.backend.refresh_db_prediction()
            model = DataFrameModel(self.backend.get_eb_df(self.b_hide_eb.checkState()))
            self.t_table_eb.setModel(model)
        elif change == 3:
            self.backend.refresh_db_prediction()
            model = DataFrameModel(self.backend.get_newbie_df(self.b_hide_new.checkState()))
            self.t_table_new.setModel(model)
        elif change == 4:
            model = DataFrameModel(self.backend.get_trash_df(self.b_hide_trash.checkState()))
            self.t_table_trash.setModel(model)
        elif change == 5:
            model = DataFrameModel(self.backend.get_knowledge_df(self.b_hide_explore.checkState()))
            self.t_table_explore.setModel(model)
        elif change == 6:
            model = DataFrameModel(self.backend.get_star_df(self.b_hide_star.checkState()))
            self.t_table_star.setModel(model)
        elif change == 7:
            model = DataFrameModel(self.backend.get_triangle_df(self.b_hide_triangle.checkState()))
            self.t_table_triangle.setModel(model)
        elif change == 8:
            version_str, eb_thresh, newbie_thresh, newbie2eb_thresh, gsheet_id = self.backend.get_setting()
            self.t_version.setText(version_str)
            self.e_eb_thresh.setValue(eb_thresh)
            self.e_newbie_thresh.setValue(newbie_thresh)
            self.e_newbie2eb_thresh.setValue(newbie2eb_thresh)
            self.e_gsheet_id.setPlainText(gsheet_id)

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
        self.backend.set_quiz_result(result, self.t_note.toPlainText(), self.star, self.triangle)
        # Get next info from backend
        self.word, self.pron, self.mean, self.syn, self.ex, \
            self.note, self.star, self.triangle, self.stat = self.backend.get_next_quiz(self.e_mode.currentText())
        self.toggle_answer(force_to=True)


if __name__ == "__main__":
    sys.argv += ['--ignore-gpu-blacklist']  # Fix OpenGL Error for QWebEngineView on MacOS
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
