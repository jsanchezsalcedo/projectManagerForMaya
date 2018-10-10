import os

projects = []
departments = ['model', 'lookdev', 'rig', 'layout', 'anim', 'fx', 'lighting']
dirA = []
dirB = []
dirC = []

class ProjectManager(dict):
    def projectsRoot(self):
        os.environ['ROOT'] = root = 'D:\Projects'
        return root

    def projectsDir(self):
        projects = []
        root = self.projectsRoot()
        for i in os.listdir(root):
            path = os.path.join(root, i)
            if os.path.isdir(path):
                projects.append(i)
        if os.getenv('PRJ') == None:
            os.environ['PRJ'] = projects[0]
        else:
            pass
        return projects

    def departmentsDir(self):
        if os.getenv('DPT') == None:
            os.environ['DPT'] = departments[0]
        else:
            os.getenv('DPT')
        return departments

    def directoryA(self):
        dirA = []
        preprod = ['model', 'lookdev', 'rig']
        try:
            if os.getenv('DPT') in preprod:
                dirA = ['assets', 'libs']
            else:
                dirA = ['seqs']
            if os.getenv('DIR_A') == None:
                os.environ['DIR_A'] = dirA[0]
            else:
                pass
            return dirA
        except WindowsError:
            pass

    def directoryB(self):
        dirB = []
        directoryApath = os.path.join(os.getenv('ROOT'), os.getenv('PRJ'), os.getenv('DIR_A'))
        try:
            for i in os.listdir(directoryApath):
                path = os.path.join(directoryApath, i)
                if os.path.isdir(path):
                    dirB.append(i)
            if os.getenv('DIR_B') == None:
                os.environ['DIR_B'] = dirB[0]
            else:
                pass
            return dirB
        except WindowsError:
            pass

    def directoryC(self):
        dirC = []
        directoryBpath = os.path.join(os.getenv('ROOT'), os.getenv('PRJ'), os.getenv('DIR_A'), os.getenv('DIR_B'))
        try:
            for i in os.listdir(directoryBpath):
                path = os.path.join(directoryBpath, i)
                if os.path.isdir(path):
                    dirC.append(i)
            if os.getenv('DIR_C') == None:
                os.environ['DIR_C'] = dirC[0]
            else:
                pass
            return dirC
        except WindowsError:
            pass

    def getProject(self):
        projectPath = os.path.join(os.getenv('ROOT'), os.getenv('PRJ'), os.getenv('DIR_A'), os.getenv('DIR_B'), os.getenv('DIR_C'), os.getenv('DPT'))
        filesPath = os.path.join(projectPath, 'version')
        return projectPath, filesPath

    def melFiles(self):
        projectPath, filesPath = self.getProject()
        try:
            files = os.listdir(projectPath)
            melFiles = [f for f in files if f.endswith('.mel')]
            return melFiles

        except WindowsError:
            pass

    def mayaFiles(self):
        projectPath, filesPath = self.getProject()
        try:
            files = os.listdir(filesPath)
            mayaFiles = [f for f in files if f.endswith('.ma')]
            return mayaFiles

        except WindowsError:
            pass



