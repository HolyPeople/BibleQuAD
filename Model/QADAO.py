import pymysql
import uuid
import datetime
from Model.QA import QA


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
    def createQA(self, qa):
        sql = ("INSERT INTO " +
               "qa(bible_id, question, answer, uuid) " +
               "VALUES " +
               "(%s, %s, %s, %s)")
        self.cursor.execute(sql, (qa.bible_id,
                                  qa.question,
                                  qa.answer,
                                  qa.uuid
                                  )
                            )
        self.conn.commit()

    # Read User
    def readAnswerByQuestion(self, question):
        return self.readAnswer('question', question)

    def readAnswerBybible(self, bible_id):
        return self.readAnswer('bible_id', bible_id)

    def readAnswer(self, key, value):
        sql = "SELECT * from user WHERE {0}=%s".format(key)
        execute_result = self.cursor.execute(sql, value)
        result = self.cursor.fetchone()
        qa = None
        if execute_result != 0:
            qa = QA(result[0], result[1], result[2], result[3])
            print(qa.question, qa.answer)
        else:
            return None
        return qa

    # Update User
    def updateAnswer(self, user):

        pass

    # Delete User
    def deleteAnswer(self, bible_id, question):
        sql = "DELETE FROM user WHERE {0}='{1}'".format(bible_id, question)
        self.cursor.execute(sql)
        self.conn.commit()
