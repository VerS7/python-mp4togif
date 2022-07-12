# -*- coding: utf-8 -*-
import tkinter as tk
import locvar
from PyQt5.Qt import *
from mp4togif import Ui_Program
from tkinter import filedialog
from gifThreading import Thread


class MainWindow(QMainWindow, Ui_Program):
    def __init__(self):
        """Конструктор программы"""
        super(MainWindow, self).__init__()
        """Интерфейс"""
        self.ui = Ui_Program()
        self.ui.setupUi(self)
        """Локализация"""
        self.localize = None
        self.setWindowTitle(locvar.LocalEN.titleStr)
        self.errorMsg = locvar.LocalEN.errorStr
        self.doneMsg = locvar.LocalEN.doneStr
        self.creatMsg = locvar.LocalEN.creatStr
        self.rtwMsg = locvar.LocalEN.rtwStr
        """Объект класса Tkinter для работы с filedialog"""
        tkobject = tk.Tk()
        tkobject.withdraw()
        """Кнопки"""
        self.ui.browse.clicked.connect(lambda: self.browse())
        self.ui.save.clicked.connect(lambda: self.save_to())
        self.ui.convert.clicked.connect(lambda: self.make_gif())
        self.ui.localization.clicked.connect(lambda: self.switch())
        """Ползунки"""
        self.ui.frame_slider.setMinimum(1)
        self.ui.frame_slider.setMaximum(40)
        self.ui.frame_slider.valueChanged.connect(lambda: self.ui.frame_count.setText(str(self.ui.frame_slider.value()*10)))
        self.ui.compr_label.setMaximum(10)
        self.ui.compr_label.valueChanged.connect(lambda: self.ui.cmp_count.setText(str(self.ui.compr_label.value())))
        """Многозадачность"""
        self.process_thread = Thread()
        self.process_thread.finished.connect(self._finished)

    def switch(self):
        """Сменить локализацию"""
        try:
            if self.ui.localization.text() == 'EN':
                self.localize = locvar.LocalRU
                self.ui.localization.setText('RU')
            else:
                self.localize = locvar.LocalEN
                self.ui.localization.setText('EN')
            self.setWindowTitle(self.localize.titleStr)
            self.ui.browse.setText(self.localize.browseStr)
            self.ui.save.setText(self.localize.saveStr)
            self.ui.convert.setText(self.localize.convertStr)
            self.ui.gif_label.setText(self.localize.giflocStr)
            self.ui.mp4_label.setText(self.localize.mp4locStr)
            self.ui.fd_label.setText(self.localize.framedurStr)
            self.ui.cmp_label.setText(self.localize.comprStr)
            self.ui.statusLabel.setText(self.localize.rtwStr)
        except Exception as e:
            print(e)

    def browse(self):
        """Открыть filedialog для видео"""
        try:
            self.process_thread.video_path = filedialog.askopenfilename()
            self.ui.filePath.setText(self.process_thread.video_path)
            print(self.process_thread.video_path)
        except:
            self.ui.statusLabel.setText(self.errorMsg)

    def save_to(self):
        """Открыть filedialog для сохранения"""
        try:
            self.process_thread.save_path = filedialog.askdirectory()
            self.ui.savePath.setText(self.process_thread.save_path)
            print(self.process_thread.save_path)
        except:
            self.ui.statusLabel.setText(self.errorMsg)

    def make_gif(self):
        """Создать гифку по параметрам"""
        try:
            if not self.process_thread.video_path and self.process_thread.save_path:
                return
            self.ui.statusLabel.setText(self.creatMsg)
            self.process_thread.compression = self.ui.compr_label.value()
            self.process_thread.frame_duration = self.ui.frame_slider.value()*10
            self.process_thread.start()
        except:
            self.ui.statusLabel.setText(self.errorMsg)

    def _finished(self):
        """Оповещение в реальном времени"""
        self.ui.statusLabel.setText(self.doneMsg)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
