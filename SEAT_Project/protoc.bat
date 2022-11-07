python -m grpc_tools.protoc -I. --python_out=.\accountingService\src --grpc_python_out=.\accountingService\src .\proto\grpc.proto
python -m grpc_tools.protoc -I. --python_out=.\apiGateway\src --grpc_python_out=.\apiGateway\src .\proto\grpc.proto
python -m grpc_tools.protoc -I. --python_out=.\reservationService\src --grpc_python_out=.\reservationService\src .\proto\grpc.proto
python -m grpc_tools.protoc -I. --python_out=.\quoteService\src --grpc_python_out=.\quoteService\src .\proto\grpc.proto
python -m grpc_tools.protoc -I. --python_out=.\reviewService\src --grpc_python_out=.\reviewService\src .\proto\grpc.proto
python -m grpc_tools.protoc -I. --python_out=.\paymentService\src --grpc_python_out=.\paymentService\src .\proto\grpc.proto
python -m grpc_tools.protoc -I. --python_out=.\serviceRegistry\src --grpc_python_out=.\serviceRegistry\src .\proto\grpc.proto