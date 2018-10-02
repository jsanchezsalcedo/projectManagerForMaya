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

mainWindow = None
__title__ = 'Project Manager'
__version__ = 'v1.2.1'

print ' '
print ' > You have openned {} {} successfully.'.format(__title__,__version__)
print ' > by Jorge Sanchez Salcedo (2018)'
print ' > www.jorgesanchez-da.com'
print ' > jorgesanchez.da@gmail.com'
print ' '

try:
    print ' > ' + (os.path.join(os.getenv('PRJ'), os.getenv('LVA'), os.getenv('LVB'), os.getenv('LVC'), os.getenv('DPT')))

except TypeError:
    os.environ['PRJ'] = 'None'
    os.environ['DPT'] = 'None'
    os.environ['LVA'] = 'None'
    os.environ['LVB'] = 'None'
    os.environ['LVC'] = 'None'

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
        self.setMinimumWidth(640)
        self.setMinimumHeight(425)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.createProjectUI()

    def rootDir(self):
        rootDir = 'D:\ProjectsFolder'
        return rootDir

    def createProjectUI(self):
        rootDir = self.rootDir()

        mainLayout = QtWidgets.QVBoxLayout()

        rootLy = QtWidgets.QHBoxLayout()
        self.rootLe = QtWidgets.QLineEdit()
        self.rootLe.setText(rootDir)
        self.rootLe.setEnabled(False)
        self.rootBtn = QtWidgets.QPushButton('Browse')
        self.rootBtn.setEnabled(False)
        rootLy.addWidget(self.rootLe)
        rootLy.addWidget(self.rootBtn)

        projectLy = QtWidgets.QHBoxLayout()

        self.projectCb = QtWidgets.QComboBox()

        self.departmentCb = QtWidgets.QComboBox()
        self.departmentCb.addItems(['model', 'lookdev', 'rig', 'layout', 'anim', 'fx', 'lighting'])

        LevelsLy = QtWidgets.QHBoxLayout()
        
        self.levelACb = QtWidgets.QComboBox()
        self.levelACb.setMinimumWidth(210)

        self.levelBCb = QtWidgets.QComboBox()
        self.levelBCb.setMinimumWidth(210)

        self.levelCCb = QtWidgets.QComboBox()
        self.levelCCb.setMinimumWidth(210)

        filesLy = QtWidgets.QVBoxLayout()
        self.filesTableWidget = QtWidgets.QTableWidget()
        self.filesTableWidget.horizontalHeader().setVisible(True)
        self.filesTableWidget.verticalHeader().setVisible(False)
        self.filesTableWidget.setColumnCount(3)
        self.filesTableWidget.setColumnWidth(0, 375)
        self.filesTableWidget.setColumnWidth(1, 100)
        self.filesTableWidget.setColumnWidth(2, 140)
        self.filesTableWidget.setHorizontalHeaderLabels(['Name', 'Type', 'Date'])
        self.filesTableWidget.setAlternatingRowColors(True)
        self.filesTableWidget.setSortingEnabled(True)
        self.filesTableWidget.setShowGrid(False)

        projectLy.addWidget(self.projectCb)
        projectLy.addWidget(self.departmentCb)

        for i in (self.levelACb, self.levelBCb, self.levelCCb):
            LevelsLy.addWidget(i)

        filesLy.addWidget(self.filesTableWidget)

        mainLayout.addLayout(rootLy)
        mainLayout.addLayout(projectLy)
        mainLayout.addLayout(LevelsLy)
        mainLayout.addLayout(filesLy)

        self.projectCb.currentTextChanged.connect(self.updateProject)
        self.departmentCb.currentTextChanged.connect(self.updateDepartment)
        self.levelACb.currentTextChanged.connect(self.updateLevelA)
        self.levelBCb.currentTextChanged.connect(self.updateLevelB)
        self.levelCCb.currentTextChanged.connect(self.updateLevelC)


        self.setLayout(mainLayout)
        self.setProject()

    def getProjects(self):
        projects = []

        projectsPath = os.path.join(self.rootDir())
        for i in os.listdir(projectsPath):
            path = os.path.join(projectsPath, i)
            if os.path.isdir(path):
                projects.append(i)

        return projects

    def setProject(self):
        projects = self.getProjects()

        self.projectCb.clear()
        self.projectCb.addItems(projects)

        if os.getenv('PRJ') == 'None':
            os.environ['PRJ'] = self.projectCb.currentText()
        else:
            self.projectCb.setCurrentText(os.getenv('PRJ'))

        self.setDepartment()

    def updateProject(self):
        os.environ['PRJ'] = self.projectCb.currentText()
        self.setDepartment()

    def setDepartment(self):
        if os.getenv('DPT') == 'None':
            os.environ['DPT'] = self.departmentCb.currentText()
        else:
            self.departmentCb.setCurrentText(os.getenv('DPT'))

        self.setLevelA()

    def updateDepartment(self):
        os.environ['DPT'] = self.departmentCb.currentText()
        self.setLevelA()

    def getLevelA(self):
        department = os.getenv('DPT')
        deptPrep = ['model', 'lookdev', 'rig']

        if department in deptPrep:
            levelA = ['assets', 'libs']
        else:
            levelA = ['seqs']

        return levelA

    def setLevelA(self):
        levelA = self.getLevelA()

        self.levelACb.clear()
        self.levelACb.addItems(levelA)

        if os.getenv('LVA') == 'None':
            os.environ['LVA'] = self.levelACb.currentText()
        else:
            self.levelACb.setCurrentText(os.getenv('LVA'))

        self.setLevelB()

    def updateLevelA(self):
        os.environ['LVA'] = self.levelACb.currentText()
        self.setLevelB()

    def getLevelB(self):
        levelB = []

        try:
            levelApath = os.path.join(self.rootDir(), os.getenv('PRJ'), os.getenv('LVA'))
            for i in os.listdir(levelApath):
                path = os.path.join(levelApath, i)
                if os.path.isdir(path):
                    levelB.append(i)

        except WindowsError:
            levelB = ['None']

        return levelB

    def setLevelB(self):
        levelB = self.getLevelB()

        self.levelBCb.clear()
        try:
            self.levelBCb.addItems(levelB)
        except TypeError:
            pass

        if os.getenv('LVB') == 'None':
            os.environ['LVB'] = self.levelBCb.currentText()
        else:
            self.levelBCb.setCurrentText(os.getenv('LVB'))

        self.setLevelC()

    def updateLevelB(self):
        os.environ['LVB'] = self.levelBCb.currentText()
        self.setLevelC()

    def getLevelC(self):
        levelC = []

        try:
            levelBpath = os.path.join(self.rootDir(), os.getenv('PRJ'), os.getenv('LVA'), os.getenv('LVB'))

            for i in os.listdir(levelBpath):
                path = os.path.join(levelBpath, i)
                if os.path.isdir(path):
                    levelC.append(i)

        except WindowsError:
            levelC = ['None']
            print ' '
            print ' > First, you have to create the hierarchy folders.'
            print ' '

        return levelC

    def setLevelC(self):
        levelC = self.getLevelC()

        self.levelCCb.clear()
        try:
            self.levelCCb.addItems(levelC)
        except TypeError:
            pass

        if os.getenv('LVC') == 'None':
            os.environ['LVC'] = self.levelCCb.currentText()
        else:
            self.levelCCb.setCurrentText(os.getenv('LVC'))

        self.setProjectFolder()

    def updateLevelC(self):
        os.environ['LVC'] = self.levelCCb.currentText()
        self.setProjectFolder()

    def setProjectFolder(self):
        self.workspaceFolder = os.path.join(self.rootDir(), os.getenv('PRJ'), os.getenv('LVA'), os.getenv('LVB'), os.getenv('LVC'), os.getenv('DPT'))

        normalizedPath = self.workspaceFolder.replace('\\', '/')

        path = normalizedPath + '/'

        try:
            cmds.workspace(dir=path)
            cmds.workspace(path, o=True)
            cmds.workspace(q=True, sn=True)
            cmds.workspace(ua=True)
        except RuntimeError:
            pass

        self.populate()

    def getMayaFiles(self):
        mayaFiles = glob(os.path.join(self.workspaceFolder, 'version', '*.ma'))
        return mayaFiles

    def populate(self):
        self.filesTableWidget.clearContents()
        mayaFiles = self.getMayaFiles()

        for i in mayaFiles:
            file = i.split('\\')[-1]
            name, ext = os.path.splitext(file)

            item = QtWidgets.QTableWidgetItem(name)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

            extensionUpper = (ext.split('.')[-1]).upper()
            itemlevelB = str(extensionUpper + ' File')
            levelB = QtWidgets.QTableWidgetItem(itemlevelB)
            levelB.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.AlignCenter)

            getDate = time.gmtime(os.path.getmtime(i))
            itemDate = str(time.strftime('%b %d, %Y - %H:%M', getDate))
            date = QtWidgets.QTableWidgetItem(itemDate)
            date.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.AlignCenter)

            self.filesTableWidget.insertRow(0)
            self.filesTableWidget.setItem(0, 0, item)
            self.filesTableWidget.setItem(0, 1, levelB)
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
        currentScene = self.filesTableWidget.currentItem()
        getFileName = currentScene.text()
        sceneName = getFileName + '.ma'
        cmds.file(sceneName, o=True, f=True, typ='mayaAscii', op='v=0')
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
        mainWindow = projectManager(parent=getMainWindow())
    mainWindow.show()
