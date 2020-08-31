from time import sleep
from random import SystemRandom 
import threading
import string
from pwn import process

class Tester:

    def __init__(self, interval=0):

        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = False
        thread.start()

    def gen_rand_str(self, length):
        return ''.join(SystemRandom()
                       .choice(string.ascii_letters + string.digits)
                 for _ in range(length))

    def register(self, email, password):
        io = process("./cloud-client -ip=192.168.122.55 -port=9999 -rapid-connect -register", shell=True)
        io.sendlineafter(b"Email: ", email.encode())
        io.sendlineafter(b"name: ", self.gen_rand_str(10).encode())
        io.sendlineafter(b"word: ", password.encode())
        io.close()

    def login(self, email, password):
        io = process("./cloud-client -ip=192.168.122.55 -port=9999 -rapid-connect -login", shell=True)
        io.sendlineafter(b"Email: ", email.encode())
        io.sendlineafter(b"word: ", password.encode())
        io.close()

    def run(self):
        while True:
            try:
                email = self.gen_rand_str(7)+"@"+self.gen_rand_str(6)+".com"
                password = self.gen_rand_str(13)
                self.register(email=email, password=password)
                self.login(email=email, password=password)
                sleep(self.interval)
            except KeyboardInterrupt:
                exit(-1)


if __name__ == "__main__":
    registrar = Tester()
    # sleep(3)
    print('Checkpoint')
    print('Bye')

