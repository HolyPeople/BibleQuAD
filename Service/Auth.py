from Model.User import User
from Model.UserDAO import UserDAO
import pymysql
import bcrypt


def __login(account, password, is_name=True):
    try:
        dao = UserDAO()
        user = None
        if is_name:
            user = dao.readUserByName(account)
        else:
            user = dao.readUserByAccount(account)
        if user is None:
            return None
        else:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return user
            else:
                return None
    except pymysql.Error as e:
        pass
    return None


def loginByEmail(account, password):
    return __login(account, password, False)


def loginByUserName(account, password):
    return __login(account, password)


def register(name, account, password):
    try:
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
        user = User(name, account, password)
        dao = UserDAO()
        dao.createUser(user)
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            return 'Duplicate entry'
    return "SUCCESS"


def is_exist(name=None, account=None):
    dao = UserDAO()
    if name is not None:
        user = dao.readUserByName(name)
        if user:
            return True
    elif account is not None:
        user = dao.readUserByAccount(account)
        if user:
            return True
    else:
        raise Exception(9999, "NO KEY")
    return False

