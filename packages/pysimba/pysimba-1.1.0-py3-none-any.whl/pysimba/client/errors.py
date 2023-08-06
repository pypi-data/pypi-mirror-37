class ClientError(Exception):
    pass


class TryAgain(ClientError):
    pass
