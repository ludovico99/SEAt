# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import grpc_pb2 as proto_dot_grpc__pb2


class AccountingStub(object):
    """------------ Accounting Service ---------------
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.configureBeachClub = channel.unary_unary(
                '/proto.Accounting/configureBeachClub',
                request_serializer=proto_dot_grpc__pb2.configurationRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.response.FromString,
                )
        self.registerAccount = channel.unary_unary(
                '/proto.Accounting/registerAccount',
                request_serializer=proto_dot_grpc__pb2.registrationRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.response.FromString,
                )
        self.login = channel.unary_unary(
                '/proto.Accounting/login',
                request_serializer=proto_dot_grpc__pb2.loginRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.session.FromString,
                )
        self.updateCredentials = channel.unary_unary(
                '/proto.Accounting/updateCredentials',
                request_serializer=proto_dot_grpc__pb2.updateRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.session.FromString,
                )
        self.deleteAccount = channel.unary_unary(
                '/proto.Accounting/deleteAccount',
                request_serializer=proto_dot_grpc__pb2.deleteRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.response.FromString,
                )
        self.getAllBeachClubUsername = channel.unary_unary(
                '/proto.Accounting/getAllBeachClubUsername',
                request_serializer=proto_dot_grpc__pb2.empty.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.usernameResponse.FromString,
                )
        self.getAllBeachClubInCity = channel.unary_unary(
                '/proto.Accounting/getAllBeachClubInCity',
                request_serializer=proto_dot_grpc__pb2.cityRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.usernameResponse.FromString,
                )
        self.getBeachClubDetails = channel.unary_unary(
                '/proto.Accounting/getBeachClubDetails',
                request_serializer=proto_dot_grpc__pb2.reviewRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.adminOptions.FromString,
                )
        self.getMatrix = channel.unary_unary(
                '/proto.Accounting/getMatrix',
                request_serializer=proto_dot_grpc__pb2.reviewRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.matrix.FromString,
                )


class AccountingServicer(object):
    """------------ Accounting Service ---------------
    """

    def configureBeachClub(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def login(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def updateCredentials(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getAllBeachClubUsername(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getAllBeachClubInCity(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getBeachClubDetails(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getMatrix(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AccountingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'configureBeachClub': grpc.unary_unary_rpc_method_handler(
                    servicer.configureBeachClub,
                    request_deserializer=proto_dot_grpc__pb2.configurationRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.response.SerializeToString,
            ),
            'registerAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.registerAccount,
                    request_deserializer=proto_dot_grpc__pb2.registrationRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.response.SerializeToString,
            ),
            'login': grpc.unary_unary_rpc_method_handler(
                    servicer.login,
                    request_deserializer=proto_dot_grpc__pb2.loginRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.session.SerializeToString,
            ),
            'updateCredentials': grpc.unary_unary_rpc_method_handler(
                    servicer.updateCredentials,
                    request_deserializer=proto_dot_grpc__pb2.updateRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.session.SerializeToString,
            ),
            'deleteAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteAccount,
                    request_deserializer=proto_dot_grpc__pb2.deleteRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.response.SerializeToString,
            ),
            'getAllBeachClubUsername': grpc.unary_unary_rpc_method_handler(
                    servicer.getAllBeachClubUsername,
                    request_deserializer=proto_dot_grpc__pb2.empty.FromString,
                    response_serializer=proto_dot_grpc__pb2.usernameResponse.SerializeToString,
            ),
            'getAllBeachClubInCity': grpc.unary_unary_rpc_method_handler(
                    servicer.getAllBeachClubInCity,
                    request_deserializer=proto_dot_grpc__pb2.cityRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.usernameResponse.SerializeToString,
            ),
            'getBeachClubDetails': grpc.unary_unary_rpc_method_handler(
                    servicer.getBeachClubDetails,
                    request_deserializer=proto_dot_grpc__pb2.reviewRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.adminOptions.SerializeToString,
            ),
            'getMatrix': grpc.unary_unary_rpc_method_handler(
                    servicer.getMatrix,
                    request_deserializer=proto_dot_grpc__pb2.reviewRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.matrix.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proto.Accounting', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Accounting(object):
    """------------ Accounting Service ---------------
    """

    @staticmethod
    def configureBeachClub(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Accounting/configureBeachClub',
            proto_dot_grpc__pb2.configurationRequest.SerializeToString,
            proto_dot_grpc__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def registerAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Accounting/registerAccount',
            proto_dot_grpc__pb2.registrationRequest.SerializeToString,
            proto_dot_grpc__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def login(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Accounting/login',
            proto_dot_grpc__pb2.loginRequest.SerializeToString,
            proto_dot_grpc__pb2.session.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def updateCredentials(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Accounting/updateCredentials',
            proto_dot_grpc__pb2.updateRequest.SerializeToString,
            proto_dot_grpc__pb2.session.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deleteAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Accounting/deleteAccount',
            proto_dot_grpc__pb2.deleteRequest.SerializeToString,
            proto_dot_grpc__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getAllBeachClubUsername(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Accounting/getAllBeachClubUsername',
            proto_dot_grpc__pb2.empty.SerializeToString,
            proto_dot_grpc__pb2.usernameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getAllBeachClubInCity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Accounting/getAllBeachClubInCity',
            proto_dot_grpc__pb2.cityRequest.SerializeToString,
            proto_dot_grpc__pb2.usernameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getBeachClubDetails(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Accounting/getBeachClubDetails',
            proto_dot_grpc__pb2.reviewRequest.SerializeToString,
            proto_dot_grpc__pb2.adminOptions.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getMatrix(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Accounting/getMatrix',
            proto_dot_grpc__pb2.reviewRequest.SerializeToString,
            proto_dot_grpc__pb2.matrix.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ReservationStub(object):
    """------------ Reservation Service ---------------

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getListOfProposal = channel.unary_unary(
                '/proto.Reservation/getListOfProposal',
                request_serializer=proto_dot_grpc__pb2.proposalRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.proposalResponse.FromString,
                )
        self.reserve = channel.unary_unary(
                '/proto.Reservation/reserve',
                request_serializer=proto_dot_grpc__pb2.reservationRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.response.FromString,
                )
        self.manualReserve = channel.unary_unary(
                '/proto.Reservation/manualReserve',
                request_serializer=proto_dot_grpc__pb2.manualReservationRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.response.FromString,
                )
        self.getReservedSeats = channel.unary_unary(
                '/proto.Reservation/getReservedSeats',
                request_serializer=proto_dot_grpc__pb2.reservedSeatsRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.reservedSeatsResponse.FromString,
                )


