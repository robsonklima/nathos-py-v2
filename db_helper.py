import pymysql


class DBHelper:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = "root"
        self.db = "nhatos_v3"

    def __connect__(self):
        try:
            self.con = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                       db=self.db, cursorclass=pymysql.cursors.DictCursor)
            self.cur = self.con.cursor()
        except pymysql.MySQLError as ex:
            print(ex)

    def __disconnect__(self):
        try:
            self.con.close()
        except pymysql.MySQLError as ex:
            print(ex, sql)

    def fetch(self, sql):
        try:
            self.__connect__()
            self.cur.execute(sql)
            result = self.cur.fetchall()
            self.__disconnect__()

            return result
        except pymysql.MySQLError as ex:
            print(ex, sql)

    def execute(self, sql):
        try:
            self.__connect__()
            self.cur.execute(sql)
            self.con.commit()
            self.__disconnect__()
        except pymysql.MySQLError as ex:
            print(ex, sql)