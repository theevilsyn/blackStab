import socket
from sys import argv

def menu(io):
    print("""
    1. CreateVM
    2. ModifyVM
    3. DeleteVM
    4. VMStatus
    5. ListMyVMs
    6. View Subscription
    7. Delete Account
    8. Exit
    """)

    try:
        choice = int(input())
        if(choice == 1):
            createvm(io)
        elif(choice == 2):
            modifyvm(io)
        elif(choice == 3):
            deletevm(io)
        elif(choice == 4):
            vmstatus(io)
        elif(choice == 5):
            listmyvms(io)
        elif(choice == 6):
            viewsubscription(io)
        elif(choice == 7):
            deleteacc(io)
        elif(choice == 8):
            _exit(io)
        else:
            menu(io)
    except KeyboardInterrupt:
        _exit(io)

def recvbytes(conn, remains):
    buf = b""
    while remains:
        data = conn.recv(remains)
        if not data:
            break
        buf += data
        remains -= len(data)
    return buf

def _exit(io):
    print("See You Again!!")
    io.send(b'-337')
    io.close()
    exit()

def catchint(io):
    response = int(io.recv(8).replace(b'\x00',b''))
    if(response == -337):
        print("The server terminated the connection!!")
        io.close()
        exit(-1)
    else:
        return response

def deleteacc(io):
    data = str(0).ljust(8, chr(0))
    data += str(len('deleteAccount')).ljust(8, chr(0))
    data += 'deleteAccount'
    password = input("For security reasons, please enter your password: ")
    data += str(len(password)).ljust(8, chr(0))
    data += password
    io.send(data.encode())
    response = catchint(io)
    if(response == 2):
        print("You entered a wrong password.")
        menu(io)
    elif(response == 0):
        print("Successfully Removed your Account, Bye!")

def viewsubscription(io):
    data = str(0).ljust(8, chr(0))
    data += str(len('viewSubscription')).ljust(8, chr(0))
    data += 'viewSubscription'
    io.send(data.encode())
    _credits = catchint(io)
    print("You have {} credits left in your account".format(_credits))
    menu(io)

def listmyvms(io):
    data = str(0).ljust(8, chr(0))
    data += str(len('listallmyVMs')).ljust(8, chr(0))
    data += 'listallmyVMs'
    io.send(data.encode())
    count = catchint(io)
    if(count == 0):
        print("You have 0 VMs associated to your account")
        menu(io)
    else:
        vms = io.recv(count)
        print(vms.decode())
        menu(io)

def vmstatus(io):
    data = str(0).ljust(8, chr(0))
    data += str(len('statusofmyVM')).ljust(8, chr(0))
    data += 'statusofmyVM'
    vm_tag = input("VM Tag: ")
    data += str(len(vm_tag)).ljust(8, chr(0))
    data += vm_tag
    io.send(data.encode())
    data_len = catchint(io)
    status = recvbytes(io, data_len)
    print(status.decode())
    print("\n\n")
    menu(io)

def deletevm(io):
    data = str(0).ljust(8, chr(0))
    data += str(len('deleteVM')).ljust(8, chr(0))
    data += 'deleteVM'
    vm_tag = input("VM Tag: ")
    data += str(len(vm_tag)).ljust(8, chr(0))
    data += vm_tag
    io.send(data.encode())
    response = catchint(io)
    if(response == 1):
        print("VM with the requested tag not found")
        menu(io)
    else:
        print("Successfully deleted the requested VM")
        menu(io)

