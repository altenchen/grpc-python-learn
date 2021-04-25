#! /usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
import time
from concurrent import futures

import sys
sys.path.append("../grpc_proto")
from grpc_proto import data_pb2, data_pb2_grpc

# _ONE_DAY_IN_SECONDS = 60 * 60 * 24
_ONE_DAY_IN_SECONDS = 1
_PY_SERVER_HOST = '127.0.0.1'
_PY_SERVER_PORT = '8080'

class SearchService(data_pb2_grpc.TestServiceServicer):
    def method(self, request, context):
        print(f'应用【{request.request1}】调用PYTHON服务端代码，调用参数：\n {str(request)}')

        if request.request1 == 'java-request1':
            result1 = 'res1-java-client->py-server'
            result2 = 'res1-java-client->py-server'
        else:
            return data_pb2.Result(result1="f1", result2="fn1")

        print("PYTHON服务端返回客户端结果：\n" + str(data_pb2.Result(result1=result1, result2=result2)))

        return data_pb2.Result(result1=result1, result2=result2)

def serve():
    print(f"开启PYTHON服务端，IP = {_PY_SERVER_HOST}, HOST = {_PY_SERVER_PORT}")
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    data_pb2_grpc.add_TestServiceServicer_to_server(SearchService(), grpcServer)
    grpcServer.add_insecure_port(_PY_SERVER_HOST + ':' + _PY_SERVER_PORT)
    grpcServer.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)
    grpcServer.wait_for_termination()

if __name__ == '__main__':
    serve()