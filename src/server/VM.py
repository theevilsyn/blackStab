from binascii import hexlify, unhexlify
from os import mkdir, chdir, path, getcwd
from dataclasses import dataclass

@dataclass
class VMStruct:
    name: str
    tag: str
    udpPorts: list
    tcpPorts: list
    CPU: int = 4
    RAM: int = 8

class VM:
    def create(self, funds, account, name, tag):
        if(not funds):
            return 2
        if(not path.exists(path.join(getcwd(), account))):
            mkdir(account)
        vm = VMStruct(name=name, tag=tag, tcpPorts=[22,80], udpPorts=[53])
        content = hexlify(str(vm).encode())
        if(not path.exists(path.join(getcwd(), account, tag))):
            open(path.join(getcwd(), account, tag), 'w').write(content.decode())
        else:
            return 1
        return 0
    
    def ruleaddtcp(self):
        return 
