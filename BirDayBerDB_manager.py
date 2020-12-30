import sqlite3


class Birthdays_db:
    def __init__(self, connection):
        #  Preparation of the DB
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    def close_database(self):
        self.connection.close()

    def create_table(self, tables):
        for table in tables.items():
            self.cursor.executemany("CREATE TABLE ? (?);", table)

    def add_person(name, surname, country, gender, birth, photo):
        """
        Table attributes:
        NOT NULL: {name, country, gender, birth}
        NULLABLE: {surname, photo}
        """

        # sql_query = """
        # INSERT ...
        # """

        # self.cursor.executemany()
        pass
