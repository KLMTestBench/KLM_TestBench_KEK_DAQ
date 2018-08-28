import re
from pexpect import pxssh
import getpass
import os

def get_ssh_connection(hostname,username,password):
    remoteShell = pxssh.pxssh()    
    remoteShell.login(hostname, username, password)
    return remoteShell
    

def sudo(remoteShell,password,command):
    rootprompt = re.compile('.*[$#]')
    remoteShell.sendline(command)
    i = remoteShell.expect([rootprompt,'assword.*: '])
    if i==0:
        print("didnt need password!")
        pass
    elif i==1:
        print("sending password")
        remoteShell.sendline(password)
        j = remoteShell.expect([rootprompt,'Sorry, try again'])
        if j == 0:
            pass
        elif j == 1:
            raise Exception("bad password")
    else:
        raise Exception("unexpected output")
    #s.
    
def scp(Password,Source,Destination):
    line = 'sshpass -p "'+ Password + '" scp -r '+ Source +" "+ Destination
    os.system(line)
    

def scp2Remote(Password,Source,DestinationFolder,UserName,Host):
    Destination=UserName+"@"+Host +":"+DestinationFolder
    scp(Password,Source,Destination)

def set_content(remoteShell,Line,FileName,Append = False):
    FillOp = " > "
    if Append:
        FillOp = " >> "

    Line ='echo "'+  Line + '" ' + FillOp +  FileName
    remoteShell.sendline(Line)
    remoteShell.prompt(timeout=1)


def append_conf_file(s,password,fileName,Line):
    sudo(s,password,'sudo -i')
    set_content(s,Line,fileName,Append=True)
    s.sendline("exit")


class DHCP_client:
    def __init__(self,HostName,hardware_ethernet,fixed_address,option_host_name="",comment=""):
        self.HostName = HostName
        self.hardware_ethernet = hardware_ethernet
        self.fixed_address = fixed_address
        self.comment = ""
        if len(comment)>0:
            self.comment = '#' + comment

        self.option_host_name = option_host_name
        
       

def add_DHCP_client(elevated_remoteShell,DHCP_cl,restart = True):
    line = 	'host ' + DHCP_cl.HostName + " { hardware ethernet " + DHCP_cl.hardware_ethernet + " ; fixed-address " + DHCP_cl.fixed_address+"; "
    if len(DHCP_cl.option_host_name)>0:
        line = line + "option host-name " +DHCP_cl.option_host_name+" ;" 
    
    line = line +  " } " +DHCP_cl.comment
    set_content(elevated_remoteShell,FileName = '/etc/dhcp/dhcpd.conf',Line=line,Append=True)
    if restart:
        elevated_remoteShell.sendline("systemctl restart dhcpd.service")
        

    


class Host:
    def __init__(self,HostName,IP_address,alias="",comment=""):
        self.HostName = HostName
        self.IP_address = IP_address
        self.alias = alias
        self.comment = ""
        if len(comment)>0:
            self.comment = '#' + comment

def add_host(elevated_remoteShell,host):
    line = host.IP_address + " " +host.HostName + " " + host.alias + " " +host.comment
    set_content(elevated_remoteShell,Line=line,FileName='/etc/hosts',Append=True)
    

#pw = "***"
#s=get_ssh_connection("168.105.254.210","belle2",pw)


#d = DHCP_client("LabComputer","3c:97:0e:91:6c:0a","192.168.1.109",comment= "comment1")
#add_DHCP_client(s,pw,d)

#s.prompt()
#print(s.before)
#h=Host(IP_address = "192.168.1.108",HostName = "cpr108", alias = "C0A8016C")
#add_host(s,pw,h)
#s.prompt()
#print(s.before)
