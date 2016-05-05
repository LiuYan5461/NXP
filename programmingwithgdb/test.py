import os,shutil
import subprocess

#project_file='c:/mcu-sdk-2.0/mcu-sdk-2.0/boards/frdmkl27z/demo_apps/power_manager/iar/power_manager.ewp'
#IarBuilderPath='c:/Program Files (x86)/IAR Systems/Embedded Workbench 7.3_2'
#option='Release'

#mdd='"%s" %s -make %s'%(IarBuilderPath+"/common/bin/IarBuild.exe",project_file,option)

#os.system(cmdd) 
#print IarBuilderPath.strip()


def SearchEwp(src,options):#def cptxt(src, dst):
  for i in os.listdir(src):
    filepath = src + os.sep + i
    if os.path.isdir(filepath):
      SearchEwp(filepath,options)
    elif i.endswith('.ewp'):
            Make(filepath,options)
            #print 'copy', filepath

def Make(filepath,options):
        IarBuilderPath='c:/Program Files (x86)/IAR Systems/Embedded Workbench 7.3_2/common/bin/IarBuild.exe'
        fatherpath=os.path.pardir(filepath)
        filename=os.path.split(filepath)[1]
        for option in options:
          if os.path.isdir(fatherpath+"\\"+option):
            print ("Exist "+option+" "+filename)
          else:
            cmd='"%s" %s -make %s'%(IarBuilderPath,filepath,option)
        #os.system(cmd)
            p = subprocess.Popen(cmd, 0, None, None, None, None, shell=True)
            p.wait()
            print ("Done "+option+" "+filename)
        
if __name__ == '__main__':
        rootDir='C:/mcu-sdk-2.0/mcu-sdk-2.0/boards/frdmkl28z/driver_examples'
        options=['Release','Debug']
        SearchEwp(rootDir,options)
