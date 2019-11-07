import pymysql
import uuid
import datetime
from Model.User import User


class UserDAO:
    def __init__(self):
        try:
            self.configure = {}
            with open('database.conf') as conf:
                lines = conf.readlines()
                for line in lines:
                    tmp = line.split('=')
                    key = tmp[0]
                    value = tmp[1][:-1]
                    self.configure[key] = value
            try:
                self.conn = pymysql.connect(host=self.configure['host'],
                                            port=int(self.configure['port']),
                                            user=self.configure['user'],
                                            passwd=self.configure['passwd'],
                                            db=self.configure['db'],
                                            charset=self.configure['charset'],
                                            )
                self.cursor = self.conn.cursor()
            except pymysql.MySQLError as e:
                print(e)
            pass
        except FileNotFoundError as e:
            print(e)

    # Create User
    def createUser(self, user):
        user_uuid = uuid.uuid4().hex
        sql = ("INSERT INTO " +
               "user(uuid, name, account, passwd, level, chk_email, timestamp) " +
               "VALUES " +
               "({0}, {1}, {2}, {3}, {4}, {5}, {6})".format(
                   "'" + user_uuid + "'",
                   "'" + user.name + "'",
                   "'" + user.account + "'",
                   "'" + user.password + "'",
                   user.level,
                   user.chk_email,
                   int(datetime.datetime.now().timestamp()))
               )
        self.cursor.execute(sql)

        self.conn.commit()

    # Read User
    def readUserByAccount(self, account):
        return self.readUser('account', account)

    def readUserByUUID(self, _uuid):
        return self.readUser('uuid', _uuid)

    def readUser(self, key, value):
        sql = "SELECT * from user WHERE {0}='{1}'".format(key, value)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        user = None
        if results:
            user = User(results[0][0], results[0][1], results[0][2],
                        results[0][3], results[0][4], results[0][5], results[0][6])
        return user

    # Update User
    def updateUser(self, user):
        pass

    # Delete User
    def deleteUser(self, key, value):
        sql = "DELETE FROM user WHERE {0}='{1}'".format(key, value)
        self.cursor.execute(sql)
        self.conn.commit()

    def deleteUserByAccount(self, account):
        self.deleteUser('account', account)

    def deleteUserByUUID(self, _uuid):
        self.deleteUser('uuid', _uuid)
