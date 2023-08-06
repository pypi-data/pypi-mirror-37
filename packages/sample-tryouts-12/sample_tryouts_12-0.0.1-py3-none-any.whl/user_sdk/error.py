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

class UserAuthenticationError(ClientError):
    pass

class UserCreationFailed(ClientError):
    pass
