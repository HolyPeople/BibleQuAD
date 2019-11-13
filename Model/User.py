
class User:
    def __init__(self, name, account, password, uuid=None, level=1, chk_email=0, created_at=0, updated_at=0):
        self.uuid = uuid
        self.name = name
        self.account = account
        self.password = password
        self.level = level
        self.chk_email = chk_email
        self.created_at = created_at
        self.updated_at = updated_at
