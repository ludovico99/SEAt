# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/grpc.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10proto/grpc.proto\x12\x05proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x1b\n\x0b\x63ityRequest\x12\x0c\n\x04\x63ity\x18\x01 \x01(\t\"\x1a\n\x06matrix\x12\x10\n\x08numInRow\x18\x01 \x03(\x05\"-\n\x10usernameResponse\x12\x19\n\x11usernameBeachClub\x18\x01 \x03(\t\"\x07\n\x05\x65mpty\"0\n\rdeleteRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05\x61\x64min\x18\x02 \x01(\x08\"y\n\rupdateRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x13\n\x0bnewPassword\x18\x03 \x01(\t\x12\x10\n\x08newEmail\x18\x04 \x01(\t\x12\r\n\x05\x61\x64min\x18\x05 \x01(\x08\x12 \n\x03opt\x18\x06 \x01(\x0b\x32\x13.proto.adminOptions\"y\n\x13registrationRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\r\n\x05\x61\x64min\x18\x04 \x01(\x08\x12 \n\x03opt\x18\x05 \x01(\x0b\x32\x13.proto.adminOptions\"2\n\x0cloginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\xac\x01\n\x0c\x61\x64minOptions\x12\x15\n\rbeachClubName\x18\x01 \x01(\t\x12\x10\n\x08location\x18\x02 \x01(\t\x12\x0e\n\x06\x63\x61rdId\x18\x03 \x01(\t\x12\x0b\n\x03\x63vc\x18\x04 \x01(\t\x12\x14\n\x0cristorazione\x18\x05 \x01(\x08\x12\x0b\n\x03\x62\x61r\x18\x06 \x01(\x08\x12\r\n\x05\x63\x61mpi\x18\x07 \x01(\x08\x12\x12\n\nanimazione\x18\x08 \x01(\x08\x12\x10\n\x08palestra\x18\t \x01(\x08\"9\n\x08response\x12\x17\n\x0foperationResult\x18\x01 \x01(\x08\x12\x14\n\x0c\x65rrorMessage\x18\x02 \x01(\t\"*\n\x07session\x12\x1f\n\x04\x64ict\x18\x01 \x03(\x0b\x32\x11.proto.dictionary\"(\n\ndictionary\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"U\n\x14reservedSeatsRequest\x12\x13\n\x0b\x62\x65\x61\x63hClubId\x18\x01 \x01(\t\x12(\n\x04\x64\x61te\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"@\n\x15reservedSeatsResponse\x12\'\n\x0breservation\x18\x01 \x03(\x0b\x32\x12.proto.reservation\"3\n\x0breservation\x12\x14\n\x0combrelloneId\x18\x01 \x01(\t\x12\x0e\n\x06userId\x18\x02 \x01(\t\"\x90\x01\n\x18manualReservationRequest\x12\x13\n\x0b\x62\x65\x61\x63hClubId\x18\x01 \x01(\t\x12\x10\n\x08\x63ustomer\x18\x02 \x01(\t\x12\x14\n\x0combrelloneId\x18\x03 \x03(\t\x12\x12\n\nnumLettini\x18\x04 \x01(\x05\x12\x11\n\tnumSdraio\x18\x05 \x01(\x05\x12\x10\n\x08numChair\x18\x06 \x01(\x05\"4\n\x10proposalResponse\x12 \n\x07offerta\x18\x01 \x03(\x0b\x32\x0f.proto.proposal\"p\n\x08proposal\x12\x0f\n\x07lido_id\x18\x01 \x01(\t\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\x12\x10\n\x08\x64istance\x18\x03 \x01(\x02\x12\r\n\x05price\x18\x04 \x01(\x02\x12\x15\n\raverageReview\x18\x05 \x01(\x02\x12\r\n\x05index\x18\x06 \x01(\x05\"\xa6\x01\n\x14\x63onfigurationRequest\x12\x0f\n\x07numRows\x18\x01 \x01(\x05\x12\"\n\x05\x61rray\x18\x02 \x01(\x0b\x32\x13.proto.numSeatByRow\x12\x12\n\nnumLettini\x18\x03 \x01(\x05\x12\x11\n\tnumSdraio\x18\x04 \x01(\x05\x12\x10\n\x08numChair\x18\x05 \x01(\x05\x12 \n\x08sessione\x18\x06 \x01(\x0b\x32\x0e.proto.session\"$\n\x0cnumSeatByRow\x12\x14\n\x0cnumSeatInRow\x18\x01 \x03(\x05\"\x94\x02\n\x0fproposalRequest\x12\x10\n\x08location\x18\x01 \x01(\t\x12\x0e\n\x06numRow\x18\x02 \x01(\x05\x12\x18\n\x10numBeachUmbrella\x18\x03 \x01(\x05\x12\x12\n\nnumLettini\x18\x04 \x01(\x05\x12\x11\n\tnumSdraio\x18\x05 \x01(\x05\x12\x10\n\x08numChair\x18\x06 \x01(\x05\x12,\n\x08\x66romDate\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12*\n\x06toDate\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08maxPrice\x18\t \x01(\x05\x12 \n\x08sessione\x18\n \x01(\x0b\x32\x0e.proto.session\"\xe1\x02\n\x12reservationRequest\x12\x13\n\x0b\x62\x65\x61\x63hClubId\x18\x01 \x01(\t\x12\x0e\n\x06numRow\x18\x02 \x01(\x05\x12\x13\n\x0bnumUmbrella\x18\x03 \x01(\x05\x12\x12\n\nnumLettini\x18\x04 \x01(\x05\x12\x11\n\tnumSdraio\x18\x05 \x01(\x05\x12\x10\n\x08numChair\x18\x06 \x01(\x05\x12,\n\x08\x66romDate\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12*\n\x06toDate\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05price\x18\t \x01(\x05\x12\x11\n\tpayOnline\x18\n \x01(\x08\x12 \n\x08sessione\x18\x0b \x01(\x0b\x32\x0e.proto.session\x12\x10\n\x08\x64istance\x18\x0c \x01(\x02\x12\x18\n\x10\x62udgetDifference\x18\r \x01(\x02\x12\x0e\n\x06idCard\x18\x0e \x01(\x05\"\xdf\x01\n\x0cpriceRequest\x12\x17\n\x0fpriceOmbrellone\x18\x01 \x01(\x05\x12\x13\n\x0bpriceSdraio\x18\x02 \x01(\x05\x12\x14\n\x0cpriceLettino\x18\x03 \x01(\x05\x12\x12\n\npriceSedia\x18\x04 \x01(\x05\x12\x15\n\rincrPrimeFile\x18\x05 \x01(\x05\x12\x18\n\x10incrAltaStagione\x18\x06 \x01(\x05\x12\x19\n\x11incrBassaStagione\x18\x07 \x01(\x05\x12\x19\n\x11incrMediaStagione\x18\x08 \x01(\x05\x12\x10\n\x08username\x18\t \x01(\t\"\xe5\x01\n\tquoteForm\x12\x0e\n\x06numRow\x18\x01 \x01(\x05\x12\x13\n\x0bnumUmbrella\x18\x02 \x01(\x05\x12\x12\n\nnumLettini\x18\x03 \x01(\x05\x12\x11\n\tnumSdraio\x18\x04 \x01(\x05\x12\x10\n\x08numChair\x18\x05 \x01(\x05\x12,\n\x08\x66romDate\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12*\n\x06toDate\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12 \n\x08sessione\x18\x08 \x01(\x0b\x32\x0e.proto.session\"-\n\rquoteResponse\x12\x1c\n\x06quotes\x18\x01 \x03(\x0b\x32\x0c.proto.quote\"1\n\x05quote\x12\x11\n\tbeachClub\x18\x01 \x01(\t\x12\x15\n\rcomputedPrice\x18\x02 \x01(\x05\" \n\x10sentimentRequest\x12\x0c\n\x04\x63ity\x18\x01 \x01(\t\"3\n\x0e\x61nalysisOutput\x12!\n\x04\x64\x61ti\x18\x01 \x03(\x0b\x32\x13.proto.analysisData\",\n\x0c\x61nalysisData\x12\x0c\n\x04mmYY\x18\x01 \x01(\t\x12\x0e\n\x06output\x18\x02 \x03(\t\"_\n\rreviewDetails\x12\x19\n\x11usernameBeachClub\x18\x01 \x01(\t\x12\x0c\n\x04star\x18\x02 \x01(\x05\x12\x14\n\x0creviewDetail\x18\x03 \x01(\t\x12\x0f\n\x07\x63omment\x18\x04 \x01(\t\"*\n\rreviewRequest\x12\x19\n\x11usernameBeachClub\x18\x01 \x01(\t\"7\n\x0ereviewResponse\x12%\n\x07reviews\x18\x01 \x03(\x0b\x32\x14.proto.reviewDetails\"%\n\x12getAverageResponse\x12\x0f\n\x07\x61verage\x18\x01 \x01(\x02\"(\n\tupdateReq\x12\x1b\n\x01o\x18\x01 \x03(\x0b\x32\x10.proto.operation\"W\n\toperation\x12\n\n\x02op\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0e\n\x06\x63\x61rdId\x18\x03 \x01(\t\x12\x0b\n\x03\x63vc\x18\x04 \x01(\t\x12\x0f\n\x07\x63redito\x18\x05 \x01(\x05\"5\n\x11\x64\x65leteCardRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0e\n\x06\x63\x61rdId\x18\x02 \x01(\t\"O\n\rcreditDetails\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0e\n\x06\x63\x61rdId\x18\x02 \x01(\t\x12\x0f\n\x07\x63redito\x18\x03 \x01(\x05\x12\x0b\n\x03\x63vc\x18\x04 \x01(\t\"2\n\rcardsResponse\x12!\n\x05\x63\x61rds\x18\x01 \x03(\x0b\x32\x12.proto.cardDetails\"G\n\x0b\x63\x61rdDetails\x12\x0e\n\x06\x63\x61rdId\x18\x01 \x01(\t\x12\x0f\n\x07\x63redito\x18\x02 \x01(\x05\x12\x0b\n\x03\x63vc\x18\x03 \x01(\t\x12\n\n\x02id\x18\x04 \x01(\x05\"&\n\x0fregistryRequest\x12\x13\n\x0bserviceName\x18\x01 \x01(\t\"?\n\x11registryResponses\x12*\n\tresponses\x18\x01 \x03(\x0b\x32\x17.proto.registryResponse\"S\n\x10registryResponse\x12\x13\n\x0bserviceName\x18\x01 \x01(\t\x12\x10\n\x08hostname\x18\x02 \x01(\t\x12\n\n\x02ip\x18\x03 \x01(\t\x12\x0c\n\x04port\x18\x04 \x01(\t2\xad\x04\n\nAccounting\x12\x42\n\x12\x63onfigureBeachClub\x12\x1b.proto.configurationRequest\x1a\x0f.proto.response\x12>\n\x0fregisterAccount\x12\x1a.proto.registrationRequest\x1a\x0f.proto.response\x12,\n\x05login\x12\x13.proto.loginRequest\x1a\x0e.proto.session\x12\x39\n\x11updateCredentials\x12\x14.proto.updateRequest\x1a\x0e.proto.session\x12\x36\n\rdeleteAccount\x12\x14.proto.deleteRequest\x1a\x0f.proto.response\x12@\n\x17getAllBeachClubUsername\x12\x0c.proto.empty\x1a\x17.proto.usernameResponse\x12\x44\n\x15getAllBeachClubInCity\x12\x12.proto.cityRequest\x1a\x17.proto.usernameResponse\x12@\n\x13getBeachClubDetails\x12\x14.proto.reviewRequest\x1a\x13.proto.adminOptions\x12\x30\n\tgetMatrix\x12\x14.proto.reviewRequest\x1a\r.proto.matrix2\x9c\x02\n\x0bReservation\x12\x44\n\x11getListOfProposal\x12\x16.proto.proposalRequest\x1a\x17.proto.proposalResponse\x12\x35\n\x07reserve\x12\x19.proto.reservationRequest\x1a\x0f.proto.response\x12\x41\n\rmanualReserve\x12\x1f.proto.manualReservationRequest\x1a\x0f.proto.response\x12M\n\x10getReservedSeats\x12\x1b.proto.reservedSeatsRequest\x1a\x1c.proto.reservedSeatsResponse2v\n\x05Quote\x12\x34\n\x0cinsertPrices\x12\x13.proto.priceRequest\x1a\x0f.proto.response\x12\x37\n\rcomputeQuotes\x12\x10.proto.quoteForm\x1a\x14.proto.quoteResponse2\x96\x02\n\x06Review\x12/\n\x06review\x12\x14.proto.reviewDetails\x1a\x0f.proto.response\x12G\n\x18getAllReviewsOfBeachClub\x12\x14.proto.reviewRequest\x1a\x15.proto.reviewResponse\x12M\n\x1agetAverageScoreOfBeachClub\x12\x14.proto.reviewRequest\x1a\x19.proto.getAverageResponse\x12\x43\n\x11sentimentAnalysis\x12\x17.proto.sentimentRequest\x1a\x15.proto.analysisOutput2\x90\x02\n\x07Payment\x12\x37\n\ndeleteCard\x12\x18.proto.deleteCardRequest\x1a\x0f.proto.response\x12\x39\n\x10insertCreditCard\x12\x14.proto.creditDetails\x1a\x0f.proto.response\x12\x31\n\tshowCards\x12\x0e.proto.session\x1a\x14.proto.cardsResponse\x12*\n\x0cstartConsume\x12\x0c.proto.empty\x1a\x0c.proto.empty\x12\x32\n\rupdateRequest\x12\x10.proto.updateReq\x1a\x0f.proto.response2S\n\x0fServiceRegistry\x12@\n\x0cgetPortAndIp\x12\x16.proto.registryRequest\x1a\x18.proto.registryResponsesb\x06proto3')



