# 一，前言

gRPC 是一款高性能、开源的 RPC 框架，产自 Google，基于 ProtoBuf 序列化协议进行开发，支持多种语言（Golang、Python、Java等），本篇只介绍 Python 的 gRPC 使用。因为 gRPC 对 HTTP/2 协议的支持使其在 Android、IOS 等客户端后端服务的开发领域具有良好的前景。gRPC 提供了一种简单的方法来定义服务，同时客户端可以充分利用 HTTP2 stream 的特性，从而有助于节省带宽、降低 TCP 的连接次数、节省CPU的使用等。

# 二，安装

## 2.1，通过pip安装

1，gRPC 的安装：

```plain
$ pip install grpcio
```
2，安装 ProtoBuf 相关的 python 依赖库：
```plain
$ pip install protobuf
```
3，安装 python grpc 的 protobuf 编译工具：
```plain
$ pip install grpcio-tools
```
## 2.2，通过pycharm和conda安装![图片](https://uploader.shimo.im/f/qevUIbEdxiWvku7z.png!thumbnail?fileGuid=PvQ9xWT9HYCx6WPY)

# 三，实践

下面我们使用 gRPC 定义一个接口，该接口实现对传入数据进行判断，根据来自不同端（java端或者python端）的请求，返回对应端的数据。

1，创建项目 python demo 工程：

* client目录下的 main.py 实现了客户端用于发送数据并打印接收到 server 端处理后的数据；
* server 目录下的 main.py 实现了 server 端用于接收客户端发送的数据，并对数据来自java或者python端的数据进行判断，返回对应端数据给客户端；
* proto 包用于编写 proto 文件并生成 data 接口

整体工程结构目录如下；

![图片](https://uploader.shimo.im/f/gUhxvpNngvFD21CE.png!thumbnail?fileGuid=PvQ9xWT9HYCx6WPY)

2，定义 gRPC 接口：

```plain
syntax = "proto3";
package example;
service TestService
{
  rpc method(Request) returns (Result){}
}
message Request
{
  string request1 = 1;
  string request2 = 2;
}
message Result
{
  string result1 = 1;
  string result2 = 2;
}
```
3，编译 protobuf：
在 proto 目录下编写脚本generate.py，并执行：

```python
proto_files = ["./data.proto"]
import subprocess
for file in proto_files:
    status = "failed"
    try:
        args = "--proto_path=. --python_out=. --grpc_python_out=. {0}".format(file)
        result = subprocess.call("python -m grpc_tools.protoc " + args, shell=True)
        if result == 0:
            status = "success"
        else:
            status = "failed"
        print("grpc_proto generation result for '{0}': generation {1}".format(file, status))
    except:
        print("grpc_proto generation result for '{0}': generation {1}".format(file, status))
```

4，实现 server 端：

```python
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
```
5，实现 client 端：
```python
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
```
6，执行验证结果：
* 先启动 server，之后再执行 client；
* client 侧控制台如果打印的结果为：“received: HELLO,WORLD!” ，证明 gRPC 接口定义成功

