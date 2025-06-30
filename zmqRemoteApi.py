import zmq
import msgpack
import msgpack_numpy

msgpack_numpy.patch()

class RemoteAPIClient:
    def __init__(self, ip='127.0.0.1', port=23000):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect(f"tcp://{ip}:{port}")

    def _pack(self, data):
        return msgpack.packb(data, use_bin_type=True)

    def _unpack(self, data):
        return msgpack.unpackb(data, raw=False)

    def _call(self, func, packedArgs):
        self._socket.send_multipart([func.encode('utf-8'), packedArgs])
        response = self._socket.recv_multipart()
        return [self._unpack(r) for r in response]

    def getObject(self, objectName):
        from remoteApi import RemoteAPIObject
        return RemoteAPIObject(self, objectName)
