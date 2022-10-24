python3 -m grpc_tools.protoc -I. --python_out=.\accountingService --grpc_python_out=.\accountingService .\proto\grpc.proto
python3 -m grpc_tools.protoc -I. --python_out=.\apiGateway --grpc_python_out=.\apiGateway .\proto\grpc.proto
python3 -m grpc_tools.protoc -I. --python_out=.\reservationService --grpc_python_out=.\reservationService .\proto\grpc.proto
python3 -m grpc_tools.protoc -I. --python_out=.\quoteService --grpc_python_out=.\quoteService .\proto\grpc.proto
python3 -m grpc_tools.protoc -I. --python_out=.\reviewService --grpc_python_out=.\reviewService .\proto\grpc.proto
python3 -m grpc_tools.protoc -I. --python_out=.\paymentService --grpc_python_out=.\paymentService .\proto\grpc.proto