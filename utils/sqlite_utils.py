import sqlite3

from utils.logger import logger


class SQLiteUtils:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(SQLiteUtils, cls).__new__(cls)
        return cls.__instance

    def __init__(self, db_name="kms.db"):
        self.__db_name = db_name
        self.__conn = None
        self.__cursor = None

    def get_conn(self):
        self.__conn = self.__conn if self.__conn else sqlite3.connect(self.__db_name)
        return self.__conn

    def get_cursor(self, conn=None):
        if conn is None:
            self.__conn = self.get_conn()
        cursor = self.__cursor if self.__cursor else self.__conn.cursor()
        return cursor

    def get_db_name(self):
        return self.__db_name


sqlite = SQLiteUtils()
conn, cursor = sqlite.get_conn(), sqlite.get_cursor()
if cursor:
    logger.success(f"Connected to {sqlite.get_db_name()}")

if __name__ == "__main__":
    ...