def modifyvm(io):
    data = str(0).ljust(8, chr(0))
    print("""
    1. Edit Firewall Rules
    2. Scale a VM
    """)
    choice = int(input())
    if(choice == 1):
        print("""
        1. Open/Close a TCP Port
        2. Open/Close a UDP Port
        """)
        proto = int(input())
        if(proto == 1):
            data += str(len('ruleAddTCP')).ljust(8, chr(0))
            data += 'ruleAddTCP'
            vm_tag = input("VM Tag: ")
            data += str(len(vm_tag)).ljust(8, chr(0))
            data += vm_tag

            port = int(input("Port: "))
            if(port > 65535):
                print("Please enter a valid port next time!!")
                menu(io)
            else:
                pass
            data += str(port).ljust(5)
            
            print("""
            1. Open {} TCP Port
            2. Close {} TCP Port
            """.format(port, port))
            operation = int(input()) 
            data += str(operation).ljust(8, chr(0))
            io.send(data.encode())
            response = catchint(io)
            if(operation == 1):
                action = 'open'
            else:
                action = 'clos'
            if(response == 0):
                print("Successfully {}ed TCP port {}".format(action, port))
                menu(io)
            elif(response == 1):
                print("TCP port {} already {}ed".format(port, action))
                menu(io)
            elif (response == 2):
                print("VM with the requested tag not found")
                menu(io)
            else:
                print("Something Went Wrong!!")
                _exit(io)

        elif(proto == 2):
            data += str(len('ruleAddUDP')).ljust(8, chr(0))
            data += 'ruleAddUDP'
            vm_tag = input("VM Tag: ")
            data += str(len(vm_tag)).ljust(8, chr(0))
            data += vm_tag

            port = int(input("Port: "))
            if(port > 65535):
                print("Please select a valid port next time!!")
                menu(io)
            data += str(port).ljust(5)
            
            print("""
            1. Open {} UDP Port
            2. Close {} UDP Port
            """.format(port, port))
            operation = int(input()) 
            data += str(operation).ljust(8, chr(0))
            io.send(data.encode())
            response = catchint(io)
            if(operation == 1):
                action = 'open'
            else:
                action = 'clos'
            if(response == 0):
                print("Successfully {}ed UDP port {}".format(action, port))
                menu(io)
            elif(response == 1):
                print("UDP port {} already {}ed".format(port, action))
                menu(io)
            elif(response == 2):
                print("VM with the requested tag not found")
                menu(io)
            else:
                print("Something Went Wrong!!")
                _exit(io)
        
        else:
            print("Undefined choice selected")
            menu(io)
    elif(choice == 2):
        print("""
        1. Add/Remove RAM
        2. Upscale/Downscale CPU
        """)
        resource = int(input())
        if(resource == 1):
            data += str(len('scaleMemory')).ljust(8, chr(0))
            data += 'scaleMemory'

            vm_tag = input("VM Tag: ")
            data += str(len(vm_tag)).ljust(8, chr(0))
            data += vm_tag

            print("""
            1. Add RAM
            2. Remove RAM
            """)
            operation = int(input())
            
            if(operation == 1):
                count = int(input("Enter how many GB should be added: "))
                data += str(operation).ljust(8, chr(0))
                data += str(count).ljust(8, chr(0))
                io.send(data.encode())
                response = catchint(io)
                if(response == 0):
                    print("Successfully Added {} GB memory to your VM".format(count))
                    menu(io)
                elif(response == 1):
                    print("Action Failed, Insufficient Funds to complete the operation.")
                    menu(io)
                elif(response == 2):
                    print("Action Failed, VM with the requested tag not found.")
                    menu(io)
            elif(operation == 2):
                count = int(input("Enter how many GB should be removed: "))
                data += str(operation).ljust(8, chr(0))
                data += str(count).ljust(8, chr(0))
                io.send(data.encode())
                response = catchint(io)
                if(response == 0):
                    print("Successfully Removed {} GB memory to your VM".format(count))
                    menu(io)
                elif(response == 1):
                    print("Action Failed, the requested quantity is greater than the current VM's RAM.")
                    menu(io)
                elif(response == 2):
                    print("Action Failed, VM with the requested tag not found.")
                    menu(io)
            else:
                print("Undefined option selected.")
                menu(io)
        elif(resource == 2):
            data += str(len('scaleCPU')).ljust(8, chr(0))
            data += 'scaleCPU'
            vm_tag = input("VM Tag: ")
            data += str(len(vm_tag)).ljust(8, chr(0))
            data += vm_tag
            print("""
            1. Upscale CPU
            2. Downscale CPU
            """)
            operation = int(input())
            if(operation == 1):
                count = int(input("Enter how many CPUs should be added: "))
                data += str(operation).ljust(8, chr(0))
                data += str(count).ljust(8, chr(0))
                io.send(data.encode())
                response = catchint(io)
                if(response == 0):
                    print("Successfully Added {} CPUs to your VM".format(count))
                    menu(io)
                elif(response == 1):
                    print("Action Failed, Insufficient Funds to complete the operation.")
                    menu(io)
                elif(response == 2):
                    print("Action Failed, VM with the requested tag not found.")
                    menu(io)
                else:
                    print("Something Went Wrong!!")
                    _exit(io)

            elif(operation == 2):
                count = int(input("Enter how many CPUs should be removed: "))
                data += str(operation).ljust(8, chr(0))
                data += str(count).ljust(8, chr(0))
                io.send(data.encode())
                response = catchint(io)
                if(response == 0):
                    print("Successfully Removed {} CPUs to your VM".format(count))
                    menu(io)
                elif(response == 1):
                    print("Action Failed, the requested quantity is greater than the current VM's CPU count.")
                    menu(io)
                elif(response == 2):
                    print("Action Failed, VM with the requested tag not found.")
                    menu(io)
                else:
                    print("Something Went Wrong!!")
                    _exit(io)
            else:
                print("Undefined option selected.")
                menu(io)
        else:
            print("Undefined option selected")
            menu(io)    
    else:
        print("Undefined Option Selected.")
        menu(io)

