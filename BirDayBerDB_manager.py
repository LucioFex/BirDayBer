import sqlite3


def get_dict(key_or_value, position=0):
    """
    Function to get the key or value from a dictionary in its own data type
    """
    return tuple(key_or_value)[position]


class Birthdays_db:
    def __init__(self, connection):
        """
        Preparation of the DB
        """
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    def close_database(self):
        """
        Finish DataBase connection
        """
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
        and data of the row in a dictionary.

        Example:

        Input:

            Birthdays_db().add_person({
                "country": {"country": "United States"},
                "person":  {"per_first": "Randolph", "per_last": "Carter"}})

        Result:

            sqlite3.connection.cursor("INSERT INTO Country
                (country) VALUES ("United States"))

            sqlite3.connection.cursor("INSERT INTO person
                (per_first, per_last) VALUES ("Randolph", "Carter")")
        """

        rows = rows[0]
        query = "INSERT INTO ? (?) VALUES (?)"

        for table, value in rows.items():
            for length in len(value):
                self.cursor.executemany(
                    query, table, get_dict(value.values(), length))
