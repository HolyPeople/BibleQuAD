from Model.BibleDAO import BibleDAO


def getChapter():
    dao = BibleDAO()
    return dao.getChapters()
