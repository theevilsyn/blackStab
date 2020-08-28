#!/usr/bin/env python3
from concurrent import futures
from base64 import b64encode as b64
from base64 import b64decode
import logging
import random
import string

import grpc

import checker_pb2 as checker
import checker_pb2_grpc as checker_grpc

checker_port = 50051

# Invoke plant flag
def test_plant_flag(ip, port):
    # open a gRPC channel
    channel = grpc.insecure_channel("localhost:50051")#'http://:{}'.format(checker_port))

    # create a stub (client)
    stub = checker_grpc.CheckerStub(channel)

    flag_request = checker.FlagRequest(ip=ip, port=port)
    flag_response = stub.PlantFlag(flag_request)
    return flag_response

ip = "13.67.47.147"
port = 9999
output = test_plant_flag(ip, port)
