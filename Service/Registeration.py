import sys

from Model.User import User
from Model.UserDAO import UserDAO
import traceback
import pymysql


def register(name, account, password):
    try:
        user = User(name, account, password)
        dao = UserDAO()
        dao.createUser(user)
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            return "ERROR=1062"
        print(e.args[0])
    return "SUCCESS"
