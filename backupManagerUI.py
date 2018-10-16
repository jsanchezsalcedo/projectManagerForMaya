import os
import time

import maya.cmds as cmds
from maya import OpenMayaUI as omui

import projectManager
reload(projectManager)

try:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance

except ImportError:
    from PySide import QtCore, QtGui, QtWidgets
    from shiboken import wrapInstance

mainWindow = None
__title__ = 'Backup Manager'
__version__ = 'v1.0.0'

print ' '
print ' > {} {}'.format(__title__,__version__)
print ' > by Jorge Sanchez Salcedo (2018)'
print ' > www.jorgesanchez-da.com'
print ' > jorgesanchez.da@gmail.com'
print ' '

directories = ['PRJ', 'DPT', 'DIR_A', 'DIR_B', 'DIR_C']

for dir in directories:
    try:
        os.getenv(dir)
    except TypeError:
        os.environ[dir] = None

def getMainWindow():
    ptr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(long(ptr), QtWidgets.QMainWindow)
    return mainWindow

class BackupManagerUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(BackupManagerUI, self).__init__(parent)

        self.setWindowTitle('{} {}'. format(__title__,__version__))
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setMinimumWidth(600)
        self.setMinimumHeight(425)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.directories = projectManager.ProjectManager()

        self.buildUI()

    def buildUI(self):
        mainLayout = QtWidgets.QVBoxLayout()

        filesLy = QtWidgets.QVBoxLayout()
        self.filesTableWidget = QtWidgets.QTableWidget()
        self.filesTableWidget.horizontalHeader().setVisible(True)
        self.filesTableWidget.verticalHeader().setVisible(False)
        self.filesTableWidget.setColumnCount(4)
        self.filesTableWidget.setColumnWidth(0, 260)
        self.filesTableWidget.setColumnWidth(1, 75)
        self.filesTableWidget.setColumnWidth(2, 90)
        self.filesTableWidget.setColumnWidth(3, 125)
        self.filesTableWidget.setHorizontalHeaderLabels(['Name', 'Version', 'Type', 'Date Modified'])

        self.filesTableWidget.setAlternatingRowColors(True)
        self.filesTableWidget.setSortingEnabled(True)
        self.filesTableWidget.setShowGrid(False)
        self.filesTableWidget.itemDoubleClicked.connect(self.openScene)
        filesLy.addWidget(self.filesTableWidget)
        mainLayout.addLayout(filesLy)

        self.setLayout(mainLayout)
        self.populate()

    def populate(self):
        self.filesTableWidget.clearContents()
        backupPath = self.directories.getBackups()
        backupFiles = self.directories.backupFiles()

        try:
            for i in backupFiles:
                filePath = os.path.join(backupPath, i)
                name, ext = os.path.splitext(i)
                name, ver = name.split('.')
                item = QtWidgets.QTableWidgetItem(name)
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

                itemVersion = ver
                version = QtWidgets.QTableWidgetItem(itemVersion)
                version.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

                itemType = str('ma File')
                type = QtWidgets.QTableWidgetItem(itemType)
                type.setFlags(QtCore.Qt.ItemIsEnabled)

                itemDate = str(time.strftime('%d/%m/%Y %H:%M', time.gmtime(os.path.getmtime(filePath))))
                date = QtWidgets.QTableWidgetItem(itemDate)
                date.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

                self.filesTableWidget.insertRow(0)
                self.filesTableWidget.setItem(0, 0, item)
                self.filesTableWidget.setItem(0, 1, version)
                self.filesTableWidget.setItem(0, 2, type)
                self.filesTableWidget.setItem(0, 3, date)

        except TypeError:
            pass

    def checkFileState(self):
        fileState = cmds.file(q=True, mf=True)
        if fileState == True:
            self.warningBoxUI()
        else:
            self.openScene()

    def warningBoxUI(self):
        warningBox = QtWidgets.QMessageBox()
        warningBox.setWindowTitle('Warning: Scene Not Saved')
        warningBox.setText('The file has been modified. Do you want to save changes?')
        warningSaveBtn = warningBox.StandardButton(QtWidgets.QMessageBox.Save)
        warningDiscardBtn = warningBox.StandardButton(QtWidgets.QMessageBox.Discard)
        warningCancelBtn = warningBox.StandardButton(QtWidgets.QMessageBox.Cancel)
        warningBox.setStandardButtons(warningSaveBtn | warningDiscardBtn | warningCancelBtn)
        warningBox.setDefaultButton(warningSaveBtn)
        warning = warningBox.exec_()

        if warning == warningSaveBtn:
            self.saveScene()
        elif warning == warningDiscardBtn:
            self.openScene()
        elif warning == warningCancelBtn:
            self.cancel()

    def openScene(self):
        backupPath = self.directories.getBackups()
        columns = self.filesTableWidget.columnCount()
        row = self.filesTableWidget.currentRow()
        for col in xrange(0, columns):
            name = self.filesTableWidget.item(row, 0)
            version = self.filesTableWidget.item(row, 1)
        sceneName = name.text() + '.' + version.text() + '.ma'
        path = os.path.join(backupPath, sceneName)
        cmds.file(path, o=True, f=True, typ='mayaAscii', op='v=0')

        print ' '
        print ' > You have opened your scene successfully.'
        print ' '

        self.close()

    def saveScene(self):
        cmds.file(s=True, f=True)
        self.openScene()
        print ' '
        print ' > You have saved your scene successfully.'
        print ' '
        self.close()

    def cancel(self):
        print ' '
        print ' > You have canceled the process successfully.'
        print ' '
        self.close()


def run():
    global mainWindow
    if not mainWindow or not cmds.window(mainWindow,q=True,e=True):
        mainWindow = BackupManagerUI(parent=getMainWindow())
    mainWindow.show()

