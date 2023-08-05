from mysql.connector import connect, Error
from mysql.connector import errorcode


class Connector:
    """
    Query execution helper methods for the MySQL class.

    Handles opening and closing a connection to a database source, fetching results
    from a query, executing a query and batch executing multiple queries.
    """
    def __init__(self, config, enable_printing):
        self.enable_printing = enable_printing
        self._cursor = None
        self._cnx = None
        self._connect(config)

    def _connect(self, config):
        """Establish a connection with a MySQL database."""
        print('\tMySQL connecting')
        try:
            self._cnx = connect(**config)
            self._cursor = self._cnx.cursor()
            self._printer('\tMySQL DB connection established')
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            raise err

    def _disconnect(self):
        """Destroy connection with MySQL database."""
        self._commit()
        self._close()

    def _printer(self, *msg):
        """Printing method for internal use."""
        if self.enable_printing:
            print(*msg)

    def _close(self):
        """Close MySQL database connection."""
        self._cursor.close()
        self._cnx.close()

    def _commit(self):
        """Commit the changes made during the current connection."""
        self._cnx.commit()

    def _fetch(self, statement, _print=False):
        """Execute a SQL query and return a result."""
        # Execute statement
        self._cursor.execute(statement)
        rows = []
        for row in self._cursor:
            if len(row) == 1:
                rows.append(row[0])
            else:
                rows.append(list(row))
        if _print:
            self._printer('\tMySQL rows successfully queried', len(rows))

        # Return a single item if the list only has one item
        return rows[0] if len(rows) == 1 else rows

    def execute(self, command):
        """Execute a single SQL query without returning a result."""
        self._cursor.execute(command)
        self._commit()

    def executemany(self, command):
        """Execute multiple SQL queries without returning a result."""
        self._cursor.executemany(command)
        self._commit()
