from Interface_code_OOP import *
import sqlite3
from contextlib import closing
import time


class DBConnector:
    def __init__(self, obj_):
        self.interface = obj_
        self.db_name = self.interface.db_name
        self.db_table_name = self.interface.db_table_name
        self.conn = None
        self.curs_ = None

    @property
    def db_name(self):
        return self._db_name

    @db_name.setter
    def db_name(self, value: str):
        if value[-3:] != '.db':
            value += '.db'
        self._db_name = value
        self.interface.db_name = value

    @property
    def db_table_name(self):
        return self._db_table_name

    @db_table_name.setter
    def db_table_name(self, value: str):
        self._db_table_name = value
        self.interface.db_table_name = value

    def connect_to_the_db(self):
        with closing(sqlite3.connect(self.db_name)) as self.conn:
            self.curs_ = self.conn.cursor()
            self.curs_.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.db_table_name} (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    BookName TEXT,
                    BookAuthor TEXT,
                    BookYear INTEGER,
                    BookDesc TEXT);
            """)
            self.check_table()

    def check_table(self):
        try:
            self.curs_.execute(f"SELECT ID, BookName, BookAuthor, BookYear, BookDesc FROM {self.db_table_name};")
            if self.conn:
                self.interface.log += f'''database {self.db_name} with table {self.db_table_name} 
are ready on {time.asctime}\n'''
                self.interface.pop_up("database connected", self.interface)
        except sqlite3.OperationalError:
            self.db_table_name = ''
            self.interface.pop_up("Not all required columns exists in the table in database", self.interface)

    def read_db(self, nm: str, auth: str, yr: int, desc: str):
        nm = nm if nm != '' else '%'
        auth = auth if auth != '' else '%'
        yr = yr if yr != '' else '%'
        desc = desc if desc != '' else '%'
        with closing(sqlite3.connect(self.db_name)) as self.conn:
            self.curs_ = self.conn.cursor()
            result = list(self.curs_.execute(f"""SELECT ID, BookName, BookAuthor, BookYear, BookDesc
                                FROM {self.db_table_name}
                                WHERE BookName LIKE '{nm}'
                                AND BookAuthor LIKE '{auth}'
                                AND BookYear LIKE '{yr}'
                                AND BookDesc LIKE '{desc}';"""))
            self.interface.log += f'data got from the db on {time.asctime}\n'

        return result

    def append_to_db(self, nm: str, auth: str, yr: int, desc: str):
        """
        appends to the database
        :param nm: name to add
        :param auth: author to add
        :param yr: year to add
        :param desc: description to add
        :return: None
        """
        query_string = self.construct_sql_sting(nm=nm, auth=auth, yr=yr, desc=desc, type=0)
        self.change_db(query_string)
        self.interface.log += f'data appended to the db on {time.asctime}\n'

    def change_entry(self, nm: str, auth: str, yr: int, desc: str, id_: int):
        """
        changes entry in database
        :param nm: name to change
        :param auth: author to change
        :param yr: year to change
        :param desc: description to change
        :param id_: id of the record
        :return: None
        """
        query_string = self.construct_sql_sting(nm=nm, auth=auth, yr=yr, desc=desc, type=1, ID_to_change=id_)
        self.change_db(query_string)
        self.interface.log += f'data changed in the db on {time.asctime}\n'

    def remove_entry(self, id_: int):
        """
        rmove the entry from database
        :param id_: Id to remove
        :return: None
        """
        query_string = self.construct_sql_sting(type=1, ID_to_change=id_)
        self.change_db(query_string)
        self.interface.log += f'data removed from the db on {time.asctime}\n'

    def construct_sql_sting(self,
                            nm=None, auth=None, yr=None, desc=None, type=None, ID_to_change=None):
        """
        construct the query for an update method
        :param nm: name
        :param auth: author
        :param yr: year
        :param desc: deescription
        :param type: type of operation: 0 - append, 1 - change, 2 - remove
        :param ID_to_change: Id to search in database
        :return: query string
        """
        result = ""
        # Add New
        if type == 0:
            result = f"""INSERT INTO {self.db_table_name}(
                                                BookName,
                                                BookAuthor,
                                                BookYear,
                                                BookDesc)
                                            VALUES ('{nm}', '{auth}', {yr}, '{desc}');"""
        # change existing one
        elif type == 1:
            result = f"""
                    UPDATE {self.db_table_name}
                    SET BookName = '{nm}', 
                        BookAuthor = '{auth}',
                        BookYear = '{yr}',
                        BookDesc = '{desc}'
                    WHERE ID = {ID_to_change};"""
        # remove
        elif type == 2:
            result = f"""
                    DELETE FROM {self.db_table_name}
                    WHERE ID = {ID_to_change};"""
        return result

    def change_db(self, sql_: str):
        """
        updates the database
        :param sql_: query string to execute
        :return: None
        """
        with closing(sqlite3.connect(self.db_name)) as self.conn:
            self.curs_ = self.conn.cursor()
            self.curs_.execute(sql_)
            self.conn.commit()
