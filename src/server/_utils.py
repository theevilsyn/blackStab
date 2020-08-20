from binascii import hexlify

def recvbytes(conn, remains):
    buf = b""
    while remains:
        data = conn.recv(remains)
        if not data:
            break
        buf += data
        remains -= len(data)
    return buf

def register(conn, account):
    username_len = int(recvbytes(conn, 4))
    username = recvbytes(conn,  username_len)

    email_len = int(recvbytes(conn, 4))
    email = recvbytes(conn, email_len)

    password_len = int(recvbytes(conn, 4))
    password = recvbytes(conn, password_len)

    _register = account.register(email=email, username=username, password=password)
    conn.send(str(_register).ljust(4))

def login(conn, account):
    email_len = int(recvbytes(conn, 4))
    email = recvbytes(conn, email_len)

    password_len = int(recvbytes(conn, 4))
    password = recvbytes(conn, password_len)

    _login = account.check_login(email=email, password=password)
    conn.send(str(_login).ljust(4))
    return email, password

def createvm(conn, vm, account, email, password):
    vmname_len = int(recvbytes(conn, 4))
    vmname = recvbytes(conn, vmname_len)

    tag_len = int(recvbytes(conn, 4))
    tag = recvbytes(conn, tag_len)

    balance = account.showCredits
    response = vm.create(funds=balance, account=hexlify(email+password), name=vmname, tag=tag)
    conn.send(str(response).ljust(4))
