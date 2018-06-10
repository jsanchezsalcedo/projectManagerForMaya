import os
import time
from glob import glob

import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI as omui

try:
    from PySide2 import QtCore, QtWidgets
    from shiboken2 import wrapInstance

except ImportError:
    from PySide import QtCore, QtGui, QtWidgets
    from shiboken import wrapInstance

__title__ = 'Project Manager'
__version__ = 'v1.0.1'
mainWindow = None
rootDir = 'D:\Projects'

print ' '
print ' > You have openned {} {} successfully.'.format(__title__,__version__)
print ' '
print '   > Project: ' + os.getenv('PRJ')
print '   > Departament: ' + os.getenv('DPT')
print '   > Type: ' + os.getenv('TYP')
print '   > Asset: ' + os.getenv('AST')
print ' '

def getMainWindow():
    omui.MQtUtil.mainWindow()
    ptr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(long(ptr), QtWidgets.QMainWindow)
    return mainWindow

class projectManager(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(projectManager, self).__init__(parent)

        self.setWindowTitle('{} {}'.format(__title__, __version__))
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setMinimumWidth(575)
        self.setMinimumHeight(325)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.createProjectUI()

    def rootDir(self):
        global rootDir
        return rootDir


    def getProjects(self):
        projectDir = self.rootDir()
        projects = []
        for i in os.listdir(projectDir):
            path = os.path.join(projectDir, i)
            if os.path.isdir(path):
                projects.append(i)

        return projects

    def createProjectUI(self):
        rootDir = self.rootDir()
        projects = self.getProjects()

        mainLayout = QtWidgets.QVBoxLayout()

        rootLy = QtWidgets.QHBoxLayout()
        self.rootLe = QtWidgets.QLineEdit()
        self.rootLe.setText(rootDir)
        self.rootLe.setEnabled(False)
        rootLy.addWidget(self.rootLe)

        projectLy = QtWidgets.QHBoxLayout()
        self.projectCb = QtWidgets.QComboBox()
        self.projectCb.addItems(projects)

        assetsLy = QtWidgets.QHBoxLayout()
        self.departamentCb = QtWidgets.QComboBox()
        self.departamentCb.setMinimumWidth(150)
        self.departamentCb.addItems([])

        self.typesCb = QtWidgets.QComboBox()
        self.typesCb.setMinimumWidth(150)
        self.typesCb.addItems([])

        self.assetCb = QtWidgets.QComboBox()
        self.assetCb.setMinimumWidth(150)
        self.assetCb.addItems([])

        filesLy = QtWidgets.QVBoxLayout()
        self.filesTableWidget = QtWidgets.QTableWidget()
        self.filesTableWidget.horizontalHeader().setVisible(True)
        self.filesTableWidget.verticalHeader().setVisible(False)
        self.filesTableWidget.setColumnCount(3)
        self.filesTableWidget.setColumnWidth(0, 305)
        self.filesTableWidget.setColumnWidth(1, 100)
        self.filesTableWidget.setColumnWidth(2, 140)
        self.filesTableWidget.setHorizontalHeaderLabels(['Name', 'Type', 'Date'])
        self.filesTableWidget.setAlternatingRowColors(True)
        self.filesTableWidget.setSortingEnabled(True)
        self.filesTableWidget.setShowGrid(False)

        projectLy.addWidget(self.projectCb)

        for i in (self.departamentCb, self.typesCb, self.assetCb):
            assetsLy.addWidget(i)

        filesLy.addWidget(self.filesTableWidget)

        mainLayout.addLayout(rootLy)
        mainLayout.addLayout(projectLy)
        mainLayout.addLayout(assetsLy)
        mainLayout.addLayout(filesLy)

        self.setLayout(mainLayout)
        self.setProjectUI()


    def setProjectUI(self):
        os.environ['PRJ'] = self.projectCb.currentText()
        self.projectCb.currentTextChanged.connect(self.updateProjectUI)
        self.setDepartamentUI()


    def updateProjectUI(self):
        os.environ['PRJ'] = self.projectCb.currentText()
        self.setDepartamentUI()


    def setDepartamentUI(self):
        self.departamentCb.clear()
        project = os.path.join(self.rootDir(), os.getenv('PRJ'))
        departaments = []

        for i in os.listdir(project):
            path = os.path.join(project, i)
            if os.path.isdir(path):
                departaments.append(i)

        self.departamentCb.addItems(departaments)
        os.environ['DPT'] = self.departamentCb.currentText()

        self.departamentCb.currentTextChanged.connect(self.updateDepartamentUI)
        self.setTypeUI()


    def updateDepartamentUI(self):
        os.environ['DPT'] = self.departamentCb.currentText()
        self.setTypeUI()


    def setTypeUI(self):
        self.typesCb.clear()
        departament = os.path.join(self.rootDir(), os.getenv('PRJ'), os.getenv('DPT'))
        types = []

        for i in os.listdir(departament):
            path = os.path.join(departament, i)
            if os.path.isdir(path):
                types.append(i)

        self.typesCb.addItems(types)
        os.environ['TYP'] = self.typesCb.currentText()

        self.typesCb.currentTextChanged.connect(self.updateTypeUI)
        self.setAssetUI()


    def updateTypeUI(self):
        os.environ['TYP'] = self.typesCb.currentText()
        self.setAssetUI()


    def setAssetUI(self):
        self.assetCb.clear()
        type = os.path.join(self.rootDir(), os.getenv('PRJ'), os.getenv('DPT'), os.getenv('TYP'))
        assets = []

        for i in os.listdir(type):
            path = os.path.join(type, i)
            if os.path.isdir(path):
                assets.append(i)

        self.assetCb.addItems(assets)
        os.environ['AST'] = self.assetCb.currentText()

        workspaceFolder = os.path.join(self.rootDir(), os.getenv('PRJ'), os.getenv('DPT'), os.getenv('TYP'), os.getenv('AST'))
        normalizedPath = workspaceFolder.replace('\\', '/')
        mel.eval('setProject \"' + normalizedPath + '\"')

        self.assetCb.currentTextChanged.connect(self.updateAssetUI)
        self.populate()


    def updateAssetUI(self):
        os.environ['AST'] = self.assetCb.currentText()
        self.populate()


    def getVersionDir(self):
        versionDir = os.path.join(self.rootDir(), os.getenv('PRJ'), os.getenv('DPT'), os.getenv('TYP'), os.getenv('AST'),'version')
        return versionDir


    def getMayaFiles(self):
        mayaFiles = glob(os.path.join(self.getVersionDir(), '*.ma'))
        return mayaFiles


    def populate(self):
        self.filesTableWidget.clearContents()
        mayaFiles = self.getMayaFiles()

        for i in mayaFiles:
            file = i.split('\\')[-1]
            name = file.split('.')[0]
            extension = file.split('.')[-1]

            item = QtWidgets.QTableWidgetItem(name)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

            extensionUpper = extension.upper()
            itemType = str(extensionUpper + ' File')
            type = QtWidgets.QTableWidgetItem(itemType)
            type.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.AlignCenter)

            getDate = time.gmtime(os.path.getmtime(i))
            itemDate = str(time.strftime('%b %d, %Y - %H:%M', getDate))
            date = QtWidgets.QTableWidgetItem(itemDate)
            date.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.AlignCenter)

            self.filesTableWidget.insertRow(0)
            self.filesTableWidget.setItem(0, 0, item)
            self.filesTableWidget.setItem(0, 1, type)
            self.filesTableWidget.setItem(0, 2, date)

        self.filesTableWidget.itemDoubleClicked.connect(self.checkFileState)


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
        global mainWindow
        currentScene = self.filesTableWidget.currentItem()
        getFileName = currentScene.text()
        sceneName = getFileName + '.ma'
        cmds.file(sceneName, o=True, f=True)
        print ' '
        print ' > You have opened your scene successfully.'
        mainWindow.close()


    def saveScene(self):
        global mainWindow
        cmds.file(s=True, f=True)
        self.openScene()
        print ' '
        print ' > You have discard to save your scene successfully.'
        mainWindow.close()


    def cancel(self):
        global mainWindow
        print ' '
        print ' > You have canceled the process successfully.'
        mainWindow.close()

def run():
    global mainWindow
    if not mainWindow or not cmds.window(mainWindow,q=True,e=True):
        mainWindow = projectManager(parent=getMainWindow())
    mainWindow.show()
