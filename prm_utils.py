import os
import maya.cmds as cmds

def getProjectFolder():
    path = cmds.workspace(q=True, sn=True)
    return path

def getFileInfo():
    file = cmds.file(q=True, sn=True, shn=True)
    name, ext = os.path.splitext(file)
    try:
        name, version = name.split('_v')
    except ValueError:
        name, version = name.split('-v')
    version = int(version) + int(1)
    return name, version, ext

def getNameConvention():
    project = os.getenv('PRJ')
    projectCode = project.split('__')[0]
    directoryB = os.getenv('DIR_B')
    directoryC = os.getenv('DIR_C')
    department = os.getenv('DPT')
    nameConvention = projectCode + '-' + directoryB + '-' + directoryC + '-' + department + '-'
    return nameConvention

def createWorkspace():
    path = getProjectFolder()
    cmds.workspace(path, o=True)

    fileRuleDict = {
        'scene': 'scenes',
        'sourceImages': 'images',
        'images': 'render',
        'iprImages': 'render/tmp',
        'ASS': 'cache',
        'Alembic': 'cache',
        'FBX': 'cache',
        'OBJ': 'cache',
        'autoSave': 'tmp',
        'sceneAssembly': 'scenes',
        'mayaAscii': 'scenes',
        'mayaBinary': 'scenes',
        'offlineEdit': 'scenes',
        'ASS Export': 'cache',
        'FBX export': 'cache',
        'OBJexport': 'cache'
    }

    for k, v in fileRuleDict.iteritems():
        cmds.workspace(fileRule=[k, v])

    cmds.workspace(s=True)
    cmds.workspace(ua=True)

def createVersion():
    path = getProjectFolder()
    name, version, ext = getFileInfo()
    name = getNameConvention()

    versionName = name + 'v' + str('%03d' % version) + ext
    versionPath = os.path.join(path, 'version', versionName)

    cmds.file(rn=versionPath)
    cmds.file(s=True, type='mayaAscii')

    print ' '
    print ' > You have created ' + name + 'v' + str('%03d' % version) + ext + ' successfully.'
    print ' '

def createFolder():
    pass

def publishAsset():
    path = getProjectFolder()
    name, version, ext = getFileInfo()
    name = getNameConvention()

    maName = name + 'main' + ext
    maPath = os.path.join(path, maName)

    geoName = name + 'geo.fbx'
    geoPath = os.path.join(path, 'cache', geoName)

    idName = name + 'id.fbx'
    idPath = os.path.join(path, 'cache', idName)

    versionName = name + 'v' + str('%03d' % version) + ext
    versionPath = os.path.join(path, 'version', versionName)

    print ' '
    print ' > You have published:'

    geo = []
    for i in cmds.ls('ASSETS'):
        for i in cmds.ls('*_geo*'):
            geo.append(i)
    cmds.select(geo)
    try:
        cmds.file(rn=maPath)
        cmds.file(es=True, f=True, type='mayaAscii')
        print '   > ' + maName
    except RuntimeError:
        pass
    try:
        cmds.file(rn=geoPath)
        cmds.file(es=True, f=True, type='FBX export')
        print '   > ' + geoName
    except RuntimeError:
        pass

    cmds.select(d=True)

    id = []
    for i in cmds.ls('ASSETS'):
        for i in cmds.ls('*_id*'):
            id.append(i)
    cmds.select(id)

    try:
        cmds.file(rn=idPath)
        cmds.file(es=True, f=True, type='FBX export')
        print '   > ' + idName
    except RuntimeError:
        pass

    cmds.select(d=True)

    cmds.file(rn=versionPath)
    cmds.file(s=True, type='mayaAscii')
    print ' '
    print ' > You have created ' + versionName + ' successfully.'
    print ' '