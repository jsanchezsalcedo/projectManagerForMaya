import os
import time

import maya.cmds as cmds
from maya import OpenMayaUI as omui

import prm_core as core
import prm_utils as util

try:
    from PySide2 import QtCore, QtWidgets, QtGui
    from shiboken2 import wrapInstance

except ImportError:
    from PySide import QtCore, QtGui, QtWidgets
    from shiboken import wrapInstance

mainWindow = None
__title__ = 'Project Manager for Maya'
__version__ = 'v3.0.0'

print('')
print(' > {} {}' . format(__title__, __version__))
print(' > Jorge Sanchez Salcedo, 2020')
print(' > www.jorgesanchez-da.com')
print('')

def getMainWindow():
    ptr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(long(ptr), QtWidgets.QMainWindow)
    return mainWindow

class ProjectManagerUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ProjectManagerUI, self).__init__(parent)
        self.setWindowTitle('{} {}'.format(__title__, __version__))
        self.setMinimumWidth(640)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        core.ProjectManager().checkedFolders()
        self.buildUI()
        self.setProject()

    def buildUI(self):
        projectManagerWidget = QtWidgets.QWidget()
        mainLayout = QtWidgets.QVBoxLayout(projectManagerWidget)
        mainLayout.setContentsMargins(2,2,2,2)
        mainLayout.setAlignment(QtCore.Qt.AlignTop)

        rootFolderWidget = QtWidgets.QWidget()
        rootFolderLayout = QtWidgets.QHBoxLayout(rootFolderWidget)
        rootFolderLayout.setAlignment(QtCore.Qt.AlignTop)
        rootFolderLayout.setContentsMargins(2,2,2,2)

        self.rootFolder = QtWidgets.QLineEdit()
        self.rootFolder.setText(os.getenv('ROOT'))
        self.rootFolder.setEnabled(False)
        rootFolderLayout.addWidget(self.rootFolder)

        mainLayout.addWidget(rootFolderWidget)
        projectWidget = QtWidgets.QWidget()
        projectLayout = QtWidgets.QHBoxLayout(projectWidget)
        projectLayout.setAlignment(QtCore.Qt.AlignTop)
        projectLayout.setContentsMargins(2,2,2,2)

        projects = core.ProjectManager().getProjectFolders()

        self.projectCb = QtWidgets.QComboBox()
        self.projectCb.addItems(projects)
        self.projectCb.setItemText(0, os.getenv('PRJ'))
        projectLayout.addWidget(self.projectCb)
        self.projectCb.currentTextChanged.connect(self.updateProjectFolder)

        mainLayout.addWidget(projectWidget)
        folderWidget = QtWidgets.QWidget()
        folderLayout = QtWidgets.QHBoxLayout(folderWidget)
        folderLayout.setAlignment(QtCore.Qt.AlignTop)
        folderLayout.setContentsMargins(2,2,2,2)

        foldersA = core.ProjectManager().getFoldersA()

        self.folderACb = QtWidgets.QComboBox()
        self.folderACb.addItems(foldersA)
        self.folderACb.setItemText(0, os.getenv('FLDA'))
        folderLayout.addWidget(self.folderACb)
        self.folderACb.currentTextChanged.connect(self.updateFolderA)

        foldersB = core.ProjectManager().getFoldersB()

        self.folderBCb = QtWidgets.QComboBox()
        self.folderBCb.addItems(foldersB)
        self.folderBCb.setItemText(0, os.getenv('FLDB'))
        folderLayout.addWidget(self.folderBCb)
        self.folderBCb.currentTextChanged.connect(self.updateFolderB)

        foldersC = core.ProjectManager().getFoldersC()

        self.folderCCb = QtWidgets.QComboBox()
        self.folderCCb.addItems(foldersC)
        self.folderCCb.setItemText(0, os.getenv('FLDC'))
        folderLayout.addWidget(self.folderCCb)
        self.folderCCb.currentTextChanged.connect(self.setProject)

        mainLayout.addWidget(folderWidget)

        filesTableWidget = QtWidgets.QWidget()
        filesTableLayout = QtWidgets.QVBoxLayout(filesTableWidget)
        filesTableLayout.setAlignment(QtCore.Qt.AlignTop)
        filesTableLayout.setContentsMargins(2,2,2,2)

        self.filesTable = QtWidgets.QTableWidget()
        self.filesTable.horizontalHeader().setVisible(True)
        self.filesTable.verticalHeader().setVisible(False)
        self.filesTable.setColumnCount(4)
        self.filesTable.setColumnWidth(0, 375)
        self.filesTable.setColumnWidth(1, 90)
        self.filesTable.setColumnWidth(2, 150)
        headerLabels = (['Name', 'Type', 'Date Modified'])
        self.filesTable.setHorizontalHeaderLabels(headerLabels)
        self.filesTable.setAlternatingRowColors(True)
        self.filesTable.setSortingEnabled(True)
        self.filesTable.setShowGrid(False)
        self.filesTable.itemDoubleClicked.connect(self.checkFileState)
        filesTableLayout.addWidget(self.filesTable)

        mainLayout.addWidget(filesTableWidget)

        statusBarWidget = QtWidgets.QStatusBar()
        statusBarLayout = QtWidgets.QHBoxLayout(statusBarWidget)
        statusBarLayout.setAlignment(QtCore.Qt.AlignTop)
        statusBarLayout.setContentsMargins(2,2,2,2)

        statusBarWidget.showMessage('Ready')

        mainLayout.addWidget(statusBarWidget)

        self.setCentralWidget(projectManagerWidget)

    def updateProjectFolder(self):
        os.environ['PRJ'] = self.projectCb.currentText()
        self.folderACb.clear()
        try:
            foldersA = core.ProjectManager().getFoldersA()
        except IndexError:
            foldersA = ['']
        self.folderACb.addItems(foldersA)

    def updateFolderA(self):
        os.environ['FLDA'] = self.folderACb.currentText()
        self.folderBCb.clear()
        try:
            foldersB = core.ProjectManager().getFoldersB()
        except IndexError:
            foldersB = ['']
        self.folderBCb.addItems(foldersB)

    def updateFolderB(self):
        os.environ['FLDB'] = self.folderBCb.currentText()
        self.folderCCb.clear()
        try:
            foldersC = core.ProjectManager().getFoldersC()
        except IndexError:
            foldersC = ['']
        self.folderCCb.addItems(foldersC)

    def setProject(self):
        os.environ['FLDC'] = self.folderCCb.currentText()
        projectPath = os.path.join(os.getenv('ROOT'), os.getenv('PRJ'), os.getenv('FLDA'), os.getenv('FLDB'), os.getenv('FLDC'), 'working')

        try:
            cmds.workspace(dir=projectPath)
            cmds.workspace(projectPath, o=True)
            cmds.workspace(q=True, sn=True)
            cmds.workspace(ua=True)

        except RuntimeError:
            pass

        self.populate()

    def populate(self):
        self.filesTable.clearContents()
        filesPath = os.path.join(os.getenv('ROOT'), os.getenv('PRJ'), os.getenv('FLDA'), os.getenv('FLDB'), os.getenv('FLDC'), 'working','scenes')
        mayaFiles = sorted(core.ProjectManager().getMayaFiles())

        try:
            for i in mayaFiles:
                filePath = os.path.join(filesPath, i)
                name, ext = os.path.splitext(i)
                if ext == '.ma':
                    ext = 'Maya ASCII'
                elif ext == '.mb':
                    ext = 'Maya Binary'

                item = QtWidgets.QTableWidgetItem(name)
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

                itemType = str(ext)
                type = QtWidgets.QTableWidgetItem(itemType)
                type.setFlags(QtCore.Qt.ItemIsEnabled)

                itemDate = str(time.strftime('%d/%m/%Y %H:%M', time.gmtime(os.path.getmtime(filePath))))
                date = QtWidgets.QTableWidgetItem(itemDate)
                date.setFlags(QtCore.Qt.ItemIsEnabled)

                self.filesTable.insertRow(0)
                self.filesTable.setItem(0, 0, item)
                self.filesTable.setItem(0, 1, type)
                self.filesTable.setItem(0, 2, date)

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
        melFiles = core.ProjectManager().getMelFiles()
        try:
            if 'workspace.mel' not in melFiles:
                util.createWorkspace()
                currentScene = self.filesTable.currentItem()
                getFileName = currentScene.text()
                sceneName = getFileName + '.ma'
                cmds.file(sceneName, o=True, f=True, typ='mayaAscii', op='v=0')
            else:
                currentScene = self.filesTable.currentItem()
                getFileName = currentScene.text()
                sceneName = getFileName + '.ma'
                cmds.file(sceneName, o=True, f=True, typ='mayaAscii', op='v=0')

        except RuntimeError:
            pass

        print(' ')
        print(' > You just opened your scene successfully.')
        print(' ')
        self.close()

    def saveScene(self):
        cmds.file(s=True, f=True)
        self.openScene()
        print(' ')
        print(' > You just saved your scene successfully.')
        print(' ')
        self.close()

    def cancel(self):
        print(' ')
        print(' > You just canceled the process successfully.')
        print(' ')
        self.close()

def run():
    global mainWindow
    if not mainWindow or not cmds.window(mainWindow,q=True,e=True):
        mainWindow = ProjectManagerUI(parent=getMainWindow())
    mainWindow.show()