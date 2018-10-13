# Project Manager v2.0.1

  <b>Updates</b>
  
  · Cleaned up and optimized version of this tool. 
  · Added more tools on <i>'projectUtilities.py'</i>:
   <p>- Create New Version:</p>
    
        import projectUtilities
        reload(projectUtilities)
        projectUtilities.createVersion()
    
   <p>- Publish Asset:</p>
    
        import projectUtilities
        reload(projectUtilities)
        projectUtilities.publishAsset()

  <b>Issues</b>
  
  · Gives RuntimeError when you try to open a file, PMM did not find <i>workspace.mel</i> FIXED!!!

  If you have in mind the next folder structure on your project, you shouldn't have any problem working in this version.

    --+ root ('ROOT')(C:\Projects, D:\Projects,...)
      |
      |--+ projectFolder ('PRJ')
      |  |
      |  |--+ DirectoryA ('DIR_A')        ---> ('assets', 'libs', 'seqs')
      |     |
      |     |--+ DirectoryB ('DIR_B')     ---> ('props', 'sets')('seqs')
      |        |
      |        |--+ DirectoryC ('DIR_C')  ---> ('prop_name')('set_name')('seq_name')
      |           |
      |           |--+ department ('DPT') ---> workspace.MEL
      |              |
      |              |--+ version         ---> MA Files
      |
      |--+ projectFolder ('PRJ')
      |  |
      |  |--+ DirectoryA ('DIR_A')
      |     |
      |     |--+ DirectoryB ('DIR_B')
      |        |
      |        |--+ DirectoryC ('DIR_C')
      |           |
      |           |--+ department ('DPT')
      |              |
      |              |--+ version
      |
      |--+ projectFolder
      |
      |
      
If you have your projects in another drive or folder different than mine, first, you must change manually <i>os.environ['ROOT'] = root = 'D:\Projects'</i> into <i>projectManager.py</i> with your root folder.

In a future version, I'll include a '<i>Browse</i>' button to change it from the tool.   
