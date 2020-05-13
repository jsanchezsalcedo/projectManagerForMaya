import os

class ProjectManager(dict):
    def checkedFolders(self):
        folders = ['ROOT', 'PRJ', 'FLDA', 'FLDB', 'FLDC']
        for i in folders:
            if os.getenv(i) == None:
                os.environ['ROOT'] = self.setProjectsRoot()
                os.environ['PRJ'] = self.setProjectFolder()
                os.environ['FLDA'] = self.setFolderA()
                os.environ['FLDB'] = self.setFolderB()
                os.environ['FLDC'] = self.setFolderC()

    def setProjectsRoot(self):
        os.environ['ROOT'] = root = '/Users/jsanchezsalcedo/Projects'
        return root

    def getProjectFolders(self):
        root = self.setProjectsRoot()
        projects = []
        for i in os.listdir(root):
            path = os.path.join(root, i)
            if os.path.isdir(path):
                projects.append(i)
        return (sorted(projects))

    def setProjectFolder(self):
        project = self.getProjectFolders()[0]
        if os.getenv('PRJ') == None:
            os.environ['PRJ'] = project
        else:
            project = os.environ['PRJ']
        return project

    def getFolders(self):
        folders = []
        for i in os.listdir(self.path):
            folderPath = os.path.join(self.path, i)
            if os.path.isdir(folderPath):
                folders.append(i)
        return folders

    def getFoldersA(self):
        self.setProjectFolder()
        self.path = os.path.join(os.getenv('ROOT'), os.getenv('PRJ'))
        foldersA = self.getFolders()
        return (sorted(foldersA))

    def setFolderA(self):
        try:
            folderA = self.getFoldersA()[0]
            if os.getenv('FLDA') == None:
                os.environ['FLDA'] = folderA
            else:
                folderA = os.environ['FLDA']

            return folderA

        except IndexError:
            pass

    def getFoldersB(self):
        self.setFolderA()
        self.path = os.path.join(os.getenv('ROOT'), os.getenv('PRJ'), os.getenv('FLDA'))
        foldersB = self.getFolders()
        return (sorted(foldersB))

    def setFolderB(self):
        try:
            folderB = self.getFoldersB()[0]
            if os.getenv('FLDB') == None:
                os.environ['FLDB'] = folderB
            else:
                folderB = os.environ['FLDB']

            return folderB

        except IndexError:
            pass

    def getFoldersC(self):
        self.setFolderB()
        self.path = os.path.join(os.getenv('ROOT'), os.getenv('PRJ'), os.getenv('FLDA'), os.getenv('FLDB'))
        foldersC = self.getFolders()
        return (sorted(foldersC))

    def setFolderC(self):
        try:
            folderC = self.getFoldersC()[0]
            if os.getenv('FLDC') == None:
                os.environ['FLDC'] = folderC
            else:
                folderC = os.environ['FLDC']

            return folderC

        except IndexError:
            pass

    def getProjectPath(self):
        self.setFolderC()
        projectPath = os.path.join(os.getenv('ROOT'), os.getenv('PRJ'), os.getenv('FLDA'), os.getenv('FLDB'), os.getenv('FLDC'), 'working')
        return projectPath

    def getMayaFiles(self):
        projectPath = self.getProjectPath()
        filesPath = os.path.join(projectPath, 'scenes')
        mayaFiles = []
        try:
            files = os.listdir(filesPath)
            mayaFiles = [f for f in files if f.endswith('.ma') or f.endswith('.mb')]
        except OSError or WindowsError:
            mayaFiles = []

        return mayaFiles

    def getMelFiles(self):
        projectPath = self.getProjectPath()
        melFiles = []
        try:
            files = os.listdir(projectPath)
            melFiles = [f for f in files if f.endswith('.mel')]
        except OSError or WindowsError:
            melFiles = []
        return melFiles

    def getBackupsFiles(self):
        projectPath = self.getProjectPath()
        filesPath = os.path.join(projectPath, 'tmp')
        backupFiles = []
        try:
            files = os.listdir(filesPath)
            backupFiles = [f for f in files if f.endswith('.ma')]
        except OSError or WindowsError:
            backupFiles = []
        return backupFiles