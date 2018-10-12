import maya.cmds as cmds

def createWorkspace():
    path = cmds.workspace(q=True, sn=True)
    cmds.workspace(path, o=True)

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
    cmds.workspace(ua=True)
