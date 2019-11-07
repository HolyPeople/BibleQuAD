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
               "(%s, %s, %s, %s, %s, %s, %s)")
        self.cursor.execute(sql, (user_uuid,
                                  user.name,
                                  user.account,
                                  user.password,
                                  user.level,
                                  user.chk_email,
                                  int(datetime.datetime.now().timestamp())
                                  )
                            )
        self.conn.commit()

    # Read User
    def readUserByAccount(self, account):
        return self.readUser('account', account)

    def readUserByUUID(self, _uuid):
        return self.readUser('uuid', _uuid)

    def readUser(self, key, value):
        sql = "SELECT * from user WHERE {0}=%s".format(key)
        execute_result = self.cursor.execute(sql, value)
        result = self.cursor.fetchone()
        user = None
        if execute_result != 0:
            user = User(result[1], result[2], result[3], result[0],
                        result[4], result[5], result[6])
            print(user.password, user.account)
        else:
            return None
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
