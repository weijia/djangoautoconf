

class UserInactive(Exception):
    pass


class InvalidLogin(Exception):
    pass


class NoLoginInfo(Exception):
    pass


class AccessTokenExpire(Exception):
    pass


class AccessTokenNotExist(Exception):
    pass


class InvalidEmailAddress(Exception):
    pass