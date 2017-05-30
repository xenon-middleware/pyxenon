#!/bin/bash

python -m grpc_tools.protoc -Iproto --python_out=xenon/grpc --grpc_python_out=xenon/grpc proto/xenon.proto
