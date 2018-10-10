import maya.cmds as cmds

import projectManager
reload(projectManager)

directories = projectManager.ProjectManager()
projectPath, filesPath = directories.getProject()

def createWorkspace():
    global projectPath

    cmds.workspace(dir=projectPath)
    cmds.workspace(projectPath, o=True)
    cmds.workspace(q=True, sn=True)
    cmds.workspace(ua=True)

    fileRuleDict = {
        'scene': 'version',
        'sourceImages': 'maps',
        'images': 'render',
        'iprImages': 'render/tmp',
        'ASS': 'cache',
        'Alembic': 'cache',
        'FBX': 'cache',
        'OBJ': 'cache',
        'autosave': 'tmp',
        'sceneAssembly': 'version',
        'mayaAscii': 'version',
        'mayaBinary': 'version',
        'offlineEdit': 'version',
        'ASS Export': 'cache',
        'FBX Export': 'cache',
        'OBJ Export': 'cache'
    }

    for k, v in fileRuleDict.iteritems():
        cmds.workspace(fileRule=[k, v])

    cmds.workspace(s=True)