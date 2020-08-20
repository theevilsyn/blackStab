from binascii import hexlify, unhexlify
from shutil import rmtree 
from os import mkdir, chdir, path, getcwd, remove, rmdir
from dataclasses import dataclass

@dataclass
class VMStruct:
    name: str
    tag: str
    udpPorts: list
    tcpPorts: list
    cpu: int = 2
    ram: int = 4

class VM:
    def create(self, funds, account, name, tag):
        if(not (funds > 100)):
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
    
    def modifyFirewall(self, account, tag, proto, port, operation):
        if(not path.exists(path.join(getcwd(), account, tag))):
            return 2
        else:
            pass
        
        vm = eval(unhexlify(open(path.join(getcwd(), account, tag)).read()))
        if(operation == 0):
            if(not (port in eval("vm.{}Ports".format(proto)))):
                eval("vm.{}Ports".format(proto)).append(port)
                open(path.join(getcwd(), account, tag), 'w').write(hexlify(str(vm).encode()).decode())
                return 0
            else:
                return 1
        else:
            if(port in eval("vm.{}Ports".format(proto))):
                eval("vm.{}Ports".format(proto)).remove(port)
                open(path.join(getcwd(), account, tag), 'w').write(hexlify(str(vm).encode()).decode())
                return 0
            else:
                return 1

    def modifyShape(self, account, balance, tag, resource, count, operation):
        """
        1GB RAM = 10$
        1 CPU = 40$
        Base VM = 100$
        Minimum RAM = 1GB
        Minimum CPU = 1
        """
        prices = {
                'ram': 30,
                'cpu': 70,
        }

        if(not path.exists(path.join(getcwd(), account, tag))):
            return 2
        else:
            pass

        vm = eval(unhexlify(open(path.join(getcwd(), account, tag)).read()))
        cost = prices[resource] * count
        if(operation == 0):
            if(cost > balance):
                return 1
            else:
                pass

            exec("vm.{} += count".format(resource))
            open(path.join(getcwd(), account, tag), 'w').write(hexlify(str(vm).encode()).decode())
            return 0

        else:
            if(eval("vm.{}".format(resource)) <= count):
                return 1
            else:
                pass
            exec("vm.{} -= count".format(resource))
            open(path.join(getcwd(), account, tag), 'w').write(hexlify(str(vm).encode()).decode())
            return 0

    def deleteVM(self, account, tag):
        if(not path.exists(path.join(getcwd(), account, tag))):
            return 1
        else:
            remove(path.join(path.join(getcwd(), account, tag)))
            return 0

    def removeAccount(self, account, challenge):
        if(not challenge):
            return 2 # incorrect password
        else:
            pass
        if(path.exists(path.join(getcwd(), account))):
            rmtree(account)
            return 0 # successfully deleted the account
        else:
            return 1 # user not found