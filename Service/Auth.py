from Model.User import User
from Model.UserDAO import UserDAO
import pymysql
import bcrypt


def login(account, password):
    try:
        dao = UserDAO()
        user = dao.readUserByAccount(account)
        if user is None:
            return None
        else:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return user
            else:
                return None
    except pymysql.Error as e:
        print(e)
    return None


def register(name, account, password):
    try:
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
        user = User(name, account, password)
        dao = UserDAO()
        dao.createUser(user)
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            return "ERROR=1062"
        print(e.args[0])
    return "SUCCESS"

