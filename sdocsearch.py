import sys
from PyQt5 import QtWidgets, QtCore
import mainwindow

class MainWindow(QtWidgets.QMainWindow):

    filters = ['*.doc', '*.docx', '*.xls', '*.xlsx', '*.ppt', '*.pptx', '*.txt', '*.pdf', '*.odt', '*.ods', '*.odp']

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.searchInLE.setText(QtCore.QDir.currentPath())
        self.ui.recurseCB.setChecked(True)
        self.ui.resultsWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.resultsWidget.setSortingEnabled(True)

        # Create a text completer for searchInLE
        dircompleter = QtWidgets.QCompleter(self.ui.searchInLE)
        dircompleterfsmodel = QtWidgets.QFileSystemModel(dircompleter)
        dircompleterfsmodel.setRootPath(QtCore.QDir.currentPath())
        dircompleterfsmodel.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)
        dircompleter.setModel(dircompleterfsmodel)
        dircompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.ui.searchInLE.setCompleter(dircompleter)

        self.ui.dirBtn.clicked.connect(self.dirBtnClicked)
        self.ui.searchBtn.clicked.connect(self.searchBtnClicked)

    def dirBtnClicked(self):
        newdir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Directory', QtCore.QDir.currentPath())
        if newdir:
            self.ui.searchInLE.setText(newdir)

    def searchBtnClicked(self):
        dir = QtCore.QDir(self.ui.searchInLE.text())
        dir.setNameFilters(self.filters)
        if not dir.exists():
            QtWidgets.QMessageBox.warning(None,"Cannot search!","Directory "+self.ui.searchInLE.text()+"doesn't exist")
        else:
            self.ui.resultsWidget.clearContents()
            it = QtCore.QDirIterator(dir)
            if self.ui.recurseCB.isChecked():
                it = QtCore.QDirIterator(dir, QtCore.QDirIterator.Subdirectories)
            i = 0
            while it.hasNext():
                it.next()
                fileInfo = it.fileInfo()
                self.ui.resultsWidget.insertRow(i)
                self.ui.resultsWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(fileInfo.fileName()))
                self.ui.resultsWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(fileInfo.size())))
                self.ui.resultsWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(fileInfo.lastModified().toString()))
                self.ui.resultsWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(fileInfo.path()))
                i += 1
            print(i)

app = QtWidgets.QApplication(sys.argv)

my_mainWindow = MainWindow()
my_mainWindow.show()

sys.exit(app.exec_())
