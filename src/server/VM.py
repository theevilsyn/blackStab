from json import load
from binascii import hexlify, unhexlify
from shutil import rmtree
import mysql.connector
from base64 import b64encode as encode
from mysql.connector import errorcode
from os import makedirs, path, remove, listdir, walk
from dataclasses import dataclass


with open("config.json",'r') as file:
  CONFIG = load(file)

@dataclass
class VMStruct:
    name: str
    tag: str
    image: str
    udpPorts: list
    tcpPorts: list
    cpu: int = 2
    ram: int = 4

"""
OSes | 0--> Archlinux | 1--> Ubuntu16 | 2--> Ubuntu18 |
     | 3--> CentOS7 | 4--> Oracle Linux 6 | 5--> OpenSUSE | 6-->Windows Server |
"""
class VM:
    def __init__(self):
        self.region = CONFIG['region'].encode()
        self.statuscount = 25
        self.images = {
            0: "Archlinux",
            1: "Ubuntu 16.04",
            2: "Ubuntu 18.04",
            3: "CentOS 7",
            4: "Oracle Linux 6",
            5: "OpenSUSE by SUSE",
            6: "Windows Server 2019 LTSC"
        }

        return

    def createVM(self, funds, account, name, tag, imageid):
        if(not (funds > 100)):
            return 2
        if(not path.exists(path.join(self.region, account))):
            makedirs(path.join(self.region, account))
        vm = VMStruct(name=name, tag=tag, image=self.images[imageid], tcpPorts=[22,80] , udpPorts=[53])
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
        if(operation == 1):
            if(not (port in eval("vm.{}Ports".format(proto)))):
                eval("vm.{}Ports".format(proto)).append(port)
                eval("vm.{}Ports".format(proto)).sort()
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
        1GB RAM = 30$
        1 CPU = 70$
        Base VM = 150$
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
        if(operation == 1):
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
            return 0 # successfully deleted all the VMs under the account
        else:
            return 1 # no VMs under the account

    def statusofVM(self, account, tag): #the vulnerable function
        if(not path.exists(path.join(self.region, account, tag))):
            data = "The VM with the tag {} does not exist".format(tag.decode())
            return data
        else:
            pass

        vm = eval(unhexlify(open(path.join(self.region, account, tag)).read()))
        data = """
        VM Name: {}
        VM Tag: {} // encoded for security reasons
        Operating System: {}
        Associated to Account: {}
        TCP Ports Open: {}
        UDP Ports Open: {}
        Specifications: Number of CPUs are {} and the RAM is {} GB
        """.format(vm.name, encode(vm.tag).decode(), vm.image,account.decode(), str(vm.tcpPorts), str(vm.udpPorts), str(vm.cpu), str(vm.ram))
        return data

    def listmyVMs(self, account):
        if(len(listdir(path.join(self.region, account))) == 0):
            return 0
        else:
            pass
        vmtags = '\n'.join(listdir(path.join(self.region.decode(), account.decode())))
        return vmtags

    def masterlist(self): # latest VMs that are spawned
        vms = []
        for account in listdir(self.region):
            for tag in listdir(path.join(self.region, account)):
                vms.append((self.statusofVM(account=account, tag=tag), tag))
                vms.sort(key=lambda x: path.getatime(path.join(self.region, account, x[1])))
                if(len(vms) > self.statuscount):
                    vms = vms[:self.statuscount]
        return '\n'.join(list(map(lambda vm: vm[0], vms)))

class accounts:
    def __init__(self):
        self.cnx = mysql.connector.connect(host="localhost",user=CONFIG['db_user'],password=CONFIG['db_pass'],database=CONFIG['database'])
        return

    def register(self, email, username, password):
        cnx = self.cnx
        cursor = cnx.cursor()
        cursor.execute("SELECT * from users where email='{}'".format(email))
        acc_match = cursor.fetchall()
        if(len(acc_match)):
            return 1 # email already taken
        elif(len(password) < 12):
            return 2
        else:
            pass
        _register = ("INSERT INTO users "
                    "(email, username, password, credits) "
                    "VALUES (%s, %s, %s, %s)")
        cursor.execute(_register, (email, username, password, 1000))
        cnx.commit()
        return 0

    def check_login(self, email, password):
        cnx = self.cnx
        cursor = cnx.cursor()
        cursor.execute("SELECT * from users where email='{}'".format(email))
        acc_match = cursor.fetchall()
        if(not len(acc_match)):
            return 1
        else:
            pass
        if(not (acc_match[0][2] == password)):
            return 2
        else:
            pass
        return 0
    
    def showCredits(self, email):
        cnx = self.cnx
        cursor = cnx.cursor()
        cursor.execute("SELECT credits from users where email='{}'".format(email))
        _credits = cursor.fetchall()[0][0]
        return _credits

    def useCredits(self, email, credits):
        cnx = self.cnx
        cursor = cnx.cursor()
        _credits = self.showCredits(email=email)
        cursor.execute("UPDATE users SET credits={} WHERE email='{}'".format((_credits-credits), email))
        cnx.commit()

    def removeAccount(self, email, password):
        cnx = self.cnx
        cursor = cnx.cursor()
        cursor.execute("SELECT password from users where email='{}'".format(email))
        acc_match = cursor.fetchall()
        if(not (acc_match[0][0] == password)):
            return 1
        else:
            pass   
        _remove = ("DELETE FROM users "
                "where email='{}'".format(email))
        cursor.execute(_remove)
        cnx.commit()
        return 0
