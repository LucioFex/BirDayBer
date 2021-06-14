import sqlite3
import os


def get_dict(key_or_value, position=0):
    """
    Function to get the key or value from a dictionary in it own data type.
    """
    return tuple(key_or_value)[position]


def photo_to_binary(photo):
    """
    Function that gets the binary data of an image and return it.
    If 'photo' parameter is None, then it returns None.
    But if the 'photo' parameter is a binary object already,
    it will return the 'photo' itself.
    """
    if photo is None:
        return

    try:
        if os.path.exists(photo):
            with open(photo, 'rb') as binary_photo:
                blob = binary_photo.read()
            return blob

        elif not os.path.exists(photo):
            return photo

        raise FileExistsError  # If there's no file found
    except FileNotFoundError:
        return


def binary_to_photo(id_person, binary, folder="bin//rows-content"):
    """
    Function that convert the binary data to an image in a X folder.
    The default folder will be "bin//rows-content"

    Every photo will be saved in '.png' type.
    """
    try:
        with open(f'{folder}//photo_{id_person}.png', 'wb') as photo:
            photo.write(binary)
    except FileNotFoundError:
        return None


def delete_files(*location):
    """
    Function that deletes all the files submitted in the parameters.
    The parameters are unlimited to add locations.

    Example:
    delete_photo("location/1.png", "location/2.png")
    """
    for file in location:
        os.remove(file)


class Db_manager:
    """
    Data base manager.
    """
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()
        self.db_path = connection

    def close_database(self):
        return self.connection.close()

    def create_table(self, tables):
        """ Table insertion:
        This method let you create a table with a dictionary where
        the Key is the table name and the values are the table columns.

        Every Primary Key should be called in the following way:
        id_[table_name]

        Example:

        DB_manager().create_table({
            'photo': f'id_photo INTEGER PRIMARY KEY AUTOINCREMENT, photo BLOB',
            "country": f'id_country {id_type}, country VARCHAR(40)'})
        """
        for table in tables.items():
            self.cursor.execute("CREATE TABLE %s (%s)" % (table[0], table[1]))
        self.connection.commit()

    def add_rows(self, rows):
        """ Insertion of rows to the table:
        To insert data, you have to especify the table with his columns
        and data of the row in a dictionary.

        Every column that ends with the name '_fk' will be aumatically taken
        as a foreign column, and it will be given an automated ID.
        You shouldn't input the foreign keys by yourself.

        Also every column that has a Blob type will be automatically checked
        to convert it to 'bytes' data type.

        Example:
            DB_manager().add_rows({
                "country": {"country": "United States"},
                "person": {"per_first": "Randolph", "per_last": "Carter"}})
        """
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

        return self.process_rows(columns)

    def process_rows(self, data):
        """
        This method tells the DB to INSERT the data in the tables of the DB.

        data[x][0] = Table Names,
        data[x][1] = Column names,
        data[x][2] = Row values
        """
        for element in data:
            self.cursor.execute("PRAGMA table_info(%s);" % element[0])
            for column in self.cursor.fetchall():
                if column[1][-3:] == "_fk":
                    element[1] = element[1] + ", " + column[1]
                    element[2].append(self.cursor.lastrowid)

                if column[2] == "BLOB":
                    for index in range(len(element[2])):
                        element[2][index] = photo_to_binary(element[2][index])

            #  Insertion of data
            values = ("?," * len(element[2]))[0:-1]  # Example: [a, b] == "?,?"
            self.cursor.execute(f"""INSERT INTO {element[0]} ({element[1]})
                VALUES ({values})""", element[2])

        self.connection.commit()

    def remove_rows(self, table, where):
        """
        This method allows you to delete rows from a table.

        First Parameter: Table name.
        Second Parameter: WHERE clause.

        Special Parameters:
        If you write "&deleteAll", then there'll be no "WHERE clause".
        """
        sql_query = "DELETE FROM " + table

        if where != "&deleteAll":
            sql_query = sql_query + " WHERE " + where
        deleted = "%s rows deleted" % self.cursor.execute(sql_query).rowcount

        self.connection.commit()
        return deleted

    def column_search(self, table, columns="*", joins="", where="&None%"):
        """
        This is a method that allows you select a table, columns, prepare joins
        clauses and a where clause to get the values of the table columns/s.

        First Parameter: Table Name:
        Example --> "country" or "person".

        Second Parameter: Columns Name/s:
        Example --> "per_last" or "age" or "*" or "per_last, per_first, age".

        Third Parameter: Join Clause:
        Example --> "inner join gender on gender.id_gender = person.id_person"

        Fourth Parameter: Where condition:
        Example --> "per_last != 'randolph'" or "age >= 18".


        Special Parameters:
        You can see all columns if in the second parameter
        you write "*" or nothing in it.

        If you don't want to make use a Join Clause, you can simply avoid it,
        or write in the third parameter "".

        Also, you can avoid the where clause if in the fourth
        parameter you write "&None%" or nothing in it.
        """
        sql_query = "SELECT %s FROM %s %s" % (columns, table, joins)

        if where != "&None%":
            sql_query = sql_query + " WHERE " + where
        self.cursor.execute(sql_query)

        return tuple(self.cursor.fetchall())

    def drop_database(self):
        """
        Elimination of the database.
        """
        os.remove(self.db_path)