_CITYREQUEST = DESCRIPTOR.message_types_by_name['cityRequest']
_MATRIX = DESCRIPTOR.message_types_by_name['matrix']
_USERNAMERESPONSE = DESCRIPTOR.message_types_by_name['usernameResponse']
_EMPTY = DESCRIPTOR.message_types_by_name['empty']
_DELETEREQUEST = DESCRIPTOR.message_types_by_name['deleteRequest']
_UPDATEREQUEST = DESCRIPTOR.message_types_by_name['updateRequest']
_REGISTRATIONREQUEST = DESCRIPTOR.message_types_by_name['registrationRequest']
_LOGINREQUEST = DESCRIPTOR.message_types_by_name['loginRequest']
_ADMINOPTIONS = DESCRIPTOR.message_types_by_name['adminOptions']
_RESPONSE = DESCRIPTOR.message_types_by_name['response']
_SESSION = DESCRIPTOR.message_types_by_name['session']
_DICTIONARY = DESCRIPTOR.message_types_by_name['dictionary']
_RESERVEDSEATSREQUEST = DESCRIPTOR.message_types_by_name['reservedSeatsRequest']
_RESERVEDSEATSRESPONSE = DESCRIPTOR.message_types_by_name['reservedSeatsResponse']
_RESERVATION = DESCRIPTOR.message_types_by_name['reservation']
_MANUALRESERVATIONREQUEST = DESCRIPTOR.message_types_by_name['manualReservationRequest']
_PROPOSALRESPONSE = DESCRIPTOR.message_types_by_name['proposalResponse']
_PROPOSAL = DESCRIPTOR.message_types_by_name['proposal']
_CONFIGURATIONREQUEST = DESCRIPTOR.message_types_by_name['configurationRequest']
_NUMSEATBYROW = DESCRIPTOR.message_types_by_name['numSeatByRow']
_PROPOSALREQUEST = DESCRIPTOR.message_types_by_name['proposalRequest']
_RESERVATIONREQUEST = DESCRIPTOR.message_types_by_name['reservationRequest']
_PRICEREQUEST = DESCRIPTOR.message_types_by_name['priceRequest']
_QUOTEFORM = DESCRIPTOR.message_types_by_name['quoteForm']
_QUOTERESPONSE = DESCRIPTOR.message_types_by_name['quoteResponse']
_QUOTE = DESCRIPTOR.message_types_by_name['quote']
_SENTIMENTREQUEST = DESCRIPTOR.message_types_by_name['sentimentRequest']
_ANALYSISOUTPUT = DESCRIPTOR.message_types_by_name['analysisOutput']
_ANALYSISDATA = DESCRIPTOR.message_types_by_name['analysisData']
_REVIEWDETAILS = DESCRIPTOR.message_types_by_name['reviewDetails']
_REVIEWREQUEST = DESCRIPTOR.message_types_by_name['reviewRequest']
_REVIEWRESPONSE = DESCRIPTOR.message_types_by_name['reviewResponse']
_GETAVERAGERESPONSE = DESCRIPTOR.message_types_by_name['getAverageResponse']
_UPDATEREQ = DESCRIPTOR.message_types_by_name['updateReq']
_OPERATION = DESCRIPTOR.message_types_by_name['operation']
_DELETECARDREQUEST = DESCRIPTOR.message_types_by_name['deleteCardRequest']
_CREDITDETAILS = DESCRIPTOR.message_types_by_name['creditDetails']
_CARDSRESPONSE = DESCRIPTOR.message_types_by_name['cardsResponse']
_CARDDETAILS = DESCRIPTOR.message_types_by_name['cardDetails']
_REGISTRYREQUEST = DESCRIPTOR.message_types_by_name['registryRequest']
_REGISTRYRESPONSES = DESCRIPTOR.message_types_by_name['registryResponses']
_REGISTRYRESPONSE = DESCRIPTOR.message_types_by_name['registryResponse']
cityRequest = _reflection.GeneratedProtocolMessageType('cityRequest', (_message.Message,), {
  'DESCRIPTOR' : _CITYREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.cityRequest)
  })
