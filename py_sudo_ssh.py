import re
from pexpect import pxssh
import getpass
import os

def get_ssh_connection(hostname,username,password):
    s = pxssh.pxssh()    
    s.login(hostname, username, password)
    return s
    

def sudo(s,password,command):
    rootprompt = re.compile('.*[$#]')
    s.sendline(command)
    i = s.expect([rootprompt,'assword.*: '])
    if i==0:
        print("didnt need password!")
        pass
    elif i==1:
        print("sending password")
        s.sendline(password)
        j = s.expect([rootprompt,'Sorry, try again'])
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

def set_content(s,Line,FileName,Append = False):
    FillOp = " > "
    if Append:
        FillOp = " >> "

    Line ='echo "'+  Line + '" ' + FillOp +  FileName
    s.sendline(Line)


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
        
       

def add_DHCP_client(s,password,DHCP_cl,restart = True):
    line = 	'host ' + DHCP_cl.HostName + " { hardware ethernet " + DHCP_cl.hardware_ethernet + " ; fixed-address " + DHCP_cl.fixed_address+"; "
    if len(DHCP_cl.option_host_name)>0:
        line = line + "option host-name " +DHCP_cl.option_host_name+" ;" 
    
    line = line +  " } " +DHCP_cl.comment
    append_conf_file(s,password,fileName = '/etc/dhcp/dhcpd.conf',Line=line)
    if restart:
        sudo(s,password,"systemctl restart dhcpd.service")

    


class Host:
    def __init__(self,HostName,IP_address,alias="",comment=""):
        self.HostName = HostName
        self.IP_address = IP_address
        self.alias = alias
        self.comment = ""
        if len(comment)>0:
            self.comment = '#' + comment

def add_host(s,password,host):
    line = host.IP_address + " " +host.HostName + " " + host.alias + " " +host.comment
    append_conf_file(s,password,fileName = '/etc/hosts',Line=line)

#pw = "12345678"
#s=get_ssh_connection("168.105.254.210","belle2",pw)


#d = DHCP_client("IsarLaptop","3c:97:0e:91:6c:0a","192.168.1.109",comment= "comment1")
#add_DHCP_client(s,pw,d)

#s.prompt()
#print(s.before)
#h=Host(IP_address = "192.168.1.108",HostName = "cpr108", alias = "C0A8016C")
#add_host(s,pw,h)
#s.prompt()
#print(s.before)
