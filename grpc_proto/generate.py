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
