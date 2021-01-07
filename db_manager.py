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
        return self.connection.close()

    def create_table(self, tables):
        """ Table insertion:
        This method let you create a table with dictionary where
        the Key is the table name and the values are the table columns.

        Example:

        DB_manager().create_table({'photo': f'id_photo {id_type} photo BLOB',
        "country": f'id_country {id_type}, country VARCHAR(40)'})
        """
        for table in tables.items():
            self.cursor.execute(f"CREATE TABLE {table[0]} ({table[1]});")

    def add_rows(self, *rows):
        """ Insertion of rows to the table:
        To insert data, you have to especify the table with his columns
        and data of the row in a dictionary.

        Example:

            DB_manager().add_rows({
                "country": {"country": "United States"},
                "person": {"per_first": "Randolph", "per_last": "Carter"}})
        """
        rows = rows[0]
        columns = []

        for index, (k, v) in enumerate(rows.items()):  # k = keys | v = values
            columns.append(None)

            for length in range(len(v)):
                if columns[index] is None:
                    columns[index] = [
                        k, get_dict(v.keys(), length),
                        [get_dict(v.values(), length)]]

                elif columns[index] is not None:
                    columns[index][1] = (
                        columns[index][1] + ", " +
                        get_dict(v.keys(), length))
                    columns[index][2].append(get_dict(v.values(), length))

        for index in range(len(columns)):
            columns[index] = tuple(columns[index])

        return self.process_rows(columns)

    def process_rows(self, data):
        """
        This method tells the DB to INSERT the data in the tables of the DB.

        data[x][0] = Table Names,
        data[x][1] = Column names,
        data[x][2] = Row values
        """

        for column in data:
            values = ("?," * len(column[2]))[0:-1]  # Example: [a, b] == "?, ?"
            self.cursor.execute(f"""INSERT INTO {column[0]} ({column[1]})
                VALUES ({values})""", column[2])

    def column_search(self, table, column="*", where="&None%"):
        """
        This is a method that allows you select a table, a column and
        a where clause to get the values of the table column/s.

        First Parameter: Table Name:
        Example --> "country" or "person".

        Second Parameter: Column Name/s:
        Example --> "per_last" or "age" or "*".

        Third Parameter: Where condition:
        Example --> "per_last != 'randolph'" or "age >= 18".

        Special Parameters:

        You can see all columns if in the second parameter
        you write "*" or nothing in it.

        Olso, you avoid the where clause if in the third parameter
        you write "&None%" or nothing in it.
        """
        sql_query = "SELECT %s FROM %s;" % (column, table)

        if where != "&None%":
            sql_query = sql_query.replace(";", "WHERE %s" % where)

        self.cursor.execute(sql_query)
        search = self.cursor.fetchall()

        return search
