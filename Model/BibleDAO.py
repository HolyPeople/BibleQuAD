import pymysql


class BibleDAO:
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
                pass
        except FileNotFoundError as e:
            pass

    def __getVerseID(self, book, chapter, verse):
        get_verse_id_sql = 'SELECT id FROM woori_bible as b ' \
                           'JOIN bible_books_woori AS book ' \
                           'ON b.book = book.book ' \
                           'WHERE book.kor=%s ' \
                           'AND b.chapter=%s ' \
                           'AND b.verse=%s'
        self.cursor.execute(get_verse_id_sql, (book, chapter, verse))
        return self.cursor.fetchone()[0]

    def __getOutline(self, _id):
        get_outline_sql = 'SELECT title, start_id, end_id FROM woori_outlines ' \
                          'WHERE start_id <= {_id} AND end_id >= {_id}'.format(_id=_id)
        self.cursor.execute(get_outline_sql)
        res = self.cursor.fetchone()
        return {'title': res[0],
                'start_id': res[1],
                'end_id': res[2]}

    def getParagraph(self, book, chapter, verse):
        _id = self.__getVerseID(book, chapter, verse)
        outline = self.__getOutline(_id)
        get_paragraph_sql = 'SELECT b.book, book.k_abb, b.chapter, b.verse, b.data FROM woori_bible as b ' \
                            'JOIN bible_books_woori AS book ' \
                            'ON b.book = book.book ' \
                            'WHERE b.id >= %s AND b.id <= %s'
        self.cursor.execute(get_paragraph_sql, (outline['start_id'], outline['end_id']))
        results = self.cursor.fetchall()
        content = results[0][4]
        for result in results[1:]:
            content = content + ' ' + result[4]
        paragraph = {'단락_제목': outline['title'],
                     '단락_내용': content,
                     '시작_장': results[0][2],
                     '성경': results[0][1],
                     '시작_절': results[0][3],
                     '끝_장': results[-1][2],
                     '끝_절': results[-1][3]
                     }
        return paragraph

    def getChapters(self):
        sql = 'SELECT bcw.book, bcw.chapter, bcw.verse_count, bbw.kor, bbw.chapter_count ' \
              'FROM bible_chapters_woori AS bcw ' \
              'JOIN bible_books_woori bbw ON bcw.book = bbw.book'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        data = {'구약': [], '신약': []}
        n_ot = 0
        n_nt = 0
        for result in results:
            if result[1] == 1:
                chapter = {'book': result[3],
                           'chapter': result[4],
                           'verse_counts': [result[2]]
                           }
                if 'O' in result[0]:
                    data['구약'].append(chapter)
                    n_ot = n_ot + 1
                else:
                    data['신약'].append(chapter)
                    n_nt = n_nt + 1
            else:
                if 'O' in result[0]:
                    data['구약'][n_ot - 1]['verse_counts'].append(result[2])
                else:
                    data['신약'][n_nt - 1]['verse_counts'].append(result[2])
        return data

'''
"verse_counts
'''