class ReservationServicer(object):
    """------------ Reservation Service ---------------

    """

    def getListOfProposal(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def reserve(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def manualReserve(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getReservedSeats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReservationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getListOfProposal': grpc.unary_unary_rpc_method_handler(
                    servicer.getListOfProposal,
                    request_deserializer=proto_dot_grpc__pb2.proposalRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.proposalResponse.SerializeToString,
            ),
            'reserve': grpc.unary_unary_rpc_method_handler(
                    servicer.reserve,
                    request_deserializer=proto_dot_grpc__pb2.reservationRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.response.SerializeToString,
            ),
            'manualReserve': grpc.unary_unary_rpc_method_handler(
                    servicer.manualReserve,
                    request_deserializer=proto_dot_grpc__pb2.manualReservationRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.response.SerializeToString,
            ),
            'getReservedSeats': grpc.unary_unary_rpc_method_handler(
                    servicer.getReservedSeats,
                    request_deserializer=proto_dot_grpc__pb2.reservedSeatsRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.reservedSeatsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proto.Reservation', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Reservation(object):
    """------------ Reservation Service ---------------

    """

    @staticmethod
    def getListOfProposal(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Reservation/getListOfProposal',
            proto_dot_grpc__pb2.proposalRequest.SerializeToString,
            proto_dot_grpc__pb2.proposalResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def reserve(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Reservation/reserve',
            proto_dot_grpc__pb2.reservationRequest.SerializeToString,
            proto_dot_grpc__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def manualReserve(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Reservation/manualReserve',
            proto_dot_grpc__pb2.manualReservationRequest.SerializeToString,
            proto_dot_grpc__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getReservedSeats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Reservation/getReservedSeats',
            proto_dot_grpc__pb2.reservedSeatsRequest.SerializeToString,
            proto_dot_grpc__pb2.reservedSeatsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class QuoteStub(object):
    """------------ Quote Service ---------------

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.insertPrices = channel.unary_unary(
                '/proto.Quote/insertPrices',
                request_serializer=proto_dot_grpc__pb2.priceRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.response.FromString,
                )
        self.computeQuotes = channel.unary_unary(
                '/proto.Quote/computeQuotes',
                request_serializer=proto_dot_grpc__pb2.quoteForm.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.quoteResponse.FromString,
                )


class QuoteServicer(object):
    """------------ Quote Service ---------------

    """

    def insertPrices(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def computeQuotes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QuoteServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'insertPrices': grpc.unary_unary_rpc_method_handler(
                    servicer.insertPrices,
                    request_deserializer=proto_dot_grpc__pb2.priceRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.response.SerializeToString,
            ),
            'computeQuotes': grpc.unary_unary_rpc_method_handler(
                    servicer.computeQuotes,
                    request_deserializer=proto_dot_grpc__pb2.quoteForm.FromString,
                    response_serializer=proto_dot_grpc__pb2.quoteResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proto.Quote', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Quote(object):
    """------------ Quote Service ---------------

    """

    @staticmethod
    def insertPrices(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Quote/insertPrices',
            proto_dot_grpc__pb2.priceRequest.SerializeToString,
            proto_dot_grpc__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def computeQuotes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Quote/computeQuotes',
            proto_dot_grpc__pb2.quoteForm.SerializeToString,
            proto_dot_grpc__pb2.quoteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ReviewStub(object):
    """------------ Review Service ---------------

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.review = channel.unary_unary(
                '/proto.Review/review',
                request_serializer=proto_dot_grpc__pb2.reviewDetails.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.response.FromString,
                )
        self.getAllReviewsOfBeachClub = channel.unary_unary(
                '/proto.Review/getAllReviewsOfBeachClub',
                request_serializer=proto_dot_grpc__pb2.reviewRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.reviewResponse.FromString,
                )
        self.getAverageScoreOfBeachClub = channel.unary_unary(
                '/proto.Review/getAverageScoreOfBeachClub',
                request_serializer=proto_dot_grpc__pb2.reviewRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.getAverageResponse.FromString,
                )
        self.sentimentAnalysis = channel.unary_unary(
                '/proto.Review/sentimentAnalysis',
                request_serializer=proto_dot_grpc__pb2.sentimentRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.analysisOutput.FromString,
                )


class ReviewServicer(object):
    """------------ Review Service ---------------

    """

    def review(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getAllReviewsOfBeachClub(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getAverageScoreOfBeachClub(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def sentimentAnalysis(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReviewServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'review': grpc.unary_unary_rpc_method_handler(
                    servicer.review,
                    request_deserializer=proto_dot_grpc__pb2.reviewDetails.FromString,
                    response_serializer=proto_dot_grpc__pb2.response.SerializeToString,
            ),
            'getAllReviewsOfBeachClub': grpc.unary_unary_rpc_method_handler(
                    servicer.getAllReviewsOfBeachClub,
                    request_deserializer=proto_dot_grpc__pb2.reviewRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.reviewResponse.SerializeToString,
            ),
            'getAverageScoreOfBeachClub': grpc.unary_unary_rpc_method_handler(
                    servicer.getAverageScoreOfBeachClub,
                    request_deserializer=proto_dot_grpc__pb2.reviewRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.getAverageResponse.SerializeToString,
            ),
            'sentimentAnalysis': grpc.unary_unary_rpc_method_handler(
                    servicer.sentimentAnalysis,
                    request_deserializer=proto_dot_grpc__pb2.sentimentRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.analysisOutput.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proto.Review', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Review(object):
    """------------ Review Service ---------------

    """

    @staticmethod
    def review(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Review/review',
            proto_dot_grpc__pb2.reviewDetails.SerializeToString,
            proto_dot_grpc__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getAllReviewsOfBeachClub(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Review/getAllReviewsOfBeachClub',
            proto_dot_grpc__pb2.reviewRequest.SerializeToString,
            proto_dot_grpc__pb2.reviewResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getAverageScoreOfBeachClub(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Review/getAverageScoreOfBeachClub',
            proto_dot_grpc__pb2.reviewRequest.SerializeToString,
            proto_dot_grpc__pb2.getAverageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def sentimentAnalysis(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Review/sentimentAnalysis',
            proto_dot_grpc__pb2.sentimentRequest.SerializeToString,
            proto_dot_grpc__pb2.analysisOutput.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class PaymentStub(object):
    """------------ Payment Service ---------------

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.deleteCard = channel.unary_unary(
                '/proto.Payment/deleteCard',
                request_serializer=proto_dot_grpc__pb2.deleteCardRequest.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.response.FromString,
                )
        self.insertCreditCard = channel.unary_unary(
                '/proto.Payment/insertCreditCard',
                request_serializer=proto_dot_grpc__pb2.creditDetails.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.response.FromString,
                )
        self.showCards = channel.unary_unary(
                '/proto.Payment/showCards',
                request_serializer=proto_dot_grpc__pb2.session.SerializeToString,
                response_deserializer=proto_dot_grpc__pb2.cardsResponse.FromString,
                )


class PaymentServicer(object):
    """------------ Payment Service ---------------

    """

    def deleteCard(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def insertCreditCard(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def showCards(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PaymentServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'deleteCard': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteCard,
                    request_deserializer=proto_dot_grpc__pb2.deleteCardRequest.FromString,
                    response_serializer=proto_dot_grpc__pb2.response.SerializeToString,
            ),
            'insertCreditCard': grpc.unary_unary_rpc_method_handler(
                    servicer.insertCreditCard,
                    request_deserializer=proto_dot_grpc__pb2.creditDetails.FromString,
                    response_serializer=proto_dot_grpc__pb2.response.SerializeToString,
            ),
            'showCards': grpc.unary_unary_rpc_method_handler(
                    servicer.showCards,
                    request_deserializer=proto_dot_grpc__pb2.session.FromString,
                    response_serializer=proto_dot_grpc__pb2.cardsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proto.Payment', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Payment(object):
    """------------ Payment Service ---------------

    """

    @staticmethod
    def deleteCard(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Payment/deleteCard',
            proto_dot_grpc__pb2.deleteCardRequest.SerializeToString,
            proto_dot_grpc__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def insertCreditCard(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Payment/insertCreditCard',
            proto_dot_grpc__pb2.creditDetails.SerializeToString,
            proto_dot_grpc__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def showCards(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Payment/showCards',
            proto_dot_grpc__pb2.session.SerializeToString,
            proto_dot_grpc__pb2.cardsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
