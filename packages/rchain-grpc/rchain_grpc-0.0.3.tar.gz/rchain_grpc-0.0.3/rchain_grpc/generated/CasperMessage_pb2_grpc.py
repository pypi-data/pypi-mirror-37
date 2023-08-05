# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import CasperMessage_pb2 as CasperMessage__pb2
import RhoTypes_pb2 as RhoTypes__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class DeployServiceStub(object):
    """--------- DeployService  --------
  """

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.DoDeploy = channel.unary_unary(
            '/coop.rchain.casper.protocol.DeployService/DoDeploy',
            request_serializer=CasperMessage__pb2.DeployData.SerializeToString,
            response_deserializer=CasperMessage__pb2.DeployServiceResponse.FromString,
        )
        self.addBlock = channel.unary_unary(
            '/coop.rchain.casper.protocol.DeployService/addBlock',
            request_serializer=CasperMessage__pb2.BlockMessage.SerializeToString,
            response_deserializer=CasperMessage__pb2.DeployServiceResponse.FromString,
        )
        self.createBlock = channel.unary_unary(
            '/coop.rchain.casper.protocol.DeployService/createBlock',
            request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            response_deserializer=CasperMessage__pb2.DeployServiceResponse.FromString,
        )
        self.showBlock = channel.unary_unary(
            '/coop.rchain.casper.protocol.DeployService/showBlock',
            request_serializer=CasperMessage__pb2.BlockQuery.SerializeToString,
            response_deserializer=CasperMessage__pb2.BlockQueryResponse.FromString,
        )
        self.showBlocks = channel.unary_stream(
            '/coop.rchain.casper.protocol.DeployService/showBlocks',
            request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            response_deserializer=CasperMessage__pb2.BlockInfo.FromString,
        )
        self.listenForDataAtName = channel.unary_unary(
            '/coop.rchain.casper.protocol.DeployService/listenForDataAtName',
            request_serializer=RhoTypes__pb2.Channel.SerializeToString,
            response_deserializer=CasperMessage__pb2.ListeningNameDataResponse.FromString,
        )
        self.listenForContinuationAtName = channel.unary_unary(
            '/coop.rchain.casper.protocol.DeployService/listenForContinuationAtName',
            request_serializer=CasperMessage__pb2.Channels.SerializeToString,
            response_deserializer=CasperMessage__pb2.ListeningNameContinuationResponse.FromString,
        )


class DeployServiceServicer(object):
    """--------- DeployService  --------
  """

    def DoDeploy(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addBlock(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def createBlock(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def showBlock(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def showBlocks(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def listenForDataAtName(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def listenForContinuationAtName(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DeployServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'DoDeploy': grpc.unary_unary_rpc_method_handler(
            servicer.DoDeploy,
            request_deserializer=CasperMessage__pb2.DeployData.FromString,
            response_serializer=CasperMessage__pb2.DeployServiceResponse.SerializeToString,
        ),
        'addBlock': grpc.unary_unary_rpc_method_handler(
            servicer.addBlock,
            request_deserializer=CasperMessage__pb2.BlockMessage.FromString,
            response_serializer=CasperMessage__pb2.DeployServiceResponse.SerializeToString,
        ),
        'createBlock': grpc.unary_unary_rpc_method_handler(
            servicer.createBlock,
            request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            response_serializer=CasperMessage__pb2.DeployServiceResponse.SerializeToString,
        ),
        'showBlock': grpc.unary_unary_rpc_method_handler(
            servicer.showBlock,
            request_deserializer=CasperMessage__pb2.BlockQuery.FromString,
            response_serializer=CasperMessage__pb2.BlockQueryResponse.SerializeToString,
        ),
        'showBlocks': grpc.unary_stream_rpc_method_handler(
            servicer.showBlocks,
            request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            response_serializer=CasperMessage__pb2.BlockInfo.SerializeToString,
        ),
        'listenForDataAtName': grpc.unary_unary_rpc_method_handler(
            servicer.listenForDataAtName,
            request_deserializer=RhoTypes__pb2.Channel.FromString,
            response_serializer=CasperMessage__pb2.ListeningNameDataResponse.SerializeToString,
        ),
        'listenForContinuationAtName': grpc.unary_unary_rpc_method_handler(
            servicer.listenForContinuationAtName,
            request_deserializer=CasperMessage__pb2.Channels.FromString,
            response_serializer=CasperMessage__pb2.ListeningNameContinuationResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'coop.rchain.casper.protocol.DeployService', rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
