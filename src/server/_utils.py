import logging
from binascii import hexlify


logger = logging.getLogger('blackStab')
logger.setLevel(logging.DEBUG)

ch = logging.FileHandler('server.log')
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[*] %(asctime)s - %(levelname)s - %(message)s ')
ch.setFormatter(formatter)
logger.addHandler(ch)

make_field = lambda data: str(len(data)).ljust(4) + data

def recvbytes(conn, remains):
    buf = b""
    while remains:
        data = conn.recv(remains)
        if not data:
            break
        buf += data
        remains -= len(data)
    return buf

def register(conn, account, addr):
    username_len = int(recvbytes(conn, 4))
    username = recvbytes(conn,  username_len)

    email_len = int(recvbytes(conn, 4))
    email = recvbytes(conn, email_len)

    password_len = int(recvbytes(conn, 4))
    password = recvbytes(conn, password_len)

    _register = account.register(email=email.decode(), username=username.decode(), password=password.decode())
    conn.send(str(_register).ljust(4).encode())
    if( (_register == 1) or (_register == 2)):
        conn.close()
        account.cnx.close()
        exit()
    else:
        pass
    _nextaction = int(recvbytes(conn, 4))
    if(_nextaction == 1): #register again
        register(conn, account, addr)
        logger.info("{} requested register function".format(addr))
    elif(_nextaction == 2): #login
        login(conn, account)
        logger.info("{} logged in to {}".format(addr,email))
    else:
        conn.close()
        account.cnx.close()
        exit()

def login(conn, account):
    email_len = int(recvbytes(conn, 4))
    email = recvbytes(conn, email_len)

    password_len = int(recvbytes(conn, 4))
    password = recvbytes(conn, password_len)

    _login = account.check_login(email=email.decode(), password=password.decode())
    conn.send(str(_login).ljust(4).encode())
    if( (_login == 1) or (_login == 2)):
        conn.close()
        account.cnx.close()
        exit()
    else:
        pass
    return email, password

def createvm(conn, vm, account, email, password):
    vmname_len = int(recvbytes(conn, 4))
    vmname = recvbytes(conn, vmname_len)

    tag_len = int(recvbytes(conn, 4))
    tag = recvbytes(conn, tag_len)

    balance = account.showCredits
    response = vm.create(funds=balance, account=hexlify(email+password), name=vmname, tag=tag)
    conn.send(str(response).ljust(4).encode())
    logger("Created VM {} for {}".format(tag, email))