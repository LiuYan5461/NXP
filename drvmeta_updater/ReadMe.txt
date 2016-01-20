Hi dear all
    We provide a tool named “drvmeta_updater.rb” in the mcu-sdk-2.0 directory (“mcu-sdk-2.0\bin\auxtools\versions_updater”). It can check the matched-degree of versions betweensoc_device.meta and driver.meta, and update the missing versions in driver.meta if needed. 
	For example, there is a version called” D_IP_ADC_16bSAR_SYN_034” in “MKV46F16_device.meta”, and it should have the same version in “mcu-sdk-2.0\platform\drivers\adc16”, but only have version ” D_IP_ADC_16bSAR_SYN_031” in there. To prevent the occurrence of this kind of mistake, this tool can help to check and update the right versions.
Before using this tool, you should make sure that your computer can run Ruby files. By the way, you can get some simple guide information by using ‘--help’.
If have any question or problem, please let me know, email me or skype me.   At the end of the mail, we show The usage of the driver is appended for your reference.


Best Regards,
Ellen LIU



Usages: $ ruby drvmeta_updater.rb   [ --help ] [ --all ] [ --log[num] ] [ --write ] [ --device <device_name> ]       (We use this tool by “git bash”)

•	$ ruby drvmeta_updater.rb  --help
“Help information”

•	$ ruby drvmeta_updater.rb  --device  MKW01Z4
If exist missing versions, will print “device_name + missing_verison + directory”
MKW01Z4: M:  D_IP_LPUART_SYN_012        C:/mcu-sdk-2.0/platform/drivers/lpuart/fsl_lpuart.meta
                                    If all versions are existing, will print “device_name + ‘checked’ ”
MKW01Z4 checked

•	$ ruby drvmeta_updater.rb  --device  MKW01Z4    --device  MKW01Z5
Check and print missing information of two device

•	$ ruby drvmeta_updater.rb  --device  MKW01Z4  --log [num]
If num==1, will print simple information” device_name + state”
            MKW01Z4: M:  D_IP_LPUART_SYN_012        C:/mcu-sdk-2.0/platform/drivers/lpuart/fsl_lpuart.meta
MKW01Z4: E:  pit_rti_033
MKW01Z4: E:  D_IP_PMC_NN_C90LP_031
                                    If num==2, will print detail information” device_name + state + directory”
                                                MKW01Z4: M:  D_IP_LPUART_SYN_012        C:/mcu-sdk-2.0/platform/drivers/lpuart/fsl_lpuart.meta
MKW01Z4: E:  pit_rti_033        C:/mcu-sdk-2.0/platform/drivers/pit/fsl_pit.meta
MKW01Z4: E:  D_IP_PMC_NN_C90LP_031      C:/mcu-sdk-2.0/platform/drivers/pmc/fsl_pmc.meta

•	$ ruby drvmeta_updater.rb  --device  MKW01Z4  --write
Adding function: not only print the missing versions in screen but also update in “mcu-sdk-2.0\platform\drivers\ (.*)\ (.*).meta” files

•	$ ruby drvmeta_updater.rb  --all
Check and print missing information of all devices in “mcu-sdk-2.0\devices\ (.*)\ (.*) _device.meta”
Note: Cannot choose both -all and --device




            





