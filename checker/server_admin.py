#!/usr/bin/env python3
from concurrent import futures
from base64 import b64encode as b64
from base64 import b64decode
import logging
import random
import string

import grpc
from pwn import *

import checker_pb2 as checker
import checker_pb2_grpc as checker_grpc

import gc

PORT = 9999
COLOR_RESET = b"\x1b[0m"
PROMPT = b'Your Choice >> ' + COLOR_RESET


context.log_level = "debug"
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
    username = gen_rand_str(random.randint(7, 13))
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
    
def admin_register(io):
    username = gen_rand_str(random.randint(7, 13))
    email = username + "@blackstab.com"
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
    io.recvuntil(PROMPT)
    io.sendline(b'1')
    io.recvuntil("Enter VM Name: ")
    io.sendline(vm_name)
    io.recvuntil("Enter VM Tag: ")
    io.sendline(vm_tag)

    io.recvuntil(PROMPT)
    io.sendline(str(random.choice(range(5))+1))

    io.recvuntil("Input >> ")
    secretkey = b64(gen_rand_str(64).encode()).decode()
    io.sendline( secretkey )
    io.recvuntil('what shall I name this key? ')
    keyname = gen_rand_str(7)
    io.sendline( keyname )
    io.recvuntil("Choice >> ")
    io.sendline("y")

    output = io.recvuntil("//////////")
    if b"Successfully" in output:
        return (True, output, secretkey, keyname)
    else:
        return (False, output, secretkey, keyname)


def get_status_of_vm(io, vm_name):
    io.recvuntil(PROMPT)
    io.sendline(b'4')
    io.recvuntil("Enter VM name: ")
    io.sendline(vm_name)
    io.recvuntil("VM Tag: ", timeout=3)

    flag = io.recvuntil(" ").rstrip()
    flag = b64decode(flag)
    return flag


def list_public_key(io, vm_name, secretkey, keyname):
    io.recvuntil(PROMPT)
    io.sendline(b'5')
    io.recvuntil("Enter VM name: ")
    io.sendline(vm_name)
    io.recvuntil('Key name: ')
    io.sendline(keyname)

    try:
        io.recvuntil('Response:\n\n', timeout = 3)
        key = io.recvline().rstrip()
        try:
            key = key.decode()
        except:
            pass
        
        if key == secretkey:
            return (True, "Key verified")
        else:
            return (False, "Wrong key: {}".format(key))
    except:
        return (False, "Unable to get public key")

def set_flag(ip,port,flag):
    context.log_level="error"
    try:
        client = process("./cloud-client -ip={} -port={} -rapid-connect -register".format(ip, port), shell=True, close_fds=True)
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.DOWN
        reason = str(e)
        status = checker.ServiceState(status = state, reason = reason)
        return (status, "")
    
    # Register a new user
    try:
        status, (email, password), reason = register(client)
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.DOWN
        reason = "Service Unreachable, unable to register"
        status = checker.ServiceState(status = state, reason = reason)
        return (status, "")
    
    try:
        client = process("./cloud-client -ip={} -port={} -rapid-connect -login".format(ip, port), shell=True, close_fds=True)
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.DOWN
        reason = str(e)
        status = checker.ServiceState(status = state, reason = reason)
        return (status, "")
    
    # login and plant flag
    try:
        status, reason = login(client, email, password)
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.MUMBLE
        reason = "Unable to Login: " + str(e)
        status = checker.ServiceState(status = state, reason = reason)
        return (status, "")

    token = gen_rand_str(16)
    try: # to plant the flag
        status, reason, secretkey, keyname = create_vm(client, token, flag)
        
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.MUMBLE
        reason = "Unable to create VM: " + str(e)
        status = checker.ServiceState(status = state, reason = reason)
        return (status,"")
    
    flag_token = ":".join([email, password, token, secretkey, keyname])
    status = checker.ServiceState(status = checker.ServiceStatus.UP , reason = "")
    client.close()
    return (status, flag_token)

def get_flag(ip,port,flag,flag_token):
    context.log_level="error"
    try:
        client = process("./cloud-client -ip={} -port={} -rapid-connect -login".format(ip, port), shell=True,close_fds=True)
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.DOWN
        reason = str(e)
        return checker.ServiceState(status = state, reason = reason)
    
    try:
        email, password, token, secretkey, keyname = flag_token.split(":")
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.CORRUPT
        reason = "Ill formated token string provided: " + str(e)
        return checker.ServiceState(status = state, reason = reason)
    
    try:
        login_status, reason = login(client, email, password)
        assert login_status == True, "Login failed" + reason
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.MUMBLE
        reason = "Unable to Login: " + str(e)
        return  checker.ServiceState(status = state, reason = reason)
    try:
        recv_flag = get_status_of_vm(client, token)
        client.close()
        if recv_flag.decode() == flag:
            return checker.ServiceState(status = checker.ServiceStatus.UP,
                                            reason = "")
        else:
            return checker.ServiceState(status = checker.ServiceStatus.CORRUPT,
                                            reason = "Unable to retrive flag: flag does not match")
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.MUMBLE
        reason = "Unable to retrive the flag" + str(e)
        return checker.ServiceState(status = state, reason = reason)