_sym_db.RegisterMessage(cityRequest)

matrix = _reflection.GeneratedProtocolMessageType('matrix', (_message.Message,), {
  'DESCRIPTOR' : _MATRIX,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.matrix)
  })
_sym_db.RegisterMessage(matrix)

usernameResponse = _reflection.GeneratedProtocolMessageType('usernameResponse', (_message.Message,), {
  'DESCRIPTOR' : _USERNAMERESPONSE,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.usernameResponse)
  })
_sym_db.RegisterMessage(usernameResponse)

empty = _reflection.GeneratedProtocolMessageType('empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.empty)
  })
_sym_db.RegisterMessage(empty)

deleteRequest = _reflection.GeneratedProtocolMessageType('deleteRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.deleteRequest)
  })
_sym_db.RegisterMessage(deleteRequest)

updateRequest = _reflection.GeneratedProtocolMessageType('updateRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.updateRequest)
  })
_sym_db.RegisterMessage(updateRequest)

registrationRequest = _reflection.GeneratedProtocolMessageType('registrationRequest', (_message.Message,), {
  'DESCRIPTOR' : _REGISTRATIONREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.registrationRequest)
  })
_sym_db.RegisterMessage(registrationRequest)

loginRequest = _reflection.GeneratedProtocolMessageType('loginRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOGINREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.loginRequest)
  })
