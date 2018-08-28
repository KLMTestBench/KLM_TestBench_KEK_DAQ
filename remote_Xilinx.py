import py_sudo_ssh

def Program_scrod(Host,UserName,Password,FileName):
    s=py_sudo_ssh.get_ssh_connection(Host,UserName,Password)
    dummyFolder = "~/"
    py_sudo_ssh.scp2Remote(Password,FileName,dummyFolder,UserName,Host)
    


def Program_SCROD_impl(s,Path,CommandFileName = "~/dummy.cmd", cleanUp = True):
    py_sudo_ssh.set_content(s,"setMode -bscan",CommandFileName,Append=False)
    py_sudo_ssh.set_content(s,"setCable -port auto",CommandFileName,Append=True)
    py_sudo_ssh.set_content(s,"Identify -inferir",CommandFileName,Append=True)
    py_sudo_ssh.set_content(s,"identifyMPM",CommandFileName,Append=True)
    progCommand = 'assignFile -p 1 -file "' + Path +'"'
    py_sudo_ssh.set_content(s,progCommand,CommandFileName,Append=True)
    py_sudo_ssh.set_content(s,"Program -p 1",CommandFileName,Append=True)
    py_sudo_ssh.set_content(s,"quit",CommandFileName,Append=True)

    Line = "impact -batch " +Path
    s.sendline(Line)
    s.prompt()
    return s.before




    