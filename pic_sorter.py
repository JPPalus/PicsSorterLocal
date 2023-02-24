import os
import sys
import random
import shutil
import subprocess
import webbrowser
import platform
from cv2 import imread
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QCheckBox,
    QLineEdit,
    QLabel,
    QScrollArea,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pics Sorter")
        self.window_layout = QHBoxLayout()
        self.page_layout = QVBoxLayout()
        self.top_button_layout = QHBoxLayout()
        self.bottom_button_layout = QHBoxLayout()
        self.class_layout = QVBoxLayout()
        self.picture_layout = QHBoxLayout()
        self.folders_info_layout = QHBoxLayout()
        self.info_layout = QHBoxLayout()

        self.dir_path_to_sort = ""
        self.dir_path_destination = ""
        self.media_list = []
        self.class_list = []

        # New class edit field
        self.class_input = QLineEdit()
        self.top_button_layout.addWidget(self.class_input)

        # Class checkboxes
        for class_folder in self.class_list:
            self.class_layout.addWidget(QCheckBox(class_folder))

        # Sort button
        self.sort_button = QPushButton("Sort")
        self.sort_button.clicked.connect(self.Sort)
        self.top_button_layout.addWidget(self.sort_button)

        # Skip button
        self.skip_button = QPushButton("Skip")
        self.skip_button.clicked.connect(self.Skip)
        self.top_button_layout.addWidget(self.skip_button)

        # Open in browser button
        self.browser_button = QPushButton("Open in browser")
        self.browser_button.clicked.connect(self.Open_in_Browser)
        self.top_button_layout.addWidget(self.browser_button)

        # Choose folder to sort button
        self.choose_folder_to_sort = QPushButton("Select Folder to Sort")
        self.choose_folder_to_sort.setToolTip("Select Folder to Sort")
        self.choose_folder_to_sort.setStatusTip("Select Folder to Sort")
        self.choose_folder_to_sort.clicked.connect(self.Choose_folder_to_sort)
        self.bottom_button_layout.addWidget(self.choose_folder_to_sort)

        # Choose destination folder button
        self.choose_destination_folder = QPushButton("Select Destination Folder")
        self.choose_destination_folder.setToolTip("Select Destination Folder")
        self.choose_destination_folder.setStatusTip("Select Destination Folder")
        self.choose_destination_folder.clicked.connect(self.Choose_destination_folder)
        self.bottom_button_layout.addWidget(self.choose_destination_folder)

        # File name info
        self.file_label = QLabel()
        self.info_layout.addWidget(self.file_label)

        # File resolution info
        self.file_resolution = QLabel()
        self.info_layout.addWidget(self.file_resolution)

        # Folder to sort info
        self.folder_to_sort_label = QLabel()
        self.folder_to_sort_label.setText(f"Sorting folder : {self.dir_path_to_sort}")
        self.folders_info_layout.addWidget(self.folder_to_sort_label)

        # Destination folder name info
        self.destination_folder_label = QLabel()
        self.destination_folder_label.setText(f"Destination folder : {self.dir_path_destination}")
        self.folders_info_layout.addWidget(self.destination_folder_label)

        # Media
        self.scroll_area = QScrollArea()
        self.label = QLabel()
        self.movie = QMovie()
        self.label.setMovie(self.movie)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setSizeAdjustPolicy(self.scroll_area.SizeAdjustPolicy.AdjustToContents)
        self.picture_layout.addWidget(self.scroll_area)

        # Open the file when clicked
        self.scroll_area.mouseReleaseEvent = lambda f: subprocess.Popen(
            self.movie.fileName(), shell=True).stderr

        self.page_layout.addLayout(self.top_button_layout)
        self.page_layout.addLayout(self.info_layout)
        self.page_layout.addLayout(self.picture_layout)
        self.page_layout.addLayout(self.folders_info_layout)
        self.page_layout.addLayout(self.bottom_button_layout)
        self.window_layout.addLayout(self.page_layout)
        self.window_layout.addLayout(self.class_layout)
        self.container = QWidget()
        self.container.setLayout(self.window_layout)
        self.setCentralWidget(self.container)

        self.sort_button.setEnabled(False)
        self.browser_button.setEnabled(False)
        self.skip_button.setEnabled(False)
        self.class_input.setEnabled(False)

        if not len(self.media_list):
            self.movie.setFileName("")
            self.movie.stop()
            self.label.adjustSize()

    def Choose_folder_to_sort(self):
        # Obfuscation / 20
        self.dir_path_to_sort = p if (p := QFileDialog.getExistingDirectory(self, "Open Directory to sort", ".", QFileDialog.Option.ShowDirsOnly)) else (sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))
        self.folder_to_sort_label.setText(f"Sorting folder : {self.dir_path_to_sort}")
        self.media_list = [filename for filename in os.listdir(
            self.dir_path_to_sort) if os.path.isfile(os.path.join(self.dir_path_to_sort, filename))]
        self.sort_button.setEnabled(True)
        self.browser_button.setEnabled(True)
        self.skip_button.setEnabled(True)
        self.class_input.setEnabled(True)
        self.Init_media()
        self.Reset_checkboxes()

    def Choose_destination_folder(self):
        self.dir_path_destination = p if (p := QFileDialog.getExistingDirectory(self, "Open destintion directory", ".", QFileDialog.Option.ShowDirsOnly)) else (sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))
        self.destination_folder_label.setText(f"Destination folder : {self.dir_path_destination}")
        self.class_list = sorted([dirname for dirname in os.listdir(self.dir_path_destination) if os.path.isdir(
            os.path.join(self.dir_path_destination, dirname)) and dirname != 'Done'])
        for i in range(self.class_layout.count()): 
            self.class_layout.itemAt(i).widget().deleteLater()
        for class_folder in self.class_list:
            self.class_layout.addWidget(QCheckBox(class_folder))
        self.Reset_checkboxes()

    def Skip(self):
        if len(self.media_list):
            self.movie.stop()
            choice = random.choice(self.media_list)
            img = imread(self.dir_path_to_sort + os.path.sep + choice)
            self.movie.setFileName(self.dir_path_to_sort + os.path.sep + choice)
            self.file_label.setText(f"Filename : {choice}")
            if (img := imread(self.dir_path_to_sort + os.path.sep + choice)) is not None:
                self.file_resolution.setText(f"Resolution : {img.shape[1]} x {img.shape[0]}")
            else:
                self.file_resolution.setText("")
            self.movie.start()
            self.label.adjustSize()
        else:
            self.movie.setFileName("")
            self.movie.stop()
            self.sort_button.setEnabled(False)
            self.browser_button.setEnabled(False)
            self.skip_button.setEnabled(False)
            self.class_input.setEnabled(False)
            self.file_label.setText("No media to sort !")
        self.Reset_checkboxes()
            
    def Reset_checkboxes(self):
        for i in range(self.class_layout.count()):
            widget = self.class_layout.itemAt(i).widget()
            if isinstance(widget, QCheckBox):
                widget.setChecked(False)

    def Open_in_Browser(self):
        if not platform.system() == 'Windows':
            webbrowser.open_new_tab(f"file:///{self.movie.fileName()}")
        else:
            subprocess.Popen(["start", "firefox", f"file:///{self.movie.fileName()}"], shell=True).stderr

    def Sort(self):
        # New picture
        current_picture = self.movie.fileName()
        self.Init_media()
        self.label.adjustSize()

        # Create classes folders if need be
        if self.class_input.text() != "":
            classes = self.class_input.text().split()
            for clas in classes:
                if not os.path.isdir(os.path.join(self.dir_path_destination, clas)):
                    os.mkdir(self.dir_path_destination + os.path.sep + clas)
                shutil.copyfile(current_picture, self.dir_path_destination + os.path.sep + clas + os.path.sep + os.path.split(current_picture)[1])
            self.class_input.clear()
            for i in range(self.class_layout.count()): 
                self.class_layout.itemAt(i).widget().deleteLater()
            for class_folder in self.class_list:
                self.class_layout.addWidget(QCheckBox(class_folder))

        # Copy the file in each class folder
        for i in range(self.class_layout.count()):
            widget = self.class_layout.itemAt(i).widget()
            if isinstance(widget, QCheckBox):
                if widget.isChecked():
                    shutil.copyfile(current_picture, self.dir_path_destination + os.path.sep + widget.text() + os.path.sep + os.path.split(current_picture)[1])
                    widget.setChecked(False)

        if not os.path.isdir(os.path.join(self.dir_path_destination, 'Done')):
            os.mkdir(self.dir_path_destination + os.path.sep + 'Done')
        os.rename(current_picture, self.dir_path_destination + '/' +'Done' + '/' + os.path.split(current_picture)[1])

    def Init_media(self):
        # Select a random picture
        if len(self.media_list):
            self.movie.stop()
            choice = random.choice(self.media_list)
            img = imread(self.dir_path_to_sort + os.path.sep + choice)
            self.media_list.remove(choice)
            self.movie.setFileName(
                self.dir_path_to_sort + os.path.sep + choice)
            self.file_label.setText(choice)
            if (img := imread(self.dir_path_to_sort + os.path.sep + choice)) is not None:
                self.file_resolution.setText(f"{img.shape[1]} x {img.shape[0]}")
            else:
                self.file_resolution.setText("")
            self.movie.start()
            self.label.adjustSize()
        else:
            self.movie.stop()
            self.movie.setFileName("")
            self.file_resolution.setText("")
            self.sort_button.setEnabled(False)
            self.browser_button.setEnabled(False)
            self.skip_button.setEnabled(False)
            self.class_input.setEnabled(False)
            self.file_label.setText("No media to sort !")
        self.Reset_checkboxes()


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('WindowsXP')
    window = MainWindow()
    window.show()
    app.exec()
