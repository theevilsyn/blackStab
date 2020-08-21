import socket

def menu(io):
    print("""
    1. CreateVM
    2. ModifyVM
    3. DeleteVM
    4. VMStatus
    5. ListMyVMs
    6. View Subscription
    7. Delete Account
    """)

    try:
        pass
    except KeyboardInterrupt:
        print("Exiting on your request")
        io.send(b"1337")
        io.close()


def register(io):
    data='1'.ljust(4)
    username = input("Username: ")
    data+=str(len(username)).ljust(4)
    data+=username

    email = input("Email: ")
    data+=str(len(email)).ljust(4)
    data+=email

    password = input("Password: ")
    data+=str(len(password)).ljust(4)
    data+=password

    io.send(data.encode())
    response = io.recv(4)

    if(int(response == 1)):
        print("Email already Taken :(")
        # io.send(b"1337")
        # io.close()
        exit()
    elif(int(response) == 2):
        print("Password not greater than 12 :/")
        exit()
    else:
        print("Registration Successful")
        reg_login(io)


def login(io):
    data='2'.ljust(4)
    email = input("Email: ")
    data+=str(len(email)).ljust(4)
    data+=email

    password = input("Password: ")
    data+=str(len(password)).ljust(4)
    data+=password
    io.send(data.encode())
    response = int(io.recv(4))
    if(response == 0):
        print("Successfully logged in")
        menu(io)
    elif(response == 1):
        print("User not found")
        exit()
    else:
        print("Password Incorrect")
        exit()


def reg_login(io):
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
    else:
        exit()


io = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
io.connect(('192.168.123.219', 9999))

try:
    reg_login(io)        
except KeyboardInterrupt:
    print("Exiting upon your request!!")
    io.send(b'1337')
    io.close()