_sym_db.RegisterMessage(loginRequest)

adminOptions = _reflection.GeneratedProtocolMessageType('adminOptions', (_message.Message,), {
  'DESCRIPTOR' : _ADMINOPTIONS,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.adminOptions)
  })
_sym_db.RegisterMessage(adminOptions)

response = _reflection.GeneratedProtocolMessageType('response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.response)
  })
_sym_db.RegisterMessage(response)

session = _reflection.GeneratedProtocolMessageType('session', (_message.Message,), {
  'DESCRIPTOR' : _SESSION,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.session)
  })
_sym_db.RegisterMessage(session)

dictionary = _reflection.GeneratedProtocolMessageType('dictionary', (_message.Message,), {
  'DESCRIPTOR' : _DICTIONARY,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.dictionary)
  })
_sym_db.RegisterMessage(dictionary)

reservedSeatsRequest = _reflection.GeneratedProtocolMessageType('reservedSeatsRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESERVEDSEATSREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.reservedSeatsRequest)
  })
_sym_db.RegisterMessage(reservedSeatsRequest)

reservedSeatsResponse = _reflection.GeneratedProtocolMessageType('reservedSeatsResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESERVEDSEATSRESPONSE,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.reservedSeatsResponse)
  })
_sym_db.RegisterMessage(reservedSeatsResponse)

