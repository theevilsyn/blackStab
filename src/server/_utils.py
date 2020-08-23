import logging
from binascii import hexlify


logger = logging.getLogger('blackStab')
logger.setLevel(logging.DEBUG)

# ch = logging.FileHandler('server.log')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[*] %(asctime)s - %(levelname)s - %(message)s ')
ch.setFormatter(formatter)
logger.addHandler(ch)

field = lambda data: str(len(data)).ljust(8, chr(0)).encode() + data.encode()

def _send(conn, data, makefield=True):
    conn.send(data.ljust(8,chr(0)).encode()) if not makefield else conn.send(field(data))

def _recv(conn, _len=8, onlypara=False):
    try:
        field_len = int(recvbytes(conn, _len).replace(chr(0).encode(),b''))
    except ValueError:
        print("Something Went Wrong!")
        conn.send(b"-337")
        exit()
    return recvbytes(conn, field_len).decode() if not onlypara else field_len

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
    email = _recv(conn)
    username = _recv(conn)
    password = _recv(conn)

    _register = account.register(email=email, username=username, password=password)
    _send(conn, str(_register), makefield=False)
    if( (_register == 1) or (_register == 2)):
        logger.info("Wrong register attempt from {} : ERROR Code: {}".format(addr[0], _register))
        conn.close()
        account.cnx.close()
        exit()
    else:
        pass
    logger.info("Registerd a new user {} from {}".format(email, addr[0]))
    conn.close()
    account.cnx.close()
    exit()

def login(conn, account, addr):
    email = _recv(conn)
    password = _recv(conn)

    _login = account.check_login(email=email, password=password)
    _send(conn, str(_login), makefield=False)
    if( (_login == 1) or (_login == 2)):
        conn.close()
        account.cnx.close()
        exit()
    else:
        logger.info("{} logged in to account {}".format(addr[0], email))
        pass
    return email, password

def createvm(conn, vm, account, email, password):
    vmname = _recv(conn)
    tag = _recv(conn)

    balance = account.showCredits(email)
    response = vm.createVM(funds=balance, account=hexlify(email.encode() + password.encode()), name=vmname, tag=tag.encode())
    _send(conn, str(response), makefield=False)
    if(response == 0):
        account.useCredits(email=email, credits=150)

    logger.info("Created VM {} for {}".format(tag, email))