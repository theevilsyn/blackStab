import socket
io = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
io.connect(('192.168.123.219', 9999))

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

print("""
1. Register
2. Login
""")
loggedin=False
try:
    choice = int(input())
    if(choice == 1):
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
        else:
            print("Registration Successful")
    elif(choice == 2):
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
        else:
            print("Password Incorrect")

except KeyboardInterrupt:
    print("Exiting upon your request!!")
    io.send(b'1337')
    io.close()