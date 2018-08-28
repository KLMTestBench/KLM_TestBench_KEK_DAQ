import py_sudo_ssh
import os





class COPPER_conf:
    def __init__(self,ID_number,HardwareAdress):
        self.ID_number=ID_number
        self.HardwareAdress=HardwareAdress

def add_copper(elevated_remoteShell,copper_conf):
    ip_computer_address=copper_conf.ID_number

    
    IP="192.168.1."+  str(ip_computer_address)
    px_cfg_fileName= ip2hex(IP)
    HostName="cpr" + str(ip_computer_address)
    
    h=py_sudo_ssh.Host(IP_address =IP ,HostName = HostName, alias = px_cfg_fileName)
    py_sudo_ssh.add_host(elevated_remoteShell,host=h)
    
    create_new_pxlinux_cfg_file(elevated_remoteShell,Snapshot=HostName,FileName=px_cfg_fileName)

    Client = py_sudo_ssh.DHCP_client(HostName=HostName,hardware_ethernet=copper_conf.HardwareAdress,fixed_address=HostName,option_host_name=HostName)
    py_sudo_ssh.add_DHCP_client(elevated_remoteShell,DHCP_cl=Client,restart=True)
         




def create_new_pxlinux_cfg_file(elevated_remoteShell,Snapshot,FileName,Path="/tftpboot/linux-install/pxelinux.cfg/"):
    FullName=Path+"/"+FileName
    py_sudo_ssh.set_content(elevated_remoteShell,"default bazinga",FileName=FullName,Append=False)
    py_sudo_ssh.set_content(elevated_remoteShell," ",FileName=FullName,Append=True)
    py_sudo_ssh.set_content(elevated_remoteShell,"label bazinga",FileName=FullName,Append=True)
    py_sudo_ssh.set_content(elevated_remoteShell,"    kernel bazinga/vmlinuz",FileName=FullName,Append=True)
    line ="    append  initrd=bazinga/initrd.img root=/dev/ram0 init=disklessrc NFSROOT=192.168.1.1:/tftpboot/copper ramdisk_size=28469 ETHERNET=eth0 SNAPSHOT="+Snapshot+ " -V -S pci=routeirq" 
    py_sudo_ssh.set_content(elevated_remoteShell,line,FileName=FullName,Append=True)
    py_sudo_ssh.set_content(elevated_remoteShell," ",FileName=FullName,Append=True)    

def ip2hex(ip):
    a = ip.split('.')
    b = hex(int(a[0]))[2:].zfill(2) + hex(int(a[1]))[2:].zfill(2) + hex(int(a[2]))[2:].zfill(2) + hex(int(a[3]))[2:].zfill(2)
    b = b.replace('0x', '')
    b = b.upper()
    return b

