from Model.QA import QA
from Model.QADAO import QADAO
import pymysql


def submitQA(qa, user_id):
    # uuid, paragraph_id, question, answers, user_id, is_impossible=0, created_at=None
    qa_obj = QA(qa['paragraph_id'], qa['question'], qa['answers'], user_id, qa['is_impossible'])
    print(qa['paragraph_id'], user_id)
    dao = QADAO()
    try:
        dao.createQA(qa_obj)
        return {'result': True}
    except pymysql.MySQLError as e:
        return {'result': False}


def getQA():
    return
