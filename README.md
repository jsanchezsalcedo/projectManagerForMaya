# Project Manager v3.0.0

  <b>Updates</b>
  
  <p>· Directories hierachy fixed.
  <p>· Optimized code from previous version.
  <p>· Fixed some internal bugs.
  <p>· Tested on MAC OS X. 
    
  To avoid the Project Manager does not work properly, you need to have your project folders hierarchy organized on the next way.

    --+ root ('ROOT')(C:\Projects, D:\Projects,...)
      |
      |--+ projectFolder ('PRJ')
      |  |
      |  |--+ Level 1 ('FLDA')        ---> ('assets', 'libs', 'seqs')
      |     |
      |     |--+ Level 2 ('FLDB')     ---> ('asset_name', 'set_name')('seq_name')
      |        |
      |        |--+ Level 3 ('FLDC')  ---> ('modeling', 'shading', 'fx')
      |           |
      |           |--+ working        ---> workspace.MEL
      |              |
      |              |--+ scenes      ---> MA Files
      |
      |--+ projectFolder ('PRJ')
      |  |
      |  |--+ Level 1 ('FLDA')        ---> ('assets', 'libs', 'seqs')
      |     |
      |     |--+ Level 2 ('FLDB')     ---> ('asset_name', 'set_name')('seq_name')
      |        |
      |        |--+ Level 3 ('FLDC')  ---> ('modeling', 'shading', 'fx')
      |           |
      |           |--+ working        ---> workspace.MEL
      |              |
      |              |--+ scenes      ---> MA Files
      |
      |--+ projectFolder
      
If you have your projects in another drive or folder different than mine, first, you must change manually <i>os.environ['ROOT'] = root = '/Users/jsanchezsalcedo/Projects'</i> into <i>prm_core.py</i> with your root folder.  
