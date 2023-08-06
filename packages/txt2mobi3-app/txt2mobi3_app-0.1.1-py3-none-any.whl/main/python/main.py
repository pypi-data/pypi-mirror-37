#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog, QFileDialog, 
    QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton)
from PyQt5.QtCore import pyqtSlot, QDir
from PyQt5.QtGui import QIntValidator
from txt2mobi3 import txt2mobi3


class Utility:
    @staticmethod
    def create_h3box_layout(label_str, line_edit_def_str, line_edit_min_width, push_button_str):
        label = QLabel(label_str)
        edit_box = QLineEdit(line_edit_def_str)
        edit_box.setMinimumWidth(line_edit_min_width)
        push_button = QPushButton(push_button_str)
        h3box_layout = QHBoxLayout()
        h3box_layout.addWidget(label)
        h3box_layout.addWidget(edit_box)
        h3box_layout.addStretch(1)
        h3box_layout.addWidget(push_button)
        return (h3box_layout, edit_box, push_button)

    
    @staticmethod
    def open_file_name_dialog(parent, caption, def_dir, filter_types):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            parent, 
            caption, 
            def_dir, 
            '{};;All Files (*)'.format(filter_types) if filter_types else 'All Files(*)', 
            options=options)
        return file_name


    @staticmethod
    def show_msg_dialog(parent, title, text, detailed_text):
        msg_dialog = QMessageBox(parent)
        msg_dialog.setWindowTitle(title)
        msg_dialog.setText(text)
        msg_dialog.setDetailedText(detailed_text)
        msg_dialog.exec()


