#!/bin/sh

python3 -m grpc_tools.protoc -I. --python_out=./accountingService --grpc_python_out=./accountingService ./proto/grpc.proto
python3 -m grpc_tools.protoc -I. --python_out=./apiGateway --grpc_python_out=./apiGateway ./proto/grpc.proto
python3 -m grpc_tools.protoc -I. --python_out=./reservationService --grpc_python_out=./reservationService ./proto/grpc.proto

gnome-terminal -- sh -c 'python3 ./accountingService/main.py'
gnome-terminal -- sh -c 'python3 ./apiGateway/main.py'
gnome-terminal -- sh -c 'python3 ./reservationService/main.py'
