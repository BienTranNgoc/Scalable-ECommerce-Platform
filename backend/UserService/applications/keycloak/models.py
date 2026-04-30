class KeycloakToken:
    client_id: str = None
    response_type: str = None
    grant_type: str = None
    scope: str = None

    def __init__(self, client_id: str = None, response_type: str = "access_token", grant_type: str = "password", scope: str = "openid email", **kwargs):
        self.client_id = client_id
        self.response_type = response_type
        self.grant_type = grant_type
        self.scope = scope
        self.__dict__.update(kwargs)


class DirectAccessGrant(KeycloakToken):
    username: str = None
    password: str = None
    client_secret: str = None
    audience: str = None
    device_id: str = None

    def __init__(self, username: str = None, password: str = None, client_secret: str = None, audience: str = None, device_id: str = None, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.password = password
        self.client_secret = client_secret
        self.audience = audience
        self.device_id = device_id
        self.__dict__.update(kwargs)


class KeycloaKResetPassword:
    temporary: bool = False
    type: str = "password"
    value: str = None

    def __init__(self, temporary: bool = False, type: str = None, value: str = None, **kwargs):
        self.temporary = temporary
        self.type = type
        self.value = value
        self.__dict__.update(kwargs)


class KeycloaKLogout:
    client_id: str = None
    refresh_token: str = None

    def __init__(self, client_id: str = None, refresh_token: str = None, **kwargs):
        self.client_id = client_id
        self.refresh_token = refresh_token
        self.__dict__.update(kwargs)
