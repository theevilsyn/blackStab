from binascii import hexlify, unhexlify
from shutil import rmtree 
from os import makedirs, path, remove, listdir, walk
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
    def __init__(self):
        self.region = "/tmp/VMs"
        return
    def create(self, funds, account, name, tag):
        if(not (funds > 100)):
            return 2
        if(not path.exists(path.join(self.region, account))):
            makedirs(path.join(self.region, account))
        vm = VMStruct(name=name, tag=tag, tcpPorts=[22,80], udpPorts=[53])
        if(not path.exists(path.join(self.region, account, tag))):
            open(path.join(self.region, account, tag), 'w').write(hexlify(str(vm).encode()).decode())
        else:
            return 1
        return 0
    
    def modifyFirewall(self, account, tag, proto, port, operation):
        if(not path.exists(path.join(self.region, account, tag))):
            return 2
        else:
            pass
        
        vm = eval(unhexlify(open(path.join(self.region, account, tag)).read()))
        if(operation == 0):
            if(not (port in eval("vm.{}Ports".format(proto)))):
                eval("vm.{}Ports".format(proto)).append(port)
                open(path.join(self.region, account, tag), 'w').write(hexlify(str(vm).encode()).decode())
                return 0
            else:
                return 1
        else:
            if(port in eval("vm.{}Ports".format(proto))):
                eval("vm.{}Ports".format(proto)).remove(port)
                open(path.join(self.region, account, tag), 'w').write(hexlify(str(vm).encode()).decode())
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

        if(not path.exists(path.join(self.region, account, tag))):
            return 2
        else:
            pass

        vm = eval(unhexlify(open(path.join(self.region, account, tag)).read()))
        cost = prices[resource] * count
        if(operation == 0):
            if(cost > balance):
                return 1
            else:
                pass

            exec("vm.{} += count".format(resource))
            open(path.join(self.region, account, tag), 'w').write(hexlify(str(vm).encode()).decode())
            return 0

        else:
            if(eval("vm.{}".format(resource)) <= count):
                return 1
            else:
                pass
            exec("vm.{} -= count".format(resource))
            open(path.join(self.region, account, tag), 'w').write(hexlify(str(vm).encode()).decode())
            return 0

    def deleteVM(self, account, tag):
        if(not path.exists(path.join(self.region, account, tag))):
            return 1
        else:
            remove(path.join(path.join(self.region, account, tag)))
            return 0

    def removeAccount(self, account, challenge):
        if(not challenge):
            return 2 # incorrect password
        else:
            pass
        if(path.exists(path.join(self.region, account))):
            rmtree(path.join(self.region, account))
            return 0 # successfully deleted the account
        else:
            return 1 # user not found

    def statusofVM(self, account, tag): #the vulnerable function
        if(not path.exists(path.join(self.region, account, tag))):
            data = "The VM with the tag {} does not exist".format(tag)
            return data
        else:
            pass

        vm = eval(unhexlify(open(path.join(self.region, account, tag)).read()))
        data = """
        VM Name: {}
        VM Tag: {}
        TCP Ports Open: {}
        UDP Ports Open: {}
        Specifications: Number of CPUs are {} and the RAM is {} GB
        """.format(vm.name, vm.tag, str(vm.tcpPorts), str(vm.udpPorts), str(vm.cpu), str(vm.ram))
        return data

    def listmyVMs(self, account):
        if(not path.exists(path.join(self.region, account))):
            return -1
        else:
            pass
        
        vmtags = '\n'.join(listdir(path.join(self.region, account)))
        return vmtags

    def masterlist(self):
        vms = []
        for r, d, f in walk(path.join(self.region)):
            for vm in f:
               vms.append(vm) 
        return '\n'.join(vms)
