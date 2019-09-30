import sys
from PyQt5 import Qt, QtWidgets, QtCore, QtGui
import mainwindow
import textract
import re

class MainWindow(QtWidgets.QMainWindow):

    filters = ['*.doc', '*.docx', '*.xls', '*.xlsx', '*.ppt', '*.pptx', '*.txt', '*.pdf', '*.odt', '*.ods', '*.odp']
    tableheader = ['Filename', 'Size', 'Date', 'Path', 'Text']
    talblemodel = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.searchInLE.setText(QtCore.QDir.currentPath())
        self.ui.recurseCB.setChecked(True)

        # Create a text completer for searchInLE
        dircompleter = QtWidgets.QCompleter(self.ui.searchInLE)
        dircompleterfsmodel = QtWidgets.QFileSystemModel(dircompleter)
        dircompleterfsmodel.setRootPath(QtCore.QDir.currentPath())
        dircompleterfsmodel.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)
        dircompleter.setModel(dircompleterfsmodel)
        dircompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.ui.searchInLE.setCompleter(dircompleter)

        # Setup the model for the table view
        self.tablemodel = QtGui.QStandardItemModel()
        self.tablemodel.setHorizontalHeaderLabels(self.tableheader)

        self.ui.resultsWidget.setModel(self.tablemodel)
        self.ui.resultsWidget.setSortingEnabled(True)
        self.ui.resultsWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

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
            self.tablemodel.clear()
            self.tablemodel.setHorizontalHeaderLabels(self.tableheader)
            it = QtCore.QDirIterator(dir)
            if self.ui.recurseCB.isChecked():
                it = QtCore.QDirIterator(dir, QtCore.QDirIterator.Subdirectories)
            i = 0
            while it.hasNext():
                it.next()
                addtoresults = True
                foundText = ''
                if self.ui.searchTextLE.text():
                    text = str(textract.process(it.filePath()))
                    print(text)
                    searchText = self.ui.searchTextLE.text().lower()
                    found = False
                    for line in text.split(sep='\\n'):
                        if searchText in line.lower():
                            print(line)
                            found = True
                            foundText = line
                            break
                    if not found:
                        print('NoMatch!')
                        addtoresults = False

                if addtoresults:
                    fileInfo = it.fileInfo()
                    #self.ui.resultsWidget.insertRow(i)
                    item1 = QtGui.QStandardItem()
                    item1.setData(fileInfo.fileName(), QtCore.Qt.DisplayRole)
                    item2 = QtGui.QStandardItem()
                    item2.setData(fileInfo.size(), QtCore.Qt.DisplayRole)
                    item3 = QtGui.QStandardItem()
                    item3.setData(fileInfo.lastModified(), QtCore.Qt.DisplayRole)
                    item4 = QtGui.QStandardItem()
                    item4.setData(fileInfo.path(), QtCore.Qt.DisplayRole)
                    item5 = QtGui.QStandardItem()
                    item5.setData(foundText, QtCore.Qt.DisplayRole)
                    newrow = [item1, item2, item3, item4, item5]
                    self.tablemodel.appendRow(newrow)
                i += 1
            print(i)

app = QtWidgets.QApplication(sys.argv)

my_mainWindow = MainWindow()
my_mainWindow.show()

sys.exit(app.exec_())
