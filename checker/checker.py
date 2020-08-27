#!/usr/bin/env python3
from concurrent import futures
import logging
import random
import string

import grpc
from pwn import *

import checker_pb2 as checker
import checker_pb2_grpc as checker_grpc

PORT = 9999

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

def set_flag(ip,port,flag):
        context.log_level="error"
        try:
            io = connect(ip,port,timeout=1)
        except Exception as e:
            state = checker.ServiceState.DOWN
            reason = str(e)
            status = checker.ServiceStatus(state = state, reason = reason)
            return (status, "")

        try:
            io.send(flag)
            token = io.recv(len(flag))
            
        except Exception as e:
            io.close()
            state = checker.ServiceState.MUMBLE
            reason = str(e)
            status = checker.ServiceStatus(state = state, reason = reason)
            return (status,"")
        
        status = checker.ServiceStatus(state = checker.ServiceState.UP , reason = "")
        io.close()
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