class Txt2Mobi3Ui(QDialog):
    def __init__(self):
        super(Txt2Mobi3Ui, self).__init__()

        self._txt2mobi3 = txt2mobi3.Txt2Mobi3()
        self._txt2mobi3.initialize()

        txt_layout, self._txt_edit_box, txt_push_button = \
            Utility.create_h3box_layout('txt文件', None, 500, '浏览')
        txt_push_button.clicked.connect(self._on_txt_clicked)
        mobi_layout, self._mobi_edit_box, mobi_push_button = \
            Utility.create_h3box_layout('mobi输出目录', None, 450, '浏览')
        mobi_push_button.clicked.connect(self._on_mobi_clicked)
        title_author_layout, self._title_edit_box, self._author_edit_box = \
            self._create_title_author_layout()
        cover_img_layout, self._cover_img_edit_box, cover_img_button = \
            Utility.create_h3box_layout(
                '封面图片', 
                self._txt2mobi3.get_config('def_cover_img'), 
                500, 
                '浏览')
        cover_img_button.clicked.connect(self._on_cover_img_clicked)
        config_button, dryrun_button, convert_button = self._create_action_buttons()
        config_button.clicked.connect(self._on_config_clicked)
        dryrun_button.clicked.connect(self._on_dryrun_clicked)
        convert_button.clicked.connect(self._on_convert_clicked)

        main_layout = QGridLayout()
        main_layout.addLayout(txt_layout, 0, 0, 1, 3)
        main_layout.addLayout(mobi_layout, 1, 0, 1, 3)
        main_layout.addLayout(title_author_layout, 2, 0, 1, 3)
        main_layout.addLayout(cover_img_layout, 3, 0, 1, 3)
        main_layout.addWidget(config_button, 4, 0)
        main_layout.addWidget(dryrun_button, 4, 1)
        main_layout.addWidget(convert_button, 4, 2)
        self.setLayout(main_layout)
        self.setWindowTitle('Txt2Mobi3 - 从txt到mobi')

        self._config_dialog = Txt2Mobi3ConfigUi(self._txt2mobi3)


    def _create_title_author_layout(self):
        title_label = QLabel('书名')
        title = QLineEdit('无题')
        title.setMinimumWidth(200)
        author_label = QLabel('作者')
        author = QLineEdit('佚名')
        author.setMinimumWidth(200)
        title_author_layout = QHBoxLayout()
        title_author_layout.addWidget(title_label)
        title_author_layout.addWidget(title)
        title_author_layout.addStretch(1)
        title_author_layout.addWidget(author_label)
        title_author_layout.addWidget(author)
        return (title_author_layout, title, author)


    def _create_action_buttons(self):
        config_button = QPushButton('配置')
        dryrun_button = QPushButton('测试')
        convert_button = QPushButton('转化')
        return (config_button, dryrun_button, convert_button)

    
    @pyqtSlot()
    def _on_txt_clicked(self):
        txt_path = Utility.open_file_name_dialog(
            self, 'txt文件路径', os.path.expanduser('~'), 'TXT Files (*.txt)')
        self._txt_edit_box.setText(txt_path)


    @pyqtSlot()
    def _on_mobi_clicked(self):
        mobi_path = QFileDialog.getExistingDirectory(self, 'mobi输出目录', 
            os.path.expanduser('~'))
        self._mobi_edit_box.setText(mobi_path)


    @pyqtSlot()
    def _on_cover_img_clicked(self):
        cover_img_path = Utility.open_file_name_dialog(
            self,
            '设置封面图片路径',
            os.path.dirname(self._txt2mobi3.get_config('def_cover_img')),
            'Image Files (*.png *.jpg *.bmp)')
        if cover_img_path:
            self._cover_img_edit_box.setText(cover_img_path)


    @pyqtSlot()
    def _on_config_clicked(self):
        self._config_dialog.show()


    def _get_book_params(self):
        if not self._txt_edit_box.text():
            Utility.show_msg_dialog(self, '错误', 'txt文件路径为空', '无')
            return None

        if not self._mobi_edit_box.text():
            Utility.show_msg_dialog(self, '错误', 'mobi文件输出目录为空', '无')
            return None

        book_params = {}
        book_params['txt_file'] = self._txt_edit_box.text()
        book_params['dest_dir'] = self._mobi_edit_box.text()

        if not self._cover_img_edit_box.text():
            Utility.show_msg_dialog(self, '警告', '封面图片路径为空', 
                '封面图片路径将被重置为默认路径{}'.format(self._txt2mobi3.get_config('def_cover_img')))
            self._cover_img_edit_box.setText(self._txt2mobi3.get_config('def_cover_img'))
            self._cover_img_edit_box.update()
        book_params['cover_img_file'] = self._cover_img_edit_box.text()

        if not self._title_edit_box.text():
            Utility.show_msg_dialog(self, '警告', '书名为空', '书名将被重置为无题')
            self._title_edit_box.setText('无题')
            self._title_edit_box.update()
        book_params['title'] = self._title_edit_box.text()

        if not self._author_edit_box.text():
            Utility.show_msg_dialog(self, '警告', '作者为空', '作者将被重置为佚名')
            self._author_edit_box.setText('佚名')
            self._author_edit_box.update()
        book_params['author'] = self._author_edit_box.text()

        return book_params


    @pyqtSlot()
    def _on_dryrun_clicked(self):
        book_params = self._get_book_params()
        if book_params is None:
            return

        self._txt2mobi3.convert(True, book_params)
        Utility.show_msg_dialog(self, '信息', '转化预演成功', 
            '该预演会生成转化过程中的中间文件但不会调用KindleGen来生成最终的mobi文件')


    @pyqtSlot()
    def _on_convert_clicked(self):
        book_params = self._get_book_params()
        if book_params is None:
            return

        self._txt2mobi3.convert(False, book_params)
        Utility.show_msg_dialog(self, '信息', '转化成功', 
            '转化生成的mobi文件在{}'.format(book_params['dest_dir']))


