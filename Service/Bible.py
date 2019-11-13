from Model.BibleDAO import BibleDAO


def getChapter():
    dao = BibleDAO()
    return dao.getChapters()


def getParagraph(book, chapter, verse):
    dao = BibleDAO()
    return dao.getParagraph(book, chapter, verse)
