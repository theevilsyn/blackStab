from re import sub as rep
import logging
from ast import literal_eval as deval
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
        logger.info("Disconnected {} upon their request".format(conn.getpeername()))
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
        try:
            data = conn.recv(remains)
        except ConnectionResetError:
            print("Client disconnected")
            exit(0)
        if not data:
            break
        buf += data
        remains -= len(data)
    return (lambda buf: rep(r'[-;"#$%&(!)*+:;<>?\\^_`{|}~]', r'', buf.decode()).encode())(buf)

def register(conn, account, addr):
    email = _recv(conn)
    username = _recv(conn)
    password = _recv(conn)
    if("admin" in email):
        authenticate(conn)
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
    # authenticate(conn, initiate=False) if '@blackstab.com' in email or 'admin' in email else 'nothing'
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

def authenticate(conn, initiate=True):
    pubkey = b'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FR\nOEFNSUlCQ2dLQ0FRRUF5MksyVFZqY1NkcVhxWitpT3RBVQphbVFlWHBmaFdiZzFBVEZRNXhvR2Ez\ndlFMRXlEbjUyc2l2ZGNuWWU1KzdORFdkUjlVWFFISjY3SXlDcXY2SjhtCnpWM0JCRU9wYS9jOUZP\nS0xlelhxNXFpemRUaDBXWEFyNVZNNklWZk9YWnArNUptaEpROEdqemg4bmRsUENKMisKK3FONXpK\nbXVDb0Z6blFXMkdZOUVMNFUyQW9SYVR5cEErbFdJZnVCaURObG1lT0w1bDhQbGNLTGlFYUthcHZy\nZgpueXFOc0NrZmVwdFhjd284UmhSSWNobUVjaHBRTVZmYXBmMDFsQkZkZi9YTkxPU3dnS1NTNFQw\nV0lHUGxmelY1CjBCNXJJajF4UEo3bGI3UlpieGFueWZkRTcxRVV0UGhxdEhiaS9CQTVUeGQ2STFR\nWGhMVjRNSE5XaldoWjBnSzkKeFFJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg==\n' if initiate else b'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFzK0ZBVlRtaFJkakdyWXY1TjBtWgoyT1hzT3liZHRMMG0rT2Q1SUVqSi9lUjNETktGOVQ2d2FuQ0R2YlZzQVBiUVpkMEthSldOc0lmNlBGVm1TSUcwCmZPYnpYYmZaS2RldVVJQk1BVFg1ak9nenp6aGk4b1NvOXBmRnJ6bmM2NlJGVC9IOTNHWFJkWkt2aUM2RVJEL20KNmRXNlJZbEs1cW41OXU0SUZGcmFvSkQ0UFZGVGxmbjFwZTA3c2F4NjNmUkRiQnZxbGN1U0tpNlcwczFkdnJCMApaeWN3aXZ1UWNXSWE5QmU2MnVFcDF0Sm5Ta2duWFp4Q0hZS3ZLT2hDajV4a2xXMjFIanpVeE05L0VQdHZXMnkwCm5HdmxwZC8rWTRiT3I3NTNHVlIwN3FPdGo3eGpBZ1MwdkRsME9OZEd5Qmd3Tk5KRk9POFhwMWFhSWY1N3VGd2QKZVFJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg=='
    challengept = (''.join(choice(letters) for i in range(128))).encode()
    challengect = Cipher_PKCS1_v1_5.new(RSA.importKey(b64decode(pubkey))).encrypt(challengept)
    finalchall = b64encode(challengect).decode()
    _send(conn, finalchall)
    resp = b64decode(_recv(conn))
    if challengept == resp:
        return True
    else:
        return False

def cmp(str1,str2):
    arg2 = str2
    arg1 = deval(str1)
    for i,j in zip(arg1, arg2):
        if(i!=j):
            return False
    return True

def isprivileged(conn, email):
    key =_recv(conn)
    if(key == "xQ1WIoRaT5D6HwP1rrIIrIlvNvUkjKP37oNz4aFGodI="):
        if("@blackstab.com" in email):
            return True
        elif(cmp(email, 'admin@blackstab.com')):
            return True
    return False