class Txt2Mobi3ConfigUi(QDialog):
    def __init__(self, txt2mobi3):
        super(Txt2Mobi3ConfigUi, self).__init__()

        self._txt2mobi3 = txt2mobi3
        self._reload_configs()

        kindlegen_layout, self._kindlegen_edit_box, kindlegen_button = \
            Utility.create_h3box_layout(
                'KindleGen工具路径', self._def_kindlegen, 400, '浏览')
        kindlegen_button.clicked.connect(self._on_kindlegen_clicked)
        def_cover_img_layout, self._def_cover_img_edit_box, def_cover_img_button = \
            Utility.create_h3box_layout(
                '默认封面图片路径', self._def_cover_img, 450, '浏览')
        def_cover_img_button.clicked.connect(self._on_def_cover_img_button_clicked)
        chap_layout, self._chap_checkbox, self._max_chaps_edit_box = self._create_chap_layout()
        reload_button, reset_button, modify_button = self._create_action_buttons()
        reload_button.clicked.connect(self._on_reload_clicked)
        reset_button.clicked.connect(self._on_reset_clicked)
        modify_button.clicked.connect(self._on_modify_clicked)

        config_layout = QGridLayout()
        config_layout.addLayout(kindlegen_layout, 0, 0, 1, 3)
        config_layout.addLayout(def_cover_img_layout, 1, 0, 1, 3)
        config_layout.addLayout(chap_layout, 2, 0, 1, 4)
        config_layout.addWidget(reload_button, 3, 0)
        config_layout.addWidget(reset_button, 3, 1)
        config_layout.addWidget(modify_button, 3, 2)
        self.setLayout(config_layout)
        self.setWindowTitle('Txt2Mobi3 - 配置')

    def _reload_configs(self):
        self._def_kindlegen = self._txt2mobi3.get_config('kindlegen')
        self._def_cover_img = self._txt2mobi3.get_config('def_cover_img')
        self._chapterization = self._txt2mobi3.get_config('chapterization')
        self._max_chapter = self._txt2mobi3.get_config('max_chapter')

        
    def _create_chap_layout(self):
        chap_checkbox = QCheckBox('划分章节')
        chap_checkbox.setChecked(self._chapterization)
        chap_label = QLabel('最大章节数')
        int_validator = QIntValidator()
        max_chaps = QLineEdit(str(self._max_chapter))
        max_chaps.setValidator(int_validator)
        chap_layout = QHBoxLayout()
        chap_layout.addWidget(chap_checkbox)
        chap_layout.addStretch(1)
        chap_layout.addWidget(chap_label)
        chap_layout.addWidget(max_chaps)
        return (chap_layout, chap_checkbox, max_chaps)


    def _create_action_buttons(self):
        reload_button = QPushButton('载入')
        reset_button = QPushButton('重置')
        modify_button = QPushButton('修改')
        return (reload_button, reset_button, modify_button)


    @pyqtSlot()
    def _on_kindlegen_clicked(self):
        kindlegen_path = Utility.open_file_name_dialog(
            self, '设置KindleGen路径', os.path.dirname(self._def_kindlegen), '')
        if kindlegen_path:
            self._kindlegen_edit_box.setText(kindlegen_path)


    @pyqtSlot()
    def _on_def_cover_img_button_clicked(self):
        def_cover_img_path = Utility.open_file_name_dialog(
            self,
            '设置默认封面图片路径',
            os.path.dirname(self._def_cover_img),
            'Image Files (*.png *.jpg *.bmp)')
        if def_cover_img_path:
            self._def_cover_img_edit_box.setText(def_cover_img_path)


    def _refresh_config(self):
        self._kindlegen_edit_box.setText(self._def_kindlegen)
        self._kindlegen_edit_box.update()
        self._def_cover_img_edit_box.setText(self._def_cover_img)
        self._def_cover_img_edit_box.update()
        self._chap_checkbox.setChecked(self._chapterization)
        self._chap_checkbox.update()
        self._max_chaps_edit_box.setText(str(self._max_chapter))
        self._max_chaps_edit_box.update()


    @pyqtSlot()
    def _on_reload_clicked(self):
        self._reload_configs()
        self._refresh_config()


    @pyqtSlot()
    def _on_reset_clicked(self):
        self._txt2mobi3.reset_config()
        self._reload_configs()
        self._refresh_config()


    @pyqtSlot()
    def _on_modify_clicked(self):
        if not self._kindlegen_edit_box.text() or not self._def_cover_img_edit_box.text() or \
            not self._max_chaps_edit_box.text():
            Utility.show_msg_dialog(self, '错误', '配置修改错误', 
                'KindleGen工具路径或默认封面图片路径或最大章节数为空！')
            return

        self._def_kindlegen = self._kindlegen_edit_box.text()
        self._def_cover_img = self._def_cover_img_edit_box.text()
        self._chapterization = self._chap_checkbox.isChecked()
        self._max_chapter = self._max_chaps_edit_box.text()
        config = {'kindlegen': self._def_kindlegen, 
            'def_cover_img': self._def_cover_img,
            'chapterization': self._chapterization,
            'max_chapter': self._max_chapter}
        self._txt2mobi3.set_config(config)


class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
    def run(self):                              # 2. Implement run()
        self.app.setStyle('Fusion')
        main_ui = Txt2Mobi3Ui()
        main_ui.show()
        return self.app.exec()                  # 3. End run() with this line


def txt2mobi3_app():
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code)


if __name__ == '__main__':
    txt2mobi3_app()