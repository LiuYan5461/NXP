from Tkinter import *
import tkMessageBox
import ttk
import sys
import os
import subprocess
import threading
import re


class Application(Frame):
    """
    Application for programming with gdb, tested on windows only with python 2.7
    """
    def __init__(self,master):
        
        Frame.__init__(self,master)

        self.master = master
        
        self.master.title("Programming with GDB")
        # Add menu
        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save Configuration", command=self.save_config)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.close)
        menubar.add_cascade(label="File", menu=filemenu)

        #variable for JLinkGDBServerCL.exe path      
        self.JLinkGDBServerCLPath = StringVar()
        
        #variable for IarBuilder.exe path  
        self.IarBuilderPath=StringVar()
        
        #variable for arm-none-eabi-gdb.exe path
        self.gdbPath = StringVar()

        #variable for root directory where binary is searched from
        self.rootDir=StringVar()

        #list for jlink device name
        self.deviceNameList = []

        #variable for jlink device
        self.deviceName = StringVar()


        self.read_config_file(os.getcwd()+r'\configFile.txt')
        
        self.grid()
        self.master.config(menu=menubar)
        self.create_widgets()

    def read_config_file(self,path):
        """
        Read configuration file, one configuration per line
        """
        # print path
        if os.path.exists(path):
            with open(path) as f:
                contents = f.readlines()
                lineNumber = len(contents)
                if lineNumber >= 1 :
                    self.JLinkGDBServerCLPath.set(contents[0])
                if lineNumber >= 2 :    
                    self.gdbPath.set(contents[1])
                if lineNumber >= 3 :
                    self.IarBuilderPath.set(contents[2])
                if lineNumber >= 4:    
                    self.deviceNameList = contents[3].strip().split(',')
                    self.deviceName = self.deviceNameList[0]
                if lineNumber >= 5 :
                    self.rootDir.set(contents[4])
               

    def create_widgets(self):
        """
        Create application's widget
        """

        #2 container frame
        self.containerFrame1 = ttk.Frame(self.master, borderwidth=1, relief="sunken")
        self.containerFrame2 = ttk.Frame(self.master, borderwidth=1, relief="sunken")

      
        #layout for 2 container frame
        self.containerFrame1.grid(row=0, column=0, sticky='nsew')
        self.containerFrame2.grid(row=0, column=1, sticky='nsew')


        #Adjust wight for resizing
        self.master.rowconfigure(0, weight = 1)      
        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)


        #LabelFrame widget for JLinkGDBServerCLPath.exe      
        LabelFrame_JLinkGDBServerCL = LabelFrame(self.containerFrame1, text="JLinkGDBServerCL.exe Path:  ")
        LabelFrame_JLinkGDBServerCL.grid(row=0, padx=4, pady=4, columnspan=3, sticky='new')

        self.containerFrame1.columnconfigure(0, weight = 20)
        self.containerFrame1.columnconfigure(1, weight = 20)
        self.containerFrame1.columnconfigure(2, weight = 20)
        #self.containerFrame1.columnconfigure(3, weight = 1)

        #Entry widget JLinkGDBServerCLPath.exe            
        Entry_JLinkGDBServerCLPath = Entry(LabelFrame_JLinkGDBServerCL, textvariable=self.JLinkGDBServerCLPath)
        Entry_JLinkGDBServerCLPath.grid(row=0, padx=5, pady=4, columnspan=3, sticky='new')

        LabelFrame_JLinkGDBServerCL.columnconfigure(0, weight = 1)
        LabelFrame_JLinkGDBServerCL.columnconfigure(1, weight = 1)
        LabelFrame_JLinkGDBServerCL.columnconfigure(2, weight = 1)

        #LabelFrame widget for arm-none-eabi-gdb.exe    
        LabelFrame_gdb = LabelFrame(self.containerFrame1, text="arm-none-eabi-gdb.exe Path:  ")
        LabelFrame_gdb.grid(row=1, padx=4, pady=4, columnspan=3, sticky='new')

        #Entry widget arm-none-eabi-gdb.exe
        Entry_gdb = Entry(LabelFrame_gdb, textvariable=self.gdbPath, width = 60)
        Entry_gdb.grid(row=0, padx=4, pady=4, columnspan=3, sticky='new')

        LabelFrame_gdb.columnconfigure(0, weight = 1)
        LabelFrame_gdb.columnconfigure(1, weight = 1)
        LabelFrame_gdb.columnconfigure(2, weight = 1)

        #LabelFrame widget for IarBuild.exe    
        LabelFrame_iar = LabelFrame(self.containerFrame1, text="IarBuild.exe  Path:  ")
        LabelFrame_iar.grid(row=2, padx=4, pady=4, columnspan=3, sticky='new')

        #Entry widget IarBuild.exe 
        Entry_iar = Entry(LabelFrame_iar, textvariable=self.IarBuilderPath, width = 60)
        Entry_iar.grid(row=0, padx=5, pady=4, columnspan=3, sticky='new')

        LabelFrame_iar.columnconfigure(0, weight = 1)
        LabelFrame_iar.columnconfigure(1, weight = 1)
        LabelFrame_iar.columnconfigure(2, weight = 1)

        #LabelFrame widget for jlink device
        LabelFrame_jlinkDevice = LabelFrame(self.containerFrame1, text="jlink device :  ")
        LabelFrame_jlinkDevice.grid(row=3, padx=4, pady=4, columnspan=3, sticky='new')

        LabelFrame_jlinkDevice.columnconfigure(0, weight = 1)
        LabelFrame_jlinkDevice.columnconfigure(1, weight = 1)
        LabelFrame_jlinkDevice.columnconfigure(2, weight = 1)

        #Combobox widget for jlink device
        self.Combobox_jlinkDevice = ttk.Combobox(LabelFrame_jlinkDevice, values=self.deviceNameList)
        self.Combobox_jlinkDevice.grid(row=0, rowspan=3, pady=5, padx=5, sticky='ew')
        if self.deviceNameList:
            self.Combobox_jlinkDevice.set(self.deviceNameList[0])
        
        #Button for adding and removing jlink device
        style = ttk.Style()
        style.map("C.TButton",foreground=[('pressed', 'red'), ('active', 'blue')],
        background = [('pressed', '!disabled', 'black'), ('active', 'white')])            

        Button_add = ttk.Button(LabelFrame_jlinkDevice, text='Add', style='C.TButton', command=self.add_device)
        Button_delete = ttk.Button(LabelFrame_jlinkDevice,text='Delete',style='C.TButton',command=self.delete_device)            
         
        Button_add.grid(row=0, column=1, pady=5, padx=5, sticky='wn')
        Button_delete.grid(row=0, column=2, pady=5, padx=5, sticky='wn')


        Usage = ['Usage:\n\n',
                 '1. Set path for jlink gdb server, arm gdb and IarBuild.exe .\n\n',
                 '2. Select jlink device, if not in the list, add a new one in the Entry box and then click add button.\n\n',
                 '3. Select a compiler and click Build button.  The default build options are "Debug" and "Release" (choose in versions)\n',
                 '   Depends on the number of program files,it will spend a period of time. Please be patient and wait!!\n\n',
                 '4. Only binary with suffix \'elf\' and \'out\' will be searched. Modify src code to support a new one.\n',
                 '   Set root path from where you want to start to search and select toolchains and versions\n',
                 '   If none of them is selected, all binarys under root path will be listed.\n\n',
                 '5. Click search button to start to search. It may take a while to get the result and in this process,\n',
                 '   the application may not respond.\n\n',
                 '6. Double click one of item in the result list to download.\n\n',
                 '7. Don\'t forget to save changed configuration before exit.Happy Programming!'
                 ]
        label_usage = Label(self.containerFrame1, text=''.join(Usage), justify = LEFT)
        label_usage.grid(row=4, pady=5, padx=5,columnspan=3, sticky='nsw')
        

        
        #LabelFrame widget for binary code seaching root dir
        LabelFrame_rootDir = LabelFrame(self.containerFrame2, text="Root searching directory:  ")
        LabelFrame_rootDir.grid(row=0, padx=4, pady=4, columnspan=3, sticky='ewns')

        self.containerFrame2.columnconfigure(1, weight = 1)
        self.containerFrame2.columnconfigure(2, weight = 1)

        Entry_rootDir = Entry(LabelFrame_rootDir, textvariable=self.rootDir)
        Entry_rootDir.grid(row=0, padx=5, pady=4, columnspan=3, sticky='new')
        
        LabelFrame_rootDir.rowconfigure(0,weight = 1)
        LabelFrame_rootDir.columnconfigure(0,weight = 1)
        LabelFrame_rootDir.columnconfigure(1,weight = 1)
        LabelFrame_rootDir.columnconfigure(2,weight = 1)

        #LabelFrame widget for 5 toolchains
        LabelFrame_toolChains = LabelFrame(self.containerFrame2, text="ToolChains:  ")
        LabelFrame_toolChains.grid(row=1, padx=4, sticky='wns')

        #5 variable for checking toolchains selection        
        self.armgccCheck = BooleanVar()
        self.mdkCheck = BooleanVar()
        self.iarCheck = BooleanVar()
        self.kdsCheck = BooleanVar()
        self.atlCheck = BooleanVar()

        #Default all toolchains are selected
        self.armgccCheck.set(False)
        self.mdkCheck.set(False)
        self.iarCheck.set(False)
        self.kdsCheck.set(False)
        self.atlCheck.set(False)

        #Checkbutton widget for 5 toolchains        
        Checkbutton_armgcc = Checkbutton(LabelFrame_toolChains, text="armgcc", variable=self.armgccCheck, onvalue=True, offvalue=False)
        Checkbutton_mdk = Checkbutton(LabelFrame_toolChains, text="mdk", variable=self.mdkCheck, onvalue=True, offvalue=False)
        Checkbutton_iar = Checkbutton(LabelFrame_toolChains, text="iar", variable=self.iarCheck, onvalue=True, offvalue=False)
        Checkbutton_kds = Checkbutton(LabelFrame_toolChains, text="kds", variable=self.kdsCheck, onvalue=True, offvalue=False)
        Checkbutton_atl = Checkbutton(LabelFrame_toolChains, text="atl", variable=self.atlCheck, onvalue=True, offvalue=False)

        Checkbutton_armgcc.grid(row=0, padx=4, sticky='w')
        Checkbutton_mdk.grid(row=1, padx=4, sticky='w')
        Checkbutton_iar.grid(row=2, padx=4, sticky='w')
        Checkbutton_kds.grid(row=3, padx=4, sticky='w')
        Checkbutton_atl.grid(row=4, padx=4, sticky='w')

        LabelFrame_toolChains.rowconfigure(0, weight = 1)
        LabelFrame_toolChains.rowconfigure(1, weight = 1)
        LabelFrame_toolChains.rowconfigure(2, weight = 1)
        LabelFrame_toolChains.rowconfigure(3, weight = 1)
        LabelFrame_toolChains.rowconfigure(4, weight = 1)

        #Button for Armgcc_build
        Button_search = ttk.Button(LabelFrame_toolChains, text='armgcc_build', style='C.TButton', command=self.Armgcc_build)
        Button_search.grid(row=0,column=2)

        #Button for Mdk_build
        Button_search = ttk.Button(LabelFrame_toolChains, text='mdk_build', style='C.TButton', command=self.Mdk_build)
        Button_search.grid(row=1,column=2)

        #Button for Iar_build
        Button_search = ttk.Button(LabelFrame_toolChains, text='iar_build', style='C.TButton', command=self.Iar_build)
        Button_search.grid(row=2,column=2)

        #Button for Kds_build
        Button_search = ttk.Button(LabelFrame_toolChains, text='kds_build', style='C.TButton', command=self.Kds_build)
        Button_search.grid(row=3,column=2)
        
        #Button for Atl_build
        Button_search = ttk.Button(LabelFrame_toolChains, text='atl_build', style='C.TButton', command=self.Atl_build)
        Button_search.grid(row=4,column=2)
        
        
        #LabelFrame widget for 2 build versions: realse and debug
        LabelFrame_version = LabelFrame(self.containerFrame2, text="Version: ")
        LabelFrame_version.grid(row=2,padx=4,sticky='ewns')

        
        #2 variable for checking version selection
        self.releaseCheck = BooleanVar()
        self.debugCheck = BooleanVar()

        self.releaseCheck.set(True)
        self.debugCheck.set(True)


        #Checkbutton widget for 2 build versions
        Checkbutton_release = Checkbutton(LabelFrame_version, text="release", variable=self.releaseCheck, onvalue=True, offvalue=False)
        Checkbutton_debug = Checkbutton(LabelFrame_version, text="debug", variable=self.debugCheck, onvalue=True, offvalue=False)
        
        Checkbutton_release.grid(row=0, padx=4, sticky='w')
        Checkbutton_debug.grid(row=1, padx=4, sticky='w')

        LabelFrame_version.rowconfigure(0, weight = 1)
        LabelFrame_version.rowconfigure(1, weight = 1)

        
        #LabelFrame widget for log 
        Labelframe_log = LabelFrame(self.containerFrame2, text="log: ")
        Labelframe_log.grid(row=3,  padx=5, pady=4, columnspan=3, sticky='new')
        
        #Listbox widget for log information
        self.Listbox_logResesult = Listbox(Labelframe_log, selectmode=BROWSE, height=9, width=60)
        self.Listbox_logResesult.grid(row=1, column=0, pady=5, padx=5, sticky='wens')

        Labelframe_log.columnconfigure(0,weight = 40)

        #scrollbar for log listbox
        yscrollbar = Scrollbar(Labelframe_log)
        yscrollbar.grid(row=1, column=1, pady=5, padx=1, sticky='wns')
        Labelframe_log.columnconfigure(1, weight = 1)
        self.Listbox_logResesult['yscrollcommand'] = yscrollbar.set
        yscrollbar.config(command=self.Listbox_logResesult.yview)

        xscrollbar = Scrollbar(Labelframe_log, orient='horizontal')
        xscrollbar.grid(row=2, column=0, padx=1, sticky='ewn')
        self.Listbox_logResesult['xscrollcommand'] = xscrollbar.set
        xscrollbar.config(command=self.Listbox_logResesult.xview)

        self.Listbox_logResesult.bind('<Double-Button-1>',self.download)


        

        #LabelFrame widget for seaching result
        Labelframe_result = LabelFrame(self.containerFrame2, text="Result:  ")
        Labelframe_result.grid(row=1, rowspan=2, columnspan=2, column=1, padx=4, sticky='ewns')

        #Button for search
        Button_search = ttk.Button(Labelframe_result, text='Search', style='C.TButton', command=self.search)
        Button_search.grid(row=0,column=0)
        



        #Listbox widget for searching result
        self.Listbox_searchResesult = Listbox(Labelframe_result, selectmode=BROWSE, height=10, width=60)
        self.Listbox_searchResesult.grid(row=1, column=0, pady=5, padx=5, sticky='wens')

        Labelframe_result.columnconfigure(0,weight = 50)
        

        #scrollbar for result listbox
        yscrollbar = Scrollbar(Labelframe_result)
        yscrollbar.grid(row=1, column=1, pady=5, padx=1, sticky='wns')
        Labelframe_result.columnconfigure(1, weight = 1)
        self.Listbox_searchResesult['yscrollcommand'] = yscrollbar.set
        yscrollbar.config(command=self.Listbox_searchResesult.yview)

        xscrollbar = Scrollbar(Labelframe_result, orient='horizontal')
        xscrollbar.grid(row=2, column=0, padx=1, sticky='ewn')
        self.Listbox_searchResesult['xscrollcommand'] = xscrollbar.set
        xscrollbar.config(command=self.Listbox_searchResesult.xview)

        self.Listbox_searchResesult.bind('<Double-Button-1>',self.download)
        
    def close(self):
        """
        Exit application
        """
        self.master.destroy()


    def add_device(self):
        """
        Function to add jlink device into ComboBox
        """
        deviceName = self.Combobox_jlinkDevice.get().upper()
        for item in self.deviceNameList:
            if item == deviceName.upper():
                tkMessageBox.showinfo('!', deviceName + ' already exsits!')
                return
        self.deviceNameList.append(deviceName)
        self.Combobox_jlinkDevice.set(deviceName)
        self.Combobox_jlinkDevice['values'] = self.deviceNameList


    def delete_device(self):
        """
        Function to remove jlink device from ComboBox
        """
        
        deviceName = self.Combobox_jlinkDevice.get().upper()
        
        if deviceName in self.deviceNameList:
            
            self.deviceNameList.remove(deviceName)            
            self.Combobox_jlinkDevice['values'] = self.deviceNameList
            if len(self.deviceNameList) != 0:
                self.Combobox_jlinkDevice.set(self.deviceNameList[0])
            else:
                self.Combobox_jlinkDevice.set('')      

    
    def save_config(self):
        """
        Function to save configuration, these 4 configuration items will be saved:
        - JLinkGDBServerCLPath.exe path
        - arm-none-eabi-gdb.exe path
        - jlink device,comma separated
        - binary root searching directory
        
        """        
        configFile = os.getcwd()+r'\configFile.txt'
        with open(configFile,'w') as f:
            f.write(self.JLinkGDBServerCLPath.get().strip()+'\n')
            f.write(self.gdbPath.get().strip()+'\n')
            f.write(self.IarBuilderPath.get().strip()+'\n')
            f.write(','.join(self.deviceNameList).strip()+'\n')
            f.write(self.rootDir.get().strip()+'\n')