def check_functionality(ip, port, flag_token):
    context.log_level="error"

    try:
        client = process("./cloud-client -ip={} -port={} -rapid-connect -login".format(ip, port), shell=True, close_fds=True)
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.DOWN
        reason = str(e)
        return checker.ServiceState(status = state, reason = reason)
    
    email, password, token, secretkey, keyname = flag_token.split(":")

    status, reason = login(client, email, password)
    

    try:

        status, reason = list_public_key(client, token, secretkey, keyname)
        client.close()
        if status == True:
            return checker.ServiceState(status = checker.ServiceStatus.UP,
                                            reason = "")
        else:
            return checker.ServiceState(status = checker.ServiceStatus.MUMBLE,
                                            reason = reason)
    except Exception as e:
        try:
            client.close()
        except:
            pass
        client.close()
        state = checker.ServiceStatus.MUMBLE
        reason = str(e)
        return checker.ServiceState(status = state, reason = reason)
    

def check_admin_functionality(ip, port, flag_token):
    context.log_level="error"
    
    try:
        client = process("./admin-client -ip={} -port={} -rapid-connect -register".format(ip, port), shell=True, close_fds=True)
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.DOWN
        reason = str(e)
        status = checker.ServiceState(status = state, reason = reason)
        return (status, "")
    
    # Register a new user
    try:
        status, (email, password), reason = admin_register(client)
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.DOWN
        reason = "Service Unreachable, unable to register"
        status = checker.ServiceState(status = state, reason = reason)
        return (status, "")
    
    try:
        client = process("./admin-client -ip={} -port={} -rapid-connect -login".format(ip, port), shell=True, close_fds=True)
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.DOWN
        reason = str(e)
        status = checker.ServiceState(status = state, reason = reason)
        return (status, "")
    
    # login and plant flag
    try:
        status, reason = login(client, email, password)
    except Exception as e:
        try:
            client.close()
        except:
            pass
        state = checker.ServiceStatus.MUMBLE
        reason = "Unable to Login: " + str(e)
        status = checker.ServiceState(status = state, reason = reason)
        return (status, "")

    # work from here
    try:

        status, reason = list_public_key(client, token, secretkey, keyname)
        client.close()
        if status == True:
            return checker.ServiceState(status = checker.ServiceStatus.UP,
                                            reason = "")
        else:
            return checker.ServiceState(status = checker.ServiceStatus.MUMBLE,
                                            reason = reason)
    except Exception as e:
        try:
            client.close()
        except:
            pass
        client.close()
        state = checker.ServiceStatus.MUMBLE
        reason = str(e)
        return checker.ServiceState(status = state, reason = reason)

class Checker(checker_grpc.CheckerServicer):
    def PlantFlag(self,request,context):
        try:

            flag = "bi0s{" + gen_rand_str(26) + "}"
            status, token = set_flag(request.ip,request.port,flag)
            print("Plant Flag {} -> {} : {} "
                    .format(request.ip,request.port,status))
            return checker.FlagResponse(state = status,
                                        flag=flag,
                                        token=token)
        except Exception as e:
            reason = "Unable to Plant Flag: " + str(e)
            state = checker.ServiceState(checker.ServiceStatus.CORRUPT, reason)
            return checker.FlagResponse(state = state,
                                        flag = "",
                                        token = "")


    def CheckService(self,request,context):
        try:
            service_state = get_flag(request.ip,request.port,
                            request.flag,request.token)
            print("Check Service {} -> {} : {}"
                    .format(request.ip,request.port,service_state.status))
            if service_state.status == checker.ServiceStatus.UP:
                # if we can retrieve the flag, check if they have made an illegal patch
                function_state = check_functionality(request.ip, request.port, request.token)
                #return function_state
                service_state = function_state
            if service_state.status == checker.ServiceStatus.UP:
                # If functionality is up, check if admin feature is working
                admin_state = check_admin_functionality(request.ip, request.port, request.token)
                service_state = admin_state
            return service_state
        except Exception as e:
            state = checker.ServiceStatus.CORRUPT
            reason = "Unable to Check Service: " + str(e)
            return checker.ServiceState(status = state, reason = reason)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=(('gprc.so_reuseport', 1),))
    checker_grpc.add_CheckerServicer_to_server(Checker(), server)
    port = 50051
    print("Launching Server on port :: {}".format(port))
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    #context.debug = False
    serve()