reservation = _reflection.GeneratedProtocolMessageType('reservation', (_message.Message,), {
  'DESCRIPTOR' : _RESERVATION,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.reservation)
  })
_sym_db.RegisterMessage(reservation)

manualReservationRequest = _reflection.GeneratedProtocolMessageType('manualReservationRequest', (_message.Message,), {
  'DESCRIPTOR' : _MANUALRESERVATIONREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.manualReservationRequest)
  })
_sym_db.RegisterMessage(manualReservationRequest)

proposalResponse = _reflection.GeneratedProtocolMessageType('proposalResponse', (_message.Message,), {
  'DESCRIPTOR' : _PROPOSALRESPONSE,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.proposalResponse)
  })
_sym_db.RegisterMessage(proposalResponse)

proposal = _reflection.GeneratedProtocolMessageType('proposal', (_message.Message,), {
  'DESCRIPTOR' : _PROPOSAL,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.proposal)
  })
_sym_db.RegisterMessage(proposal)

configurationRequest = _reflection.GeneratedProtocolMessageType('configurationRequest', (_message.Message,), {
  'DESCRIPTOR' : _CONFIGURATIONREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.configurationRequest)
  })
_sym_db.RegisterMessage(configurationRequest)

numSeatByRow = _reflection.GeneratedProtocolMessageType('numSeatByRow', (_message.Message,), {
  'DESCRIPTOR' : _NUMSEATBYROW,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.numSeatByRow)
  })
