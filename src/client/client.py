import socket
io = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
io.connect(('192.168.123.219', 9999))

print("""
1. Register
2. Login
""")

if(int(raw_input()) == 1):
    data='1'.ljust(4)
    username = raw_input("Username: ")
    data+=str(len(username)).ljust(4)
    data+=username

    email = raw_input("Email: ")
    data+=str(len(email)).ljust(4)
    data+=email

    password = raw_input("Password: ")
    data+=str(len(password)).ljust(4)
    data+=password
    io.send(data)

    from IPython import embed; embed()