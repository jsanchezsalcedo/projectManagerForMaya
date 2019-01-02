import os
import time

import maya.cmds as cmds
from maya import OpenMayaUI as omui

import projectManager
reload(projectManager)

try:
    from PySide2 import QtCore, QtWidgets, QtGui
    from shiboken2 import wrapInstance

except ImportError:
    from PySide import QtCore, QtGui, QtWidgets
    from shiboken import wrapInstance

mainWindow = None
__title__ = 'Project Manager'
__version__ = 'v2.2.1'

print ' '
print ' > {} {}'.format(__title__,__version__)
print ' > by Jorge Sanchez Salcedo (2019)'
print ' > www.jorgesanchez-da.com'
print ' > jorgesanchez.da@gmail.com'
print ' '

directories = ['PRJ', 'DIR_A', 'DIR_B', 'DIR_C', 'DPT']

for dir in directories:
    try:
        os.getenv(dir)
    except TypeError:
        os.environ[dir] = None

def getMainWindow():
    ptr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(long(ptr), QtWidgets.QMainWindow)
    return mainWindow

class ProjectManagerUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ProjectManagerUI, self).__init__(parent)

        self.setWindowTitle('{} {}'.format(__title__, __version__))
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setMinimumWidth(640)
        self.setMinimumHeight(425)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.directories = projectManager.ProjectManager()
        self.root = self.directories.projectsRoot()
        self.projects = self.directories.projectsDir()
        self.directoryA = self.directories.directoryA()
        self.directoryB = self.directories.directoryB()
        self.directoryC = self.directories.directoryC()
        self.departments = self.directories.departmentsDir()
        self.projectPath, self.filesPath = self.directories.getProject()

        self.buildUI()

    def buildUI(self):
        mainLayout = QtWidgets.QVBoxLayout()

        rootLy = QtWidgets.QHBoxLayout()

        self.rootLe = QtWidgets.QLineEdit()
        self.rootLe.setText(self.root)
        self.rootLe.setEnabled(False)
        self.rootBtn = QtWidgets.QPushButton('Browse')
        self.rootBtn.setEnabled(False)
        rootLy.addWidget(self.rootLe)
        rootLy.addWidget(self.rootBtn)

        projectLy = QtWidgets.QHBoxLayout()

        self.projectCb = QtWidgets.QComboBox()
        self.projectCb.addItems(self.projects)
        self.projectCb.setCurrentText(os.getenv('PRJ'))
        self.projectCb.currentTextChanged.connect(self.updateProject)

        self.directoryACB = QtWidgets.QComboBox()
        self.directoryACB.addItems(self.directoryA)
        self.directoryACB.setCurrentText(os.getenv('DIR_A'))
        self.directoryACB.currentTextChanged.connect(self.updateDirA)

        for i in (self.projectCb, self.directoryACB):
            projectLy.addWidget(i)

        directoriesLy = QtWidgets.QHBoxLayout()

        self.directoryBCB = QtWidgets.QComboBox()
        self.directoryBCB.setMinimumWidth(210)
        self.directoryBCB.addItems(self.directoryB)
        self.directoryBCB.setCurrentText(os.getenv('DIR_B'))
        self.directoryBCB.currentTextChanged.connect(self.updateDirB)

        self.directoryCCB = QtWidgets.QComboBox()
        self.directoryCCB.setMinimumWidth(210)
        self.directoryCCB.addItems(self.directoryC)
        self.directoryCCB.setCurrentText(os.getenv('DIR_C'))
        self.directoryCCB.currentTextChanged.connect(self.updateDirC)

        self.departmentCb = QtWidgets.QComboBox()
        self.departmentCb.setMinimumWidth(210)
        self.departmentCb.addItems(self.departments)
        self.departmentCb.setCurrentText(os.getenv('DPT'))
        self.departmentCb.currentTextChanged.connect(self.updateDepartment)

        for i in (self.directoryBCB, self.directoryCCB, self.departmentCb):
            directoriesLy.addWidget(i)

        filesLy = QtWidgets.QVBoxLayout()
        self.filesTableWidget = QtWidgets.QTableWidget()
        self.filesTableWidget.horizontalHeader().setVisible(True)
        self.filesTableWidget.verticalHeader().setVisible(False)
        self.filesTableWidget.setColumnCount(3)
        self.filesTableWidget.setColumnWidth(0, 375)
        self.filesTableWidget.setColumnWidth(1, 90)
        self.filesTableWidget.setColumnWidth(2, 160)
        self.headerLabels = (['Name', 'Type', 'Date Modified'])
        self.filesTableWidget.setHorizontalHeaderLabels(self.headerLabels)

        self.filesTableWidget.setAlternatingRowColors(True)
        self.filesTableWidget.setSortingEnabled(True)
        self.filesTableWidget.setShowGrid(False)
        self.filesTableWidget.itemDoubleClicked.connect(self.checkFileState)
        filesLy.addWidget(self.filesTableWidget)

        mainLayout.addLayout(rootLy)
        mainLayout.addLayout(projectLy)
        mainLayout.addLayout(directoriesLy)
        mainLayout.addLayout(filesLy)

        self.setLayout(mainLayout)
        self.setProject()

    def updateProject(self):
        os.environ['PRJ'] = self.projectCb.currentText()
        dirA = self.directories.directoryA()
        self.directoryACB.clear()
        try:
            self.directoryACB.addItems(dirA)
        except TypeError:
            pass

    def updateDirA(self):
        os.environ['DIR_A'] = self.directoryACB.currentText()
        dirB = self.directories.directoryB()
        self.directoryBCB.clear()
        try:
            self.directoryBCB.addItems(dirB)
        except TypeError:
            pass

    def updateDirB(self):
        os.environ['DIR_B'] = self.directoryBCB.currentText()
        dirC = self.directories.directoryC()
        self.directoryCCB.clear()
        try:
            self.directoryCCB.addItems(dirC)
        except TypeError:
            pass

    def updateDirC(self):
        os.environ['DIR_C'] = self.directoryCCB.currentText()
        departments = self.directories.departmentsDir()
        self.departmentCb.clear()
        try:
            self.departmentCb.addItems(departments)
        except TypeError:
            pass

    def updateDepartment(self):
        os.environ['DPT'] = self.departmentCb.currentText()
        try:
            self.setProject()
        except TypeError:
            pass

    def setProject(self):
        projectPath, filesPath = self.directories.getProject()

        try:
            cmds.workspace(dir=projectPath)
            cmds.workspace(projectPath, o=True)
            cmds.workspace(q=True, sn=True)
            cmds.workspace(ua=True)

        except RuntimeError:
            pass

        self.populate()

    def populate(self):
        self.filesTableWidget.clearContents()
        projectPath, filesPath = self.directories.getProject()
        mayaFiles = self.directories.mayaFiles()

        try:
            for i in mayaFiles:
                filePath = os.path.join(filesPath, i)
                name, ext = os.path.splitext(i)
                item = QtWidgets.QTableWidgetItem(name)
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

                itemType = str('ma File')
                type = QtWidgets.QTableWidgetItem(itemType)
                type.setFlags(QtCore.Qt.ItemIsEnabled)

                itemDate = str(time.strftime('%d/%m/%Y %H:%M', time.gmtime(os.path.getmtime(filePath))))
                date = QtWidgets.QTableWidgetItem(itemDate)
                date.setFlags(QtCore.Qt.ItemIsEnabled)

                self.filesTableWidget.insertRow(0)
                self.filesTableWidget.setItem(0, 0, item)
                self.filesTableWidget.setItem(0, 1, type)
                self.filesTableWidget.setItem(0, 2, date)
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
        melFiles = self.directories.melFiles()
        try:
            if 'workspace.mel' not in melFiles:
                from projectUtilities import createWorkspace
                createWorkspace()
                currentScene = self.filesTableWidget.currentItem()
                getFileName = currentScene.text()
                sceneName = getFileName + '.ma'
                cmds.file(sceneName, o=True, f=True, typ='mayaAscii', op='v=0')
            else:
                currentScene = self.filesTableWidget.currentItem()
                getFileName = currentScene.text()
                sceneName = getFileName + '.ma'
                cmds.file(sceneName, o=True, f=True, typ='mayaAscii', op='v=0')

        except RuntimeError:
            pass

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
        mainWindow = ProjectManagerUI(parent=getMainWindow())
    mainWindow.show()