_sym_db.RegisterMessage(numSeatByRow)

proposalRequest = _reflection.GeneratedProtocolMessageType('proposalRequest', (_message.Message,), {
  'DESCRIPTOR' : _PROPOSALREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.proposalRequest)
  })
_sym_db.RegisterMessage(proposalRequest)

reservationRequest = _reflection.GeneratedProtocolMessageType('reservationRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESERVATIONREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.reservationRequest)
  })
_sym_db.RegisterMessage(reservationRequest)

priceRequest = _reflection.GeneratedProtocolMessageType('priceRequest', (_message.Message,), {
  'DESCRIPTOR' : _PRICEREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.priceRequest)
  })
_sym_db.RegisterMessage(priceRequest)

quoteForm = _reflection.GeneratedProtocolMessageType('quoteForm', (_message.Message,), {
  'DESCRIPTOR' : _QUOTEFORM,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.quoteForm)
  })
_sym_db.RegisterMessage(quoteForm)

quoteResponse = _reflection.GeneratedProtocolMessageType('quoteResponse', (_message.Message,), {
  'DESCRIPTOR' : _QUOTERESPONSE,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.quoteResponse)
  })
_sym_db.RegisterMessage(quoteResponse)

quote = _reflection.GeneratedProtocolMessageType('quote', (_message.Message,), {
  'DESCRIPTOR' : _QUOTE,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.quote)
  })
_sym_db.RegisterMessage(quote)

sentimentRequest = _reflection.GeneratedProtocolMessageType('sentimentRequest', (_message.Message,), {
  'DESCRIPTOR' : _SENTIMENTREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.sentimentRequest)
  })
_sym_db.RegisterMessage(sentimentRequest)

analysisOutput = _reflection.GeneratedProtocolMessageType('analysisOutput', (_message.Message,), {
  'DESCRIPTOR' : _ANALYSISOUTPUT,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.analysisOutput)
  })
_sym_db.RegisterMessage(analysisOutput)

analysisData = _reflection.GeneratedProtocolMessageType('analysisData', (_message.Message,), {
  'DESCRIPTOR' : _ANALYSISDATA,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.analysisData)
  })
_sym_db.RegisterMessage(analysisData)

reviewDetails = _reflection.GeneratedProtocolMessageType('reviewDetails', (_message.Message,), {
  'DESCRIPTOR' : _REVIEWDETAILS,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.reviewDetails)
  })
_sym_db.RegisterMessage(reviewDetails)

reviewRequest = _reflection.GeneratedProtocolMessageType('reviewRequest', (_message.Message,), {
  'DESCRIPTOR' : _REVIEWREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.reviewRequest)
  })
