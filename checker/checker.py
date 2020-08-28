#!/usr/bin/env python3
from concurrent import futures
from base64 import b64encode as b64
import logging
import random
import string

import grpc
from pwn import *

import checker_pb2 as checker
import checker_pb2_grpc as checker_grpc

PORT = 9999
COLOR_RESET = b"\x1b[0m"
PROMPT = b'Your Choice >> ' + COLOR_RESET

def gen_rand_str(length):
    return ''.join(random.SystemRandom()
                   .choice(string.ascii_letters + string.digits)
             for _ in range(length))

def recvuntil(io,string):
    res = io.recvuntil(string,timeout=3)
    if res == b'' :
        raise Exception("Timeout while reciving : \"{}\""
                        .format(string))
    return res


def register(io):
    username = gen_rand_str(random.randint(7, 13)
    email = username + "@gmail.com"
    password = gen_rand_str(random.randint(12, 15))
    io.recvuntil("Enter Email: ")
    io.sendline(email)
    io.recvuntil("Enter Username: ")
    io.sendline(username)
    io.recvuntil("Enter Password: ")
    io.sendline(password)

    output = io.recvline()
    if b'Registration Successful' in output:
        return (True, (email, password), output)
    else:
        return (False, (email, password), output)
    
def login(io, email, password):
    io.recvuntil("Enter Email: ")
    io.sendline(email)
    io.recvuntil("Enter Password: ")
    io.sendline(password)

    output = io.recvline()
    if b"Successfully Logged In" in output:
        return (True, output)
    else:
        return (False, output)

def create_vm(io, vm_name, vm_tag):
    io.recvuntil(PROMPT})
    io.sendline(b'1')
    io.recvuntil("Enter VM Name: ")
    io.sendline(vm_name)
    io.recvuntil("Enter VM Tag: ")
    io.sendline(vm_tag)

    io.recvuntil(PROMPT})
    io.sendline(random.choice(range(5))+1)

    io.recvuntil("Input >> ")
    io.sendline(b64(gen_rand_str(64).encode()))
    io.sendline('what shall I name this key? ')
    io.sendline( gen_rand_str(7))
    io.recvuntil("Choice >> ")
    io.sendline("y")

    output = io.recvline()
    if b"Successfully" in output:
        return (True, output)
    else:
        return (False, output)

    



def set_flag(ip,port,flag):
    context.log_level="error"
    try:
        client = process("./cloud-client -ip={} -port={} -rapid-connect -register".format(ip, port), shell=True)
    except Exception as e:
        state = checker.ServiceState.DOWN
        reason = str(e)
        status = checker.ServiceStatus(state = state, reason = reason)
        return (status, "")

    # Register a new user
    status, (email, password), reason = register(client)

    try:
        client = process("./cloud-client -ip={} -port={} -rapid-connect -login".format(ip, port), shell=True)
    except Exception as e:
        state = checker.ServiceState.DOWN
        reason = str(e)
        status = checker.ServiceStatus(state = state, reason = reason)
        return (status, "")
    
    # login and plant flag
    status, reason = login(client, email, password)
    
    token = gen_rand_str(16)
    try: # to plant the flag
        status, reason = create_vm(client, token, flag)
        
    except Exception as e:
        client.close()
        state = checker.ServiceState.MUMBLE
        reason = str(e)
        status = checker.ServiceStatus(state = state, reason = reason)
        return (status,"")
    
    status = checker.ServiceStatus(state = checker.ServiceState.UP , reason = reason)
    client.close()
    return (status, token)

def get_flag(ip,port,flag,token):
        context.log_level="error"
        try:
            io = connect(ip,port,timeout=1)
        except Exception as e:
            state = checker.ServiceState.DOWN
            reason = str(e)
            return checker.ServiceStatus(state = state, reason = reason)

        try:

            io.send(flag)
            recv_flag = io.recv(len(flag))
            io.close()
            if recv_flag == flag:
                return checker.ServiceStatus(state = checker.ServiceState.UP,
                                             reason = "")
            else:
                return checker.ServiceStatus(state = checker.ServiceState.CORRUPT,
                                             reason = "Unable to retrive flag")
        except Exception as e:
            io.close()
            state = checker.ServiceState.MUMBLE
            reason = str(e)
            return checker.ServiceStatus(state = state, reason = reason)


class Checker(checker_grpc.CheckerServicer):
    def PlantFlag(self,request,context):
        flag = "bi0s{" + gen_rand_str(26) + "}"
        status, token = set_flag(request.ip,request.port,flag)
        print("Plant Flag {} -> {} : {} "
                .format(request.ip,request.port,status))
        return checker.FlagResponse(status = status,
                                    flag=flag,
                                    token=token)
    
    def CheckService(self,request,context):
        service_state = get_flag(request.ip,request.port,
                        request.flag,request.token)
        print("Check Service {} -> {} : {}"
                .format(request.ip,request.port,service_state.state))
        return service_state

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    checker_grpc.add_CheckerServicer_to_server(Checker(), server)
    port = 50051
    print("Launching Server on port :: {}".format(port))
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    context.debug = False
    serve()

