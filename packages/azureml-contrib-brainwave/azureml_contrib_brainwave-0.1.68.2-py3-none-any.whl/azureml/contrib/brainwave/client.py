# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Score on deployed Project Brainwave webservices.
"""
import tensorflow as tf
import grpc
import time
from datetime import datetime, timedelta


try:
    from tensorflow_serving.apis import predict_pb2
    from tensorflow_serving.apis import prediction_service_pb2_grpc
except ImportError:
    from .external.tensorflow_serving.apis import predict_pb2
    from .external.tensorflow_serving.apis import prediction_service_pb2_grpc

from tensorflow.core.framework import tensor_shape_pb2
from tensorflow.core.framework import types_pb2


class PredictionClient:
    """
    Scoring client for Realtime AI Services.
    """
    def __init__(self, address: str, port: int, use_ssl: bool = False, access_token: str = "",
                 channel_shutdown_timeout: timedelta = timedelta(minutes=2)):
        """
        Create a prediction client.
        :param address: Address of the service.
        :param port: Port of the service to connect to.
        :param use_ssl: If the client should use SSL to connect.
        :param access_token: Access token key for the webservice.
        :param channel_shutdown_timeout: Timeout after which channel should reconnect.
        """
        if (address is None):
            raise ValueError("address")

        if (port is None):
            raise ValueError("port")

        host = "{0}:{1}".format(address, port)
        metadata_transormer = (lambda x: [('authorization', access_token)])
        grpc.composite_channel_credentials(grpc.ssl_channel_credentials(),
                                           grpc.metadata_call_credentials(metadata_transormer))

        if use_ssl:
            self._channel_func = lambda: grpc.secure_channel(host, grpc.ssl_channel_credentials())
        else:
            self._channel_func = lambda: grpc.insecure_channel(host)

        self.__channel_shutdown_timeout = channel_shutdown_timeout
        self.__channel_usable_until = None
        self.__channel = None

    def score_numpy_array(self, npdata):
        """
        Score a numpy array.
        :param npdata: Numpy array to score

        :return:
        """
        request = predict_pb2.PredictRequest()
        request.inputs['images'].CopyFrom(tf.contrib.util.make_tensor_proto(npdata, types_pb2.DT_FLOAT, npdata.shape))
        result_tensor = self.__predict(request, 30.0)
        return tf.contrib.util.make_ndarray(result_tensor)

    def score_image(self, path: str, timeout: float = 10.0):
        """
        Score an image file
        :param path: Path of the image to score.
        :param timeout: Timeout in seconds.
        :return: The result of the prediction, as a numpy array.
        """
        with open(path, 'rb') as f:
            data = f.read()
            return self.score_file(data, timeout)

    def score_file(self, data, timeout=10.0):
        """
        Score the data, like an image.

        with open('test.jpg','rb') as f:
            result = client.score_file(f.read())
        print(result)

        :param data: bytes to score
        :param timeout: timeout in seconds
        :return: The result of the prediction, as a numpy array.
        """
        result = self.score_tensor(data, [1], types_pb2.DT_STRING, timeout)  # 7 is dt_string
        result_ndarray = tf.contrib.util.make_ndarray(result)
        # result is a batch, but the API only allows a single image so we return the
        # single item of the batch here
        return result_ndarray[0]

    @staticmethod
    def _make_dim_list(shape: list):
        ret_list = []
        for val in shape:
            dim = tensor_shape_pb2.TensorShapeProto.Dim()
            dim.size = val
            ret_list.append(dim)
        return ret_list

    def score_tensor(self, data: bytes, shape: list, datatype, timeout: float = 10.0):
        """
        Score a tensor.
        :param data: Bytes to score.
        :param data: bytes
        :param shape: Shape of the tensor to score.
        :type shape: list[int]
        :param datatype: Datatype of the tensor to score.
        :param timeout: Timeout of the request in seconds
        :return: Tensor with the predicted values.
        """
        request = predict_pb2.PredictRequest()
        request.inputs['images'].string_val.append(data)
        request.inputs['images'].dtype = datatype
        request.inputs['images'].tensor_shape.dim.extend(self._make_dim_list(shape))
        return self.__predict(request, timeout)

    def _get_datetime_now(self):
        return datetime.now()

    def _get_grpc_stub(self):
        if self.__channel_usable_until is None or self.__channel_usable_until < self._get_datetime_now():
            self.__reinitialize_channel()
        self.__channel_usable_until = self._get_datetime_now() + self.__channel_shutdown_timeout
        return self.__stub

    def __predict(self, request, timeout):
        retry_count = 5
        sleep_delay = 1

        while True:
            try:
                result = self._get_grpc_stub().Predict(request, timeout)

                return result.outputs["output_alias"]
            except grpc.RpcError as rpcError:
                retry_count = retry_count - 1
                if (retry_count <= 0):
                    raise
                time.sleep(sleep_delay)
                sleep_delay = sleep_delay * 2
                print("Retrying", rpcError)
                self.__reinitialize_channel()

    def __reinitialize_channel(self):
        self.__stub = None
        if self.__channel is not None:
            self.__channel.close()
        self.__channel = self._channel_func()
        self.__stub = prediction_service_pb2_grpc.PredictionServiceStub(self.__channel)
