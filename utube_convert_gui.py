import sys
import utube_downloader

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtGui import QIcon

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QStandardPaths
from PyQt5.QtCore import QFile

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.label_progress = QLabel("remain data 0", self)
        self.edit_url_input = QLineEdit(self)
        self.edit_output_dir = QLineEdit(self)
        self.edit_output_dir.setText(QStandardPaths.writableLocation (QStandardPaths.StandardLocation.MoviesLocation))
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('Youtube media convert')

        layout_main = QVBoxLayout()
        layout_main.setAlignment(Qt.AlignTop)
      
        self.edit_url_input.setPlaceholderText("input youtube url")
        layout_main.addWidget(self.edit_url_input)
        
        layout_output_path = QHBoxLayout()
        btn_find_save_dir = QPushButton("Find directory", self)
        btn_find_save_dir.clicked.connect(self.select_save_directory)
        layout_output_path.addWidget(btn_find_save_dir)

        layout_output_path.addWidget(self.edit_output_dir)
        layout_main.addLayout(layout_output_path)

        btn_download = QPushButton("Download", self)
        btn_download.clicked.connect(self.slot_download)
        layout_main.addWidget(btn_download)

        layout_progress = QHBoxLayout()
        layout_progress.setAlignment(Qt.AlignRight)
     
        layout_progress.addWidget(self.label_progress)

        layout_main.addLayout(layout_progress)

        self.setLayout(layout_main)

        self.move(300, 300)
        self.resize(400, 200)
        self.show()

    def select_save_directory(self):
        str_file_path = QFileDialog.getExistingDirectory(self, "Save Directory")
        self.edit_output_dir.setText(str_file_path)

    def slot_download(self):
        str_url = self.edit_url_input.text()
        if 0 == len(str_url):
            msg = QMessageBox.question(self, "error", "Empty url, please input youtube url", QMessageBox.Yes)
            return
        
        str_output_path = self.edit_output_dir.text()
        if 0 == len(str_output_path):
            msg = QMessageBox.question(self, "error", "Output path is not specified. Please enter the path.", QMessageBox.Yes)
            return

        if False == QFile.exists(str_output_path):
            msg = QMessageBox.question(self, "error", "Invalid output path.", QMessageBox.Yes)
            return

        utube_downloader.download_youtube(str_url, str_output_path, self.callbak_progress)

    def callbak_progress(self, stream, chunk, remain):
        self.label_progress.setText("remain data " + str(remain))
        self.label_progress.repaint()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())