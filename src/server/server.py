import socket
from time import sleep
from _utils import *
from _utils import _recv, _send
del(logging, ch, formatter, field, recvbytes) # just that code shows these are unused, remove later
from binascii import hexlify, unhexlify
from _thread import start_new_thread
from VM import VM, VMStruct, accounts


##########
## TODO ##
##########
###########################
###   Improve Logging   ###
###########################

def client_thread(conn, addr):
    vm = VM()
    account = accounts()
    actions = [
        "'createVM'",
        "'ruleAddTCP'",
        "'ruleAddUDP'",
        "'scaleMemory'",
        "'scaleCPU'",
        "'deleteVM'",
        "'deleteAccount'",
        "'statusofmyVM'",
        "'viewSubscription'",
        "'listallmyVMs'",
        "'noonecallsme'"
    ]
    if(authenticate(conn)):
        logger.info("{} authenticated".format(addr[0]))
        _send(conn, str(0), makefield=False)
    else:
        logger.info("Wrong auth attempt from {}")
        _send(conn, str(-1), makefield=False)
        conn.close()
        exit(-1)
    action_code = _recv(conn, onlypara=True)
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
        action = _recv(conn, onlypara=True)
        if(action == -337): # bye bye received
            logger.info("{} Bye Bye requested".format(addr[0]))
            conn.close()
            exit()
        elif(action == 0): # wants to call a function
            action = _recv(conn)
            if(action not in actions):
                _send(conn, str(-337), makefield=False)
            else:
                pass
            if(cmp(action, 'createVM')):
                logger.info("{} requested {} function".format(addr[0], action))
                vmname = _recv(conn)
                vmtag = _recv(conn)
                imageid = _recv(conn, onlypara=True)
                balance = account.showField(email=email)
                resp = vm.createVM(funds=balance, account=hexlify(email.encode() + password.encode()), name=vmname, tag=vmtag.encode(), imageid=imageid)
                _send(conn, str(resp), makefield=False)
                if(resp == 0):
                    account.useCredits(email=email, credits=150)
                    logger.info("Created VM {} for {}".format(vmtag, email))

            elif(cmp(action, 'ruleAddTCP')):
                logger.info("{} requested {} function".format(addr[0], action))
                tag = _recv(conn)
                port = _recv(conn, _len=5, onlypara=True)
                operation = _recv(conn, onlypara=True)
                response = vm.modifyFirewall(account=hexlify(email.encode() + password.encode()), tag=tag.encode(), proto='tcp', port=port, operation=operation)
                _send(conn, str(response), makefield=False)
            
            elif(cmp(action, 'ruleAddUDP')):
                logger.info("{} requested {} function".format(addr[0], action))
                tag = _recv(conn)
                port = _recv(conn, _len=5, onlypara=True)
                operation = _recv(conn, onlypara=True)
                response = vm.modifyFirewall(account=hexlify(email.encode() + password.encode()), tag=tag.encode(), proto='udp', port=port, operation=operation)
                _send(conn, str(response), makefield=False)

            elif(cmp(action, 'scaleMemory')):
                logger.info("{} requested {} function".format(addr[0], action))
                tag = _recv(conn)
                operation = _recv(conn, onlypara=True)
                count = _recv(conn, onlypara=4)
                _credits = account.showField(email=email)                
                response = vm.modifyShape(account=hexlify(email.encode() + password.encode()), balance=_credits, tag=tag.encode(), resource='ram', count=count, operation=operation)
                _send(conn, str(response), makefield=False)
                if(response == 0 and operation == 1):
                    account.useCredits(email=email, credits=count*30)
                            
            elif(cmp(action, 'scaleCPU')):
                logger.info("{} requested {} function".format(addr[0], action))
                tag = _recv(conn)
                operation = _recv(conn, onlypara=True)
                count = _recv(conn, onlypara=True)
                _credits = account.showField(email=email)                
                response = vm.modifyShape(account=hexlify(email.encode() + password.encode()), balance=_credits, tag=tag.encode(), resource='cpu', count=count, operation=operation)
                _send(conn, str(response), makefield=False)                
                if(response == 0 and operation == 1):
                    account.useCredits(email=email, credits=count*70)
                        
            elif(cmp(action, 'deleteVM')):
                logger.info("{} requested {} function".format(addr[0], action))
                tag = _recv(conn)
                response = vm.deleteVM(account=hexlify(email.encode() + password.encode()), tag=tag.encode())
                _send(conn, str(response), makefield=False)

            elif(cmp(action, 'deleteAccount')):
                logger.info("{} requested {} function".format(addr[0], action))
                password = _recv(conn)
                response = account.removeAccount(email=email, password=password)
                vm.removeAccount(account=hexlify(email.encode()+password.encode()), challenge=True)
                _send(conn, str(response), makefield=False)
                if(response == 0):
                    logger.info("Deleted account of {} : Request from {}".format(email, addr[0]))
                    conn.close()
                    exit()
                else:
                    pass
            
            elif(cmp(action, 'statusofmyVM')):
                logger.info("{} requested {} function".format(addr[0], action))
                tag = _recv(conn)

                status = vm.statusofVM(account=hexlify(email.encode() + password.encode()), tag=tag.encode())
                _send(conn, str(status))

            elif(cmp(action, 'viewSubscription')):
                logger.info("{} requested {} function".format(addr[0], action))
                credits_left = account.showField(email=email)
                _send(conn, str(credits_left), makefield=False)

            elif(cmp(action, 'listallmyVMs')):
                logger.info("{} requested {} function".format(addr[0], action))
                all_my_vms = vm.listmyVMs(account=hexlify(email.encode() + password.encode()))
                if(all_my_vms == 0):
                    _send(conn, str(0), makefield=False)
                else:
                    count = len(all_my_vms)
                    _send(conn, str(all_my_vms))

            elif(cmp(action, 'noonecallsme')):
                logger.info("{} requested {} function".format(addr[0], action))
                allstatus = vm.masterlist()
                if(isprivileged(conn, email)):
                   _send(conn, allstatus)
                else:
                    message = "Authentication Failed :("
                    _send(conn, message)
            else:
                logger.warn("Unexpected function call from {} : {}".format(addr[0], action))
                conn.send(unhexlify(b'4655434b'))


HOST = ''
PORT = 9999


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    logger.error("Could not create socket. Error: " + str(msg))
    exit()

logger.info("Socket Created")

try:
    s.bind((HOST, PORT))
    logger.info("Socket Bound to port " + str(PORT))
except socket.error as msg:
    logger.error("Bind Failed. Error: {}".format(msg))
    exit()

s.listen(10)

while True:
    conn, addr = s.accept()
    logger.info("Connection received from " + addr[0] + ":" + str(addr[1]))

    start_new_thread(client_thread, (conn,addr))

s.close()
