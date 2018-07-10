# Project Manager v1.0.1
    
  Bugs:
  · When you run the script, if don't find any folder (roject, dept, type,...), the scripts gaves an error. FIXED!
  
  Updates:
  · When you run the script and opened a file, the next time you run it, it opened the first project on the list. Now, after opening a file, the next time you run the script, it will open on this project.
  
# Project Manager v1.0.0
  Tested in Maya 2018

  I started this project from the previously tool I have share AMN, same idea different software, how to manage your files in a easy way.

  To work with this tool, you need to have in mind that only works with the same folder hierarchy I use to.

  Firstly, yo need to redirect my rootDir with yours, line 20 (rootDir = 'Your projects root'), then, you need to have in mind the next folder hierarchy:

    --+ rootDir (D:\Projects))
      |
      |--+ project1Folder ('PRJ')
      |  |
      |  |--+ deptFolder ('DPT')
      |     |
      |     |--+ typFolder ('TYP')
      |        |
      |        |--+ assetFolder ('AST')
      |           |
      |           |--+ version
      |              |
      |              |-- MA Files
      |
      |--+ project2Folder ('PRJ')
      .  |
      .  |--+ dept1Folder ('DPT')
      .     |
            |--+ typFolder ('TYP')
               |
               |--+ assetFolder ('AST')
                  |
                  |--+ version
                     |
                     |-- MA Files
