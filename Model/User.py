
class User:
    def __init__(self, name, account, password, uuid=None, level=1, chk_email=0, timestamp=0):
        self.uuid = uuid
        self.name = name
        self.account = account
        self.password = password
        self.level = level
        self.chk_email = chk_email
        self.timestamp = timestamp
