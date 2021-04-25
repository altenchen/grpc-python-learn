#! /usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
import sys
sys.path.append("../grpc_proto")
from grpc_proto import data_pb2, data_pb2_grpc

_PY_CLIENT_HOST = '127.0.0.1'
_PY_CLIENT_PORT = '8000'

def guide_get_one_feature(stub, requestInfo):
    feature = stub.method(requestInfo)
    if feature is None:
        print("未找到匹配结果")
        return

    if feature.result1:
        print(f"PYTHON客户端请求服务端成功...")
        return feature

def guide_get_feature(stub):
    print("PYTHON客户端向服务端发起请求...")
    return guide_get_one_feature(stub, data_pb2.Request(
            request1 = 'py-request1',
            request2 = 'py-request2'
        )
    )



def run():
    print(f"开启PYTHON客户端，IP = {_PY_CLIENT_HOST}, HOST = {_PY_CLIENT_PORT}")
    conn = grpc.insecure_channel(_PY_CLIENT_HOST + ':' + _PY_CLIENT_PORT)
    stub = data_pb2_grpc.TestServiceStub(channel=conn)
    response = guide_get_feature(stub)
    print("PYTHON客户端调用服务端返回结果: \n" + str(response))

if __name__ == '__main__':
    run()