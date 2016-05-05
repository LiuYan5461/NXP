import os,shutil
import subprocess

def SearchEwp(src,options):
  for i in os.listdir(src):
    filepath = src + os.sep + i
    if os.path.isdir(filepath):
      SearchEwp(filepath,options)
    elif i.endswith('.ewp'):
            Make(filepath,options)
            print 'copy', filepath

def Make(filepath,options):
        IarBuilderPath='c:/Program Files (x86)/IAR Systems/Embedded Workbench 7.3_2/common/bin/IarBuild.exe'
        for option in options:
                cmd='"%s" %s -make %s'%(IarBuilderPath,filepath,option)
        #os.system(cmd)
                p = subprocess.Popen(cmd, shell=True)
                p.wait()
                print filepath
        
if __name__ == '__main__':
        rootDir='C:/mcu-sdk-2.0/mcu-sdk-2.0/boards/frdmkl28z/driver_examples'
        options=["Release","Debug"]
        print options
        SearchEwp(rootDir,options)
