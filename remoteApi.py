class RemoteAPIObject:
    def __init__(self, client, objectName):
        self._client = client
        self._objectName = objectName

    def __getattr__(self, attrName):
        def func(*args, **kwargs):
            packedArgs = self._client._pack(args)
            [retArgs] = self._client._call(self._objectName + '.' + attrName, packedArgs)
            return self._client._unpack(retArgs)
        return func
