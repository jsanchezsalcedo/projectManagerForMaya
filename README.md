# Project Manager v1.1.1

  <b>Updates</b>
  
  Cleaned and optimized part of the code to be more readable.
  
  <b>Issues>/b>
    
  It is still having a bug when you change of project after opening an asset of another project previously selected, this duplicates the process when you select an asset and open it. If you are always working on the same project, there is no problem.


At the moment, the solution to this issue is, change the project and select the asset in what you want to work, the project manager saves the level which you are, close it and open it again, then you could work fine in this project.

Sorry for the inconveniences, I am learning at the same time I am working on this script and hope to find a solution as soon as will be possible.

Thanks!

# Project Manager v1.0.1
    
  <b>Bugs</b>
  
  When you run the script, if don't find any folder project, dept, type,...), the scripts gaves an error. FIXED!
  
  <b>Updates</b>
  
  When you run the script and opened a file, the next time you run it, it opened the first project on the list. Now, after opening a file, the next time you run the script, it will open on this project.
  
# Project Manager v1.0.0
  <i>Tested in Maya 2018</i>

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