def createvm(io):
    data = str(0).ljust(8, chr(0))
    data += str(len('createVM')).ljust(8, chr(0))
    data += 'createVM'
    vm_name = input("VM Name: ")
    data += str(len(vm_name)).ljust(8, chr(0))
    data += vm_name

    vm_tag = input("VM Tag: ")
    data += str(len(vm_tag)).ljust(8, chr(0))
    data += vm_tag
    io.send(data.encode())
    response = catchint(io)
    if(response == 2):
        print("Funds not sufficient to spawn a VM")
        menu(io)
    elif(response == 1):
        print("VM with the requested tag is already present")
        menu(io)
    elif(response == 0):
        print("Successfully created the VM")
        menu(io)
    else:
        print("Something Went Wrong!!!")
        _exit(io)


def register(io):
    data='1'.ljust(8, chr(0))

    email = input("Email: ")
    data+=str(len(email)).ljust(8, chr(0))
    data+=email

    username = input("Username: ")
    data+=str(len(username)).ljust(8, chr(0))
    data+=username

    password = input("Password: ")
    data+=str(len(password)).ljust(8, chr(0))
    data+=password

    io.send(data.encode())
    response = catchint(io)

    if(int(response == 1)):
        print("Email already Taken :(")
        _exit(io)
    elif(int(response) == 2):
        print("Password not greater than 12 :/")
        exit()
    elif(response == 0):
        print("Registration Successful")
    else:
        print("Something Went Wrong!!")
        _exit(io)
        


def login(io):
    data='2'.ljust(8, chr(0))
    email = input("Email: ")
    data+=str(len(email)).ljust(8, chr(0))
    data+=email

    password = input("Password: ")
    data+=str(len(password)).ljust(8, chr(0))
    data+=password
    io.send(data.encode())
    response = catchint(io)
    if(response == 0):
        print("Successfully logged in")
        menu(io)
    elif(response == 1):
        print("User not found")
        exit()
    elif(response == 2):
        print("Password Incorrect")
        exit()
    else:
        print("Something Went Wrong")
        _exit(io)


def start(io):
    print("""
        1. Register
        2. Login
        3. Exit
        """)
    choice = int(input())
    if(choice == 1):
        register(io)
    elif(choice == 2):
        login(io)
    elif(choice == 3):
        _exit(io)
    else:
        print("Select a valid option")
        start(io)


io = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
io.connect((argv[1], int(argv[2])))

try:
    start(io)        
except KeyboardInterrupt:
    _exit(io)