_sym_db.RegisterMessage(reviewRequest)

reviewResponse = _reflection.GeneratedProtocolMessageType('reviewResponse', (_message.Message,), {
  'DESCRIPTOR' : _REVIEWRESPONSE,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.reviewResponse)
  })
_sym_db.RegisterMessage(reviewResponse)

getAverageResponse = _reflection.GeneratedProtocolMessageType('getAverageResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETAVERAGERESPONSE,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.getAverageResponse)
  })
_sym_db.RegisterMessage(getAverageResponse)

updateReq = _reflection.GeneratedProtocolMessageType('updateReq', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEREQ,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.updateReq)
  })
_sym_db.RegisterMessage(updateReq)

operation = _reflection.GeneratedProtocolMessageType('operation', (_message.Message,), {
  'DESCRIPTOR' : _OPERATION,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.operation)
  })
_sym_db.RegisterMessage(operation)

deleteCardRequest = _reflection.GeneratedProtocolMessageType('deleteCardRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETECARDREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.deleteCardRequest)
  })
_sym_db.RegisterMessage(deleteCardRequest)

creditDetails = _reflection.GeneratedProtocolMessageType('creditDetails', (_message.Message,), {
  'DESCRIPTOR' : _CREDITDETAILS,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.creditDetails)
  })
_sym_db.RegisterMessage(creditDetails)

cardsResponse = _reflection.GeneratedProtocolMessageType('cardsResponse', (_message.Message,), {
  'DESCRIPTOR' : _CARDSRESPONSE,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.cardsResponse)
  })
_sym_db.RegisterMessage(cardsResponse)

cardDetails = _reflection.GeneratedProtocolMessageType('cardDetails', (_message.Message,), {
  'DESCRIPTOR' : _CARDDETAILS,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.cardDetails)
  })
_sym_db.RegisterMessage(cardDetails)

registryRequest = _reflection.GeneratedProtocolMessageType('registryRequest', (_message.Message,), {
  'DESCRIPTOR' : _REGISTRYREQUEST,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.registryRequest)
  })
_sym_db.RegisterMessage(registryRequest)

registryResponses = _reflection.GeneratedProtocolMessageType('registryResponses', (_message.Message,), {
  'DESCRIPTOR' : _REGISTRYRESPONSES,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.registryResponses)
  })
_sym_db.RegisterMessage(registryResponses)

registryResponse = _reflection.GeneratedProtocolMessageType('registryResponse', (_message.Message,), {
  'DESCRIPTOR' : _REGISTRYRESPONSE,
  '__module__' : 'proto.grpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.registryResponse)
  })
_sym_db.RegisterMessage(registryResponse)

