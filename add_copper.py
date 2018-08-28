import py_sudo_ssh
import os
starting_var =0xC0A80100

 
s=py_sudo_ssh.get_ssh_connection(Host,UserName,Password)
py_sudo_ssh.sudo(s,password,"sudo -i")

def add_copper(elevated_remoteShell,ip_computer_address,HardwareAdress):
    Alias=starting_var+ip_computer_address
    IP="192.168.1."+  str(ip_computer_address)
    HostName="cpr" + str(ip_computer_address)
    
    h=py_sudo_ssh.Host(IP_address =IP ,HostName = HostName, alias = Alias)
    py_sudo_ssh.add_host(elevated_remoteShell,h)
    
    create_new_pxlinux_cfg_file(elevated_remoteShell,Snapshot=HostName,FileName=Alias)

    Client = py_sudo_ssh.DHCP_client(HostName=HostName,hardware_ethernet=HardwareAdress,fixed_address=HostName,option_host_name=HostName)
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



