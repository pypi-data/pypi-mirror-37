class ClientError(Exception):
    pass

class NoSuchUser(ClientError):
    pass

class NoSuchProfile(ClientError):
    pass

class ProfileCreationError(ClientError):
    pass

class ProfileUpdateError(ClientError):
    pass

class UserAlreadyExist(ClientError):
    pass


class ServerError(Exception):
    pass

class OtpGenerationFailed(ServerError):
    pass

class UserCreationFailed(ServerError):
    pass

class UserAuthenticationError(ServerError):
    pass