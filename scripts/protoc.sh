#!/bin/bash

silent () {
    return $* > /dev/null 2> /dev/null
}

if (silent which xenon-grpc)
then
    echo "Xenon GRPC could not be located."
    exit
fi

echo "Obtaining \`xenon.proto\` file."
xenon-grpc --proto > xenon/proto/xenon.proto

echo "Generating Python code."
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. xenon/proto/xenon.proto
