import sqlite3


class Birthdays_db:
    def __init__(self, connection):
        #  Preparation of the DB
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    def close_database(self):
        #  Finish DataBase connection
        self.connection.close()

    def create_table(self, tables):
        """ Table insertion:
        This method let you create a table with dictionary where
        the Key is the table name and the values are the table columns.

        Example:

        Birthdays_db().create_table({'photo': f'id_photo {id_type} photo BLOB',
        "country": f'id_country {id_type}, country VARCHAR(40)'})
        """
        for table in tables.items():
            self.cursor.executemany("CREATE TABLE ? (?);", table)

    def add_person(self, *rows):
        """ Insertion of rows to the table:
        To insert data, you have to especify the table with his columns
        and data of the row.

        Example:

        Birthdays_db().add_person({"country": {"country", "United States"}},
        "person": {"per_first": "Randolph", "per_last": "Carter"}})
        """

        # Continue with this: ----------------------------------------------------

        # self.cursor.execute("PRAGMA tabla_info(?)", table_name) ...
        # all_columns = [] ...
        # for table in ...

        # if len(rows) > all_columns:
        #     raise TypeError(
        #         "Tried to introduce %d columns when total\n" % (len(rows)) +
        #         "columns of the %s table is of %d" % (table_name, all_columns))

        self.cursor.executemany()