##################################
    def Armgcc_build(self):
        if self.armgccCheck.get():
            rootDir = self.rootDir.get().strip()
            self.Listbox_searchResesult.delete(0,END)
            options=[]
            if self.releaseCheck.get():
                 options.append("Release")
            if self.debugCheck.get():
                 options.append("Debug")
         
            index=0
            self.Gccbuild(rootDir,options,index)
            tkMessageBox.showinfo('Armgcc_Build:', rootDir + '\n     ALL DONE!')
        else:
            tkMessageBox.showinfo('Error:', 'Please chose armgcc in ToolChains!')
            
    def Gccbuild(self,rootDir,options,index):            
        """
        Function to search build_all.bat / build_debug.bat/ build_release.bat files in IAR and make .out file
        """ 

        for i in os.listdir(rootDir):
           # print (i)
            filepath = rootDir + os.sep + i
           # print ("\n"+filepath)
            for j in os.listdir(filepath):
                if j=='armgcc':
                    filepath = filepath + os.sep + j                   
                    for option in options:
                        if os.path.exists(filepath+os.sep+option.lower()):
                            log="Exist ["+option+"] "+filepath
                            self.Listbox_logResesult.insert(index,log)
                            index += 1                         
                        else:                     
                         # run .bat file
                            os.chdir(filepath)
                            cmd='build_%s.bat'%(option.lower())
                            p = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                            p.wait()
                            if p.stdout:
                                p.stdout.close()
                        #Insert result into logbox
                            log="Done ["+option+"] "+filepath
                            self.Listbox_logResesult.insert(index,log)
                            index += 1

    def Mdk_build(self):
        rootDir = self.rootDir.get().strip()
        
    def Kds_build(self):
        rootDir = self.rootDir.get().strip()
        

    def Atl_build(self):
        rootDir = self.rootDir.get().strip()
        
            
    def Iar_build(self): 
        if self.iarCheck.get():
            rootDir = self.rootDir.get().strip()
            self.Listbox_searchResesult.delete(0,END)
            options=[]
            if self.releaseCheck.get():
                 options.append("Release")
            if self.debugCheck.get():
                 options.append("Debug")
            index=0
            self.Iarbuild(rootDir,options,index)
            tkMessageBox.showinfo('Iar_Build:', rootDir + '\n     ALL DONE!')
        else:
            tkMessageBox.showinfo('Error:', 'Please chose iar in ToolChains!')
             
        
    def Iarbuild(self,rootDir,options,index):
        """
        Function to search .ewp files in IAR and make .out file
        """ 
        Iarpath=self.IarBuilderPath.get().strip()
        for i in os.listdir(rootDir):
            filepath = rootDir + os.sep + i
            if os.path.isdir(filepath):
                self.Iarbuild(filepath,options,index)
            elif i.endswith('.ewp'):
                fatherpath=os.path.split(filepath)[0]     
                for option in options:
                     if os.path.isdir(fatherpath+os.sep+option):
                         log="Exist ["+option+"] "+filepath
                         self.Listbox_logResesult.insert(index,log)
                         index += 1                         
                     else:
                         #use IarBuild.exe
                         cmd='"%s" %s -make %s'%(Iarpath,filepath,option)
                         p = subprocess.Popen(cmd, shell=True)
                         p.wait()
                        #Insert result into logbox
                         log="Done ["+option+"] "+filepath
                         self.Listbox_logResesult.insert(index,log)
                         index += 1

                    
      
     
        ##################################
        



    def search(self):
        """
        Function to search binary
        """
   
        rootDir = self.rootDir.get().strip()
        toolChains = []
        version = []

        if os.path.exists(rootDir):    
            index = 0
            
            #Delete all items in the listbox first
            self.Listbox_searchResesult.delete(0,END)
            
            #Check toolchains selection
            if self.armgccCheck.get():
                toolChains.append('armgcc')
            if self.mdkCheck.get():
                toolChains.append('mdk')
            if self.iarCheck.get():
                toolChains.append('iar')
            if self.kdsCheck.get():
                toolChains.append('kds')
            if self.atlCheck.get():
                toolChains.append('atl')

            #Check build version selection
            if self.releaseCheck.get():
                version.append('release')
            if self.debugCheck.get():
                version.append('debug')

            #print '|'.join(toolChains)
            
            toolChainRule = re.compile('|'.join(toolChains))
            versionRule = re.compile('|'.join(version))

            for parent,dirnames,filenames in os.walk(rootDir):
                if re.findall(toolChainRule, parent) and re.findall(versionRule, parent):
                    for eachFile in filenames:
                        suffix = os.path.splitext(eachFile)[1]
                        #Add new binary suffix here
                        if  suffix== '.elf' or suffix == '.out':
                            fileName = os.path.join(parent,eachFile)
                            #Insert result into listbox
                            fileName = fileName.replace(rootDir,'')
                            self.Listbox_searchResesult.insert(index, fileName)
                            index += 1
            
        else:
            tkMessageBox.showinfo('Error', rootDir + '\nnot exsits!')
            
    def download(self,event):
        """
        Function to download binary
        """
        
        #Get the selected jlink device 
        jlinkDevice = self.Combobox_jlinkDevice.get()
        #print jlinkDevice

        #Get the selected binary
        index = self.Listbox_searchResesult.curselection()
        if index:            
            binaryFile = self.rootDir.get().strip() + self.Listbox_searchResesult.get(index)
            binaryFile = binaryFile.replace('\\','\\\\')
            #print binaryFile
        else:
            return
        
        jlinkBin = self.JLinkGDBServerCLPath.get().strip() + r'\JLinkGDBServerCL.exe'
        gdbBin = self.gdbPath.get().strip() + r'\arm-none-eabi-gdb.exe'
        
        if not os.path.exists(jlinkBin):
            tkMessageBox.showinfo('Error', jlinkBin + '\nnot exsits!')
            return
        if not os.path.exists(gdbBin):
            tkMessageBox.showinfo('Error', gdbBin + '\nnot exsits!')
            return            
            
        jlinkConnected = False
        
        #DETACHED_PROCESS 0x00000008 For console processes, the new process does not inherit its parent's console (the default).
        jlinkSession = subprocess.Popen([jlinkBin,'-select','USB','-device',jlinkDevice,'-if','SWD','-speed','1000'], shell = False, stdout=subprocess.PIPE, creationflags=0x08)
        kill_jlinkSession = lambda p: p.kill()
        
        #Set timeout as 20 seconds,kill the process if times out.
        timer = threading.Timer(20, kill_jlinkSession, [jlinkSession])
        try:
            timer.start()
            while True:
                next_line = jlinkSession.stdout.readline()
  
                if next_line == '' and jlinkSession.poll() != None:
                    break
                if 'J-Link is connected' in next_line:
                    timer.cancel()
                    jlinkConnected = True
                    break
                #sys.stdout.write(next_line)
        finally:
            timer.cancel()
        
        if jlinkConnected == True:

            #create gdbscript to download binary
            gdbScript = open('gdbScript.txt','w')
            gdbScript.write('target remote localhost:2331\n')
            gdbScript.write('monitor reset\n')
            gdbScript.write('monitor speed auto\n')
            gdbScript.write('monitor endian little\n')
            gdbScript.write('monitor reset\n')

            gdbScript.write('load '+ binaryFile + '\n')
            gdbScript.write('monitor reset\n')
            gdbScript.write('monitor go\n')
            gdbScript.write('disconnect\n')
            gdbScript.write('q\n')
            gdbScript.close()

            gdbSession = subprocess.Popen([gdbBin,'-x','gdbScript.txt'], creationflags=0x08)
            gdbSession.wait()
            
            jlinkSession.kill()            
            gdbSession.kill()
        else:
            tkMessageBox.showinfo('Error','Connecting to J-Link failed!')
 
        
if __name__ == '__main__':
    root=Tk()
    app = Application(root)
 
    app.mainloop()
