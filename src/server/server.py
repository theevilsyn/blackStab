import socket
from _utils import *
del(logging, ch, formatter) # just that code shows these are unused, remove later
from binascii import hexlify, unhexlify
from _thread import start_new_thread
from VM import VM, VMStruct, accounts


##########
## TODO ##
##########
###########################
###   Improve Logging   ###
###########################

HOST = ''
PORT = 9999


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    logger.info("Could not create socket. Error: " + str(msg))
    exit()

logger.info("Socket Created")

try:
    s.bind((HOST, PORT))
    logger.info("Socket Bound to port " + str(PORT))
except socket.error as msg:
    logger.info("Bind Failed. Error: {}".format(msg))
    exit()

s.listen(10)


def client_thread(conn, addr):
    vm = VM()
    account = accounts()
    actions = [
        'createVM',
        'ruleAddTCP',
        'ruleAddUDP',
        'scaleMemory',
        'scaleCPU',
        'deleteVM',
        'deleteAccount',
        'statusofmyVM',
        'viewSubscription',
        'listallmyVMs',
        'noonecallsme'
    ]
    
    # timestamp = recvbytes(conn, 8)
    
    action_code = int(recvbytes(conn, 4))
    if(action_code == 1): # register
        logger.info("{} requested register function".format(addr[0]))
        register(conn, account, addr)

    elif(action_code == 2): # login
        email, password = login(conn, account, addr)
        logger.info("{} logged in to {}".format(addr[0],email))
    else:
        conn.close()
        logger.info("{} Bye Bye requested".format(addr[0]))
        exit()
    while True:
        action = int(recvbytes(conn, 4))
        if(action == 1337): # bye bye received
            logger.info("{} Bye Bye requested".format(addr[0]))
            conn.close()
            exit()
        elif(action == 0): # wants to call a function
            action_len = int(recvbytes(conn, 4))
            action = recvbytes(conn, action_len).decode()
            if(action not in actions):
                conn.send(str(-1).ljust(4).encode())
            else:
                pass
            if(action == 'createVM'):
                logger.info("{} requested {} function".format(addr[0], action))
                createvm(conn, vm, account, email, password)
            
            elif(action == 'ruleAddTCP'):
                logger.info("{} requested {} function".format(addr[0], action))
                tag_len = int(recvbytes(conn, 4))
                tag = recvbytes(conn, tag_len)
                port = int(recvbytes(conn, 5)) # receive 5 bytes because max number 65535
                operation = int(recvbytes(conn, 4))
                response = vm.modifyFirewall(account=hexlify(email+password), tag=tag, proto='tcp', port=port, operation=operation)
                conn.send(str(response).ljust(4).encode())
            
            elif(action == 'ruleAddUDP'):
                logger.info("{} requested {} function".format(addr[0], action))
                tag_len = int(recvbytes(conn, 4))
                tag = recvbytes(conn, tag_len)
                port = int(recvbytes(conn, 5)) # receive 5 bytes because max number 65535
                operation = int(recvbytes(conn, 4))
                response = vm.modifyFirewall(account=hexlify(email+password), tag=tag, proto='udp', port=port, operation=operation)
                conn.send(str(response).ljust(4).encode())
                
            elif(action == 'scaleMemory'):
                logger.info("{} requested {} function".format(addr[0], action))
                tag_len = int(recvbytes(conn, 4))
                tag = recvbytes(conn, tag_len)
                operation = int(recvbytes(conn, 4)) #0 for upscale; 1 for downscale
                count = int(recvbytes(conn, 4))
                _credits = account.showCredits(email=email)
                response = vm.modifyShape(account=hexlify(email+password), balance=_credits, tag=tag, resource='ram', count=count, operation=operation)
                conn.send(str(response).ljust(4).encode())
                            
            elif(action == 'scaleCPU'):
                logger.info("{} requested {} function".format(addr[0], action))
                tag_len = int(recvbytes(conn, 4))
                tag = recvbytes(conn, tag_len)
                operation = int(recvbytes(conn, 4))
                count = int(recvbytes(conn, 4))
                _credits = account.showCredits(email=email)
                response = vm.modifyShape(account=hexlify(email+password), balance=_credits, tag=tag, resource='cpu', count=count, operation=operation)
                conn.send(str(response).ljust(4).encode())
                        
            elif(action == 'deleteVM'):
                logger.info("{} requested {} function".format(addr[0], action))
                tag_len = int(recvbytes(conn, 4))
                tag = recvbytes(conn, tag_len)
                response = vm.deleteVM(account=hexlify(email+password), tag=tag)
                conn.send(str(response).ljust(4).encode())

            elif(action == 'deleteAccount'):
                logger.info("{} requested {} function".format(addr[0], action))
                password_len = int(recvbytes(conn, 4))
                password = recvbytes(conn, password_len)
                response = account.removeAccount(email=email, password=password)
                vm.removeAccount(account=hexlify(email+password), challenge=True)
                conn.send(str(response).ljust(4).encode())
                if(response == 0):
                    logger.info("Deleted account of {} : Reques from {}".format(email, addr[0]))
                    conn.close()
                    exit()
                else:
                    pass
            
            elif(action == 'statusofmyVM'):
                logger.info("{} requested {} function".format(addr[0], action))
                tag_len = int(recvbytes(conn, 4))
                tag = recvbytes(conn, tag_len)

                status = vm.statusofVM(account=hexlify(email+password), tag=tag)
                conn.send(str(len(status)).ljust(4).encode())
                conn.send(status)
            
            elif(action == 'viewSubscription'):
                logger.info("{} requested {} function".format(addr[0], action))
                credits_left = account.showCredits(email=email)
                conn.send(str(credits_left).ljust(4).encode())

            elif(action == 'listallmyVMs'):
                logger.info("{} requested {} function".format(addr[0], action))
                all_my_vms = vm.listmyVMs(account=hexlify(email, password))
                if(all_my_vms == 0):
                    conn.send(str(0).ljust(4).encode())
                else:
                    count = len(all_my_vms)
                    conn.send(str(count).ljust(4).encode())
                    conn.send(all_my_vms.encode())

            elif(action == 'noonecallsme'):
                logger.info("{} requested {} function".format(addr[0], action))
                alltags = vm.masterlist()
                conn.send(str(len(alltags)).ljust(4).encode())
                conn.send(alltags.encode())
            
            else:
                logger.warn("Unexpected function call from {} : {}".format(addr[0], action))
                conn.send(b'FUCK') # no proper function is called client prints something went wrong


while True:
    conn, addr = s.accept()
    logger.info("Connection received from " + addr[0] + ":" + str(addr[1]))

    start_new_thread(client_thread, (conn,addr))

s.close()
