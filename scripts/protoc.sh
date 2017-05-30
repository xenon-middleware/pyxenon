#!/bin/bash

python -m grpc_tools.protoc -I. --python_out=xenon --grpc_python_out=xenon proto/xenon.proto
