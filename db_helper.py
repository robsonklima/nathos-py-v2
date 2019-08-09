import pymysql


class DBHelper:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = "root"
        self.db = "nhatos_v2"

    def __connect__(self):
        try:
            self.con = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                       db=self.db, cursorclass=pymysql.cursors.DictCursor)
            self.cur = self.con.cursor()
        except MySQLError as ex:
            print(ex)

    def __disconnect__(self):
        try:
            self.con.close()
        except MySQLError as ex:
            print(ex)

    def fetch(self, sql):
        try:
            self.__connect__()
            self.cur.execute(sql)
            result = self.cur.fetchall()
            self.__disconnect__()

            return result
        except MySQLError as ex:
            print(ex)

    def execute(self, sql):
        try:
            self.__connect__()
            self.cur.execute(sql)
            self.con.commit()
            self.__disconnect__()
        except MySQLError as ex:
            print(ex)