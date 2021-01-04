import sqlite3


def get_dict(key_or_value, position=0):
    """
    Function to get the key or value from a dictionary in its own data type
    """
    return tuple(key_or_value)[position]


class Db_manager:
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

        DB_manager().create_table({'photo': f'id_photo {id_type} photo BLOB',
        "country": f'id_country {id_type}, country VARCHAR(40)'})
        """
        for table in tables.items():
            self.cursor.executemany("CREATE TABLE ? (?);", table)

    def add_attributes(self, *rows):
        """ Insertion of rows to the table:
        To insert data, you have to especify the table with his columns
        and data of the row in a dictionary.

        Example:

            DB_manager().add_attributes({
                "country": {"country": "United States"},
                "person": {"per_first": "Randolph", "per_last": "Carter"}})
        """
        rows = rows[0]
        columns = []

        for index, (k, v) in enumerate(rows.items()):
            columns.append(None)

            for length in range(len(v)):
                if columns[index] is None:
                    columns[index] = [
                        k, [get_dict(v.keys(), length)],
                        [get_dict(v.values(), length)]]

                elif columns[index] is not None:
                    columns[index][1].append(get_dict(v.keys(), length))
                    columns[index][2].append(get_dict(v.values(), length))

        return self.process_attributes(columns)
