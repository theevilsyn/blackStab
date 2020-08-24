import logging
from binascii import hexlify
from Crypto.PublicKey import RSA
from string import ascii_lowercase as letters
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode,b64encode
from random import choice

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
        try:
            conn.send(b"-337")
        except BrokenPipeError:
            pass
        conn.close()
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

def authenticate(conn):
    pubkey = b'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FR\nOEFNSUlCQ2dLQ0FRRUF5MksyVFZqY1NkcVhxWitpT3RBVQphbVFlWHBmaFdiZzFBVEZRNXhvR2Ez\ndlFMRXlEbjUyc2l2ZGNuWWU1KzdORFdkUjlVWFFISjY3SXlDcXY2SjhtCnpWM0JCRU9wYS9jOUZP\nS0xlelhxNXFpemRUaDBXWEFyNVZNNklWZk9YWnArNUptaEpROEdqemg4bmRsUENKMisKK3FONXpK\nbXVDb0Z6blFXMkdZOUVMNFUyQW9SYVR5cEErbFdJZnVCaURObG1lT0w1bDhQbGNLTGlFYUthcHZy\nZgpueXFOc0NrZmVwdFhjd284UmhSSWNobUVjaHBRTVZmYXBmMDFsQkZkZi9YTkxPU3dnS1NTNFQw\nV0lHUGxmelY1CjBCNXJJajF4UEo3bGI3UlpieGFueWZkRTcxRVV0UGhxdEhiaS9CQTVUeGQ2STFR\nWGhMVjRNSE5XaldoWjBnSzkKeFFJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg==\n'
    keyDER = b64decode(pubkey)
    challengept = (''.join(choice(letters) for i in range(128))).encode()
    keyPub = RSA.importKey(keyDER)
    cipher = Cipher_PKCS1_v1_5.new(keyPub)
    challengect = cipher.encrypt(challengept)
    finalchall = b64encode(challengect).decode()
    _send(conn, finalchall)
    resp = b64decode(_recv(conn))
    if challengept == resp:
        print("Authenticated")
        return True
    else:
        print("Auth wrong")
        return False


def createvm(conn, vm, account, email, password):
    vmname = _recv(conn)
    tag = _recv(conn)
    imageid = _recv(conn, onlypara=True)
    balance = account.showCredits(email)
    response = vm.createVM(funds=balance, account=hexlify(email.encode() + password.encode()), name=vmname, tag=tag.encode(), imageid=imageid)
    _send(conn, str(response), makefield=False)
    if(response == 0):
        account.useCredits(email=email, credits=150)

    logger.info("Created VM {} for {}".format(tag, email))