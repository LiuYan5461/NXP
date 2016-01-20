
require 'getoptlong'
 def check_version(device,keys,log,write)
	miss =0
	Dir.chdir("../../../platform/drivers")do
	Dir.glob("#{Dir.pwd}/**/*/*.meta").each{|file|
		keys.each{|key|		
			while  File.read(file)=~/\.#{key[0,(key.length-3)]}/ 			 
				if (File.read(file))=~ /\.#{key}/ # if exist the right version
					if log == "1" 
						puts "#{device}: E:  #{key} "
					end
					if log == "2" 
						puts "#{device}: E:  #{key}	#{file} "			
					end
				else	
					miss=1
					File_update(device,file ,key, log,write)
				end 
				break
			end
		}		
	}
	end 
		return miss
 end 
 
 def File_update(device,file,key,log,write)
	if write!=1 
		puts "#{device}: M:  #{key}	#{file}"	
	else
	puts "#{device}: U:  #{key}	#{file}" 	
	file_lines=IO.readlines("#{file}")				
		for i in 1..(file_lines.length)-1 # search the insert line number
			if file_lines[i]=~/\.#{key[0,(key.length-3)]}/ 
				index=i
			end 
		end
		file_lines[index+1,0]=file_lines[index].sub(/\.#{key[0,(key.length-3)]}\d\d\d/,"\.#{key}")	# insert 			
	file_update=File.open(file,"r+")
	file_update.puts file_lines   
	file_update.close
	end
 end 
 
 def Find_Keys(device,flag)	# scan the key versions in _device.meta file 
	Dir.chdir("../../../devices/#{device}")do
	buffer=	Array.new(0)
	if (Dir.glob("*device.meta")).length!=1 # if can not accurately find the meta file
	 	puts "#{device}: Can not find ' #{device}_device.meta 'file "
		error=1
		if flag ==1
			exit 0
		end 
	end 
	if error != 1
		Dir.glob("*device.meta").each{|file|
			(File.read(file)).scan(/(\")+(\w\w?.*_\d\d\d)/){|matched|
			buffer.push($2)
			}
		}
		buffer.uniq!
	end
	return buffer
	end
 end

 
 
 
opts = GetoptLong.new(
  [ '--help', '-h', GetoptLong::NO_ARGUMENT ],
  [ '--all', '-a', GetoptLong::NO_ARGUMENT ],
  [ '--device','-d', GetoptLong::REQUIRED_ARGUMENT ],
  [ '--log', '-l', GetoptLong::OPTIONAL_ARGUMENT ],
  [ '--write', '-w', GetoptLong::NO_ARGUMENT ]
)

 devices = Array.new(0)
 log=nil
 flag=nil
 write = nil
 all=nil
 sigle_device=nil

 
 opts.each do |opt, arg|
  case opt
    when '--help'
      puts <<-EOF
	  
     -h, --help:
       Show help
	   
     -a, --all:
       Check and update all versions, based on devices in directory ".\\devices"  	   
	   
     --device <device name>:
        Device name, e.g.: MKL36Z4;	  
        Can not choose both -all and --device

     -l [num] , --log [num]:
        --log [1]: print simple information, both existing and updated
        --log [2]: print all details information, both existing and updated
        If "num" or "--log" not supplied default only print updated informations
	   
     -w, --write:
       write the updated verisions in ".\\platform\\drivers\\ *.meta" files 
       If not supplied default only show the updated information	   
		
     Example: "--device MKL36Z4 --log 1"  ; "--all --write"
     
     If you want check multiple devices, please use:
        "--device MKL36Z4 --device MKL28Z7 --log"
		
     -Output tip:		
		E: Existing   M: Missing   U: Updated

      EOF
	exit 0
    when '--log'
		log = arg
    when '--write'
		write = 1
	when '--all'
		all=1
		Dir.chdir("../../../devices") do
			Dir.glob("M*").each{|file|
			devices.push(file)
			devices.uniq!
		}	end	
    when '--device'
		sigle_device=1
		devices.push(arg)
		devices.uniq!
		flag=1
   end  
end

if (all==1)&&(sigle_device==1)
puts " Error: Cannot choose both -all and --device  "
exit 0
else 

devices.each{|device|
	puts
	keys=Find_Keys(device,flag)
	unless keys.length == 0
		miss=check_version(device,keys,log,write)		
		if miss==0
		puts "#{device}: checked"
		end
	end 
}

end

