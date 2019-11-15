import pymysql
import uuid
import datetime
from Model.QA import QA


class QADAO:
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
        answers_id = uuid.uuid4().hex
        sql = "INSERT INTO " \
              "qas(paragraph_id, question, is_impossible, answers, user_id) " \
              "VALUES " \
              "(%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (qa.paragraph_id,
                                  qa.question,
                                  qa.is_impossible,
                                  answers_id,
                                  qa.user_id,
                                  )
                            )
        self.conn.commit()

        sql = "INSERT INTO " \
              "answers(id, text, answer_start) " \
              "VALUES " \
              "(%s, %s, %s)"
        for answer in qa.answers:
            self.cursor.execute(sql, (answers_id, answer['text'], answer['answer_start']))
            self.conn.commit()

    def __readAnswersByID(self, answers_id):
        answers = []
        sql = 'SELECT * FROM answers WHERE id=' + answers_id
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for result in results:
            answers.append({'text': result[1], 'answer_start': result[2]})
        return answers

    def readQAByParagraphID(self, p_id):
        qas = []
        sql = 'SELECT * FROM qas WHERE paragraph_id=' + p_id + ' ORDER BY id DESC LIMIT 5'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for result in results:
            qas.append(QA(result[0], result[1], result[2], result[4], result[5]))

        for qa in qas:
            qa.answers = self.__readAnswersByID(qa.answers)

        return qas