_ACCOUNTING = DESCRIPTOR.services_by_name['Accounting']
_RESERVATION = DESCRIPTOR.services_by_name['Reservation']
_QUOTE = DESCRIPTOR.services_by_name['Quote']
_REVIEW = DESCRIPTOR.services_by_name['Review']
_PAYMENT = DESCRIPTOR.services_by_name['Payment']
_SERVICEREGISTRY = DESCRIPTOR.services_by_name['ServiceRegistry']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CITYREQUEST._serialized_start=60
  _CITYREQUEST._serialized_end=87
  _MATRIX._serialized_start=89
  _MATRIX._serialized_end=115
  _USERNAMERESPONSE._serialized_start=117
  _USERNAMERESPONSE._serialized_end=162
  _EMPTY._serialized_start=164
  _EMPTY._serialized_end=171
  _DELETEREQUEST._serialized_start=173
  _DELETEREQUEST._serialized_end=221
  _UPDATEREQUEST._serialized_start=223
  _UPDATEREQUEST._serialized_end=344
  _REGISTRATIONREQUEST._serialized_start=346
  _REGISTRATIONREQUEST._serialized_end=467
  _LOGINREQUEST._serialized_start=469
  _LOGINREQUEST._serialized_end=519
  _ADMINOPTIONS._serialized_start=522
  _ADMINOPTIONS._serialized_end=694
  _RESPONSE._serialized_start=696
  _RESPONSE._serialized_end=753
  _SESSION._serialized_start=755
  _SESSION._serialized_end=797
  _DICTIONARY._serialized_start=799
  _DICTIONARY._serialized_end=839
  _RESERVEDSEATSREQUEST._serialized_start=841
  _RESERVEDSEATSREQUEST._serialized_end=926
  _RESERVEDSEATSRESPONSE._serialized_start=928
  _RESERVEDSEATSRESPONSE._serialized_end=992
  _RESERVATION._serialized_start=994
  _RESERVATION._serialized_end=1045
  _MANUALRESERVATIONREQUEST._serialized_start=1048
  _MANUALRESERVATIONREQUEST._serialized_end=1192
  _PROPOSALRESPONSE._serialized_start=1194
  _PROPOSALRESPONSE._serialized_end=1246
  _PROPOSAL._serialized_start=1248
  _PROPOSAL._serialized_end=1360
  _CONFIGURATIONREQUEST._serialized_start=1363
  _CONFIGURATIONREQUEST._serialized_end=1529
  _NUMSEATBYROW._serialized_start=1531
  _NUMSEATBYROW._serialized_end=1567
  _PROPOSALREQUEST._serialized_start=1570
  _PROPOSALREQUEST._serialized_end=1846
  _RESERVATIONREQUEST._serialized_start=1849
  _RESERVATIONREQUEST._serialized_end=2202
  _PRICEREQUEST._serialized_start=2205
  _PRICEREQUEST._serialized_end=2428
  _QUOTEFORM._serialized_start=2431
  _QUOTEFORM._serialized_end=2660
  _QUOTERESPONSE._serialized_start=2662
  _QUOTERESPONSE._serialized_end=2707
  _QUOTE._serialized_start=2709
  _QUOTE._serialized_end=2758
  _SENTIMENTREQUEST._serialized_start=2760
  _SENTIMENTREQUEST._serialized_end=2792
  _ANALYSISOUTPUT._serialized_start=2794
  _ANALYSISOUTPUT._serialized_end=2845
  _ANALYSISDATA._serialized_start=2847
  _ANALYSISDATA._serialized_end=2891
  _REVIEWDETAILS._serialized_start=2893
  _REVIEWDETAILS._serialized_end=2988
  _REVIEWREQUEST._serialized_start=2990
  _REVIEWREQUEST._serialized_end=3032
  _REVIEWRESPONSE._serialized_start=3034
  _REVIEWRESPONSE._serialized_end=3089
  _GETAVERAGERESPONSE._serialized_start=3091
  _GETAVERAGERESPONSE._serialized_end=3128
  _UPDATEREQ._serialized_start=3130
  _UPDATEREQ._serialized_end=3170
  _OPERATION._serialized_start=3172
  _OPERATION._serialized_end=3259
  _DELETECARDREQUEST._serialized_start=3261
  _DELETECARDREQUEST._serialized_end=3314
  _CREDITDETAILS._serialized_start=3316
  _CREDITDETAILS._serialized_end=3395
  _CARDSRESPONSE._serialized_start=3397
  _CARDSRESPONSE._serialized_end=3447
  _CARDDETAILS._serialized_start=3449
  _CARDDETAILS._serialized_end=3520
  _REGISTRYREQUEST._serialized_start=3522
  _REGISTRYREQUEST._serialized_end=3560
  _REGISTRYRESPONSES._serialized_start=3562
  _REGISTRYRESPONSES._serialized_end=3625
  _REGISTRYRESPONSE._serialized_start=3627
  _REGISTRYRESPONSE._serialized_end=3710
  _ACCOUNTING._serialized_start=3713
  _ACCOUNTING._serialized_end=4270
  _RESERVATION._serialized_start=4273
  _RESERVATION._serialized_end=4557
  _QUOTE._serialized_start=4559
  _QUOTE._serialized_end=4677
  _REVIEW._serialized_start=4680
  _REVIEW._serialized_end=4958
  _PAYMENT._serialized_start=4961
  _PAYMENT._serialized_end=5233
  _SERVICEREGISTRY._serialized_start=5235
  _SERVICEREGISTRY._serialized_end=5318
# @@protoc_insertion_point(module_scope)
