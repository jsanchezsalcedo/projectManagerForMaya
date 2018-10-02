# Project Manager v1.2.1

  <b>Update</b>
  
  Revisited, cleaned and optimized the entire code to fix some bugs.
  
  <b>Issues</b>
    
  NOT FIXED AT ALL!!! It is still having the bug when you change of project after opening an asset of another project previously selected, duplicates (LESS) the process (ONLY) when you open it. If you are always working on the same project, there is no problem.

Sorry for the inconveniences, I am learning Python at the same time I am working on this and other scripts and hope to find a fix as soon as will be possible.

Thanks!

    --+ rootDir (D:\ProjectFolder))
      |
      |--+ project1Folder ('PRJ')
      |  |
      |  |--+ levelA ('LVA')
      |     |
      |     |--+ levelB ('LVB')
      |        |
      |        |--+ levelC ('LVC')
      |           |
      |           |--+ department ('DPT') ---> workspace.MEL
      |              |
      |              |--+ version         ---> files .MA
      |
      |--+ project2Folder ('PRJ')
      |  |
      |  |--+ levelA ('LVA')
      |     |
      |     |--+ levelB ('LVB')
      |        |
      |        |--+ levelC ('LVC')
      |           |
      |           |--+ department ('DPT') ---> workspace.MEL
      |              |
      |              |--+ version         ---> files .MA
      |
      |--+ project3Folder ('PRJ')
      |
      |
      
Please, include the file <i>workspace.mel</i> into <b>department</b> folder and <i>mayaAscii</i>(.ma) files into <b>version</b> folder, if not, does not work. If you want to use it with <i>default</i> scene folder, change into the script, version for scenes and it should be work.
