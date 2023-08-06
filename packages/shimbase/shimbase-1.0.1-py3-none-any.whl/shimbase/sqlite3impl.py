from sqlite3 import connect, IntegrityError
from dbimpl import DatabaseDataError, DatabaseIntegrityError, DatabaseImpl

class SQLite3Impl(DatabaseImpl):
    '''
    SQLite3 implementation class to be used with the generic Database class
    '''
    def connect(self, dbname:str):
        '''
        Connect to the named db

        :param dbname: the full path to the database file
        '''
        self._dbname = dbname
        self._conn = connect(dbname)

    def select(self, table:str, where:dict = None):
        '''
        Select from db the row(s) matching the provided fields or all rows if
        fields are None

        :param table: the table name to select from
        :param where: a dictionary of where clauses, k=v and k1=v1...
        :returns: a list of rows from table
        :raises: None
        '''
        s = 'SELECT * FROM {} '.format(table)
        if where and len(where) > 0:
            s += 'WHERE '
            for k, v in where.items():
                if v is None:
                    s += '{}=NULL and '.format(k)
                elif isinstance(v, str):
                    s += '{}="{}" and '.format(k, v) 
                else:
                    s += '{}={} and '.format(k, v) 
            # remove the extraneous ' and '
            s = s[:-5]
   
        return self.execute(s)

    def insert(self, table:str, inserts:dict):
        '''
        Insert the given data into the database

        :param table: the table name to insert into
        :param inserts: a dictionary of key value pairs to be inserted
        :raises: DatabaseDataError if no inserts
        '''
        if inserts is None or len(inserts) == 0:
            raise DatabaseDataError('No values provided for INSERT')
    
        s = 'INSERT INTO {} ('.format(table)
        for k in inserts.keys():
            s += '{},'.format(k) 
        # remove the extraneous comma
        s = s[:-1]

        s += ') values ('
        for v in inserts.values():
            if v is None:
                s += 'NULL,'
            elif isinstance(v, str):
                s += '"{}",'.format(v)
            else:
                s += '{},'.format(v)
        # remove the extraneous comma
        s = s[:-1]
        s += ')'

        self.execute(s)

    def update(self, table:str, updates:dict, where:dict = None):
        '''
        Update the fields whose row(s) are identified by the where dict

        :param table: the table name to update
        :param updates: a dictionary of key value pairs to be updated
        :param where: a dictionary of where clauses, k=v and k1=v1...
        :raises: DatabaseDataError if no updates
        '''
        print(updates)
        print(where)
        if updates is None or len(updates) == 0:
            raise DatabaseDataError('No values provided for UPDATE')
        
        s = 'UPDATE {} SET '.format(table)
        for k, v in updates.items():
            if v is None:
                s += '{}=NULL,'.format(k)
            elif isinstance(v, str):
                s += '{}="{}",'.format(k, v) 
            else:
                s += '{}={},'.format(k, v) 
        # remove the extraneous comma
        s = s[:-1]

        if where and len(where) > 0:
            s += ' WHERE '
            for k, v in where.items():
                if v is None:
                    s += '{}=NULL and '.format(k)
                elif isinstance(v, str):
                    s += '{}="{}" and '.format(k, v) 
                else:
                    s += '{}={} and '.format(k, v) 
            # remove the extraneous ' and '
            s = s[:-5]
        else:
            raise DatabaseDataError('No keys provided for UPDATE')

        self.execute(s)

    def delete(self, table:str, where:dict = None):
        '''
        Delete the row(s) identified by the where dict

        :param table: the table name to delete from
        :param where: a dictionary of where clauses, k=v and k1=v1...
        '''
        s = 'DELETE FROM {} '.format(table)
        if where and len(where) > 0:
            s += 'WHERE '
            for k, v in where.items():
                if v is None:
                    s += '{}=NULL and '.format(k, v) 
                elif isinstance(v, str):
                    s += '{}="{}" and '.format(k, v) 
                else:
                    s += '{}={} and '.format(k, v) 
            # remove the extraneous ' and '
            s = s[:-5]
        else:
            raise DatabaseDataError('No keys provided for DELETE')

        self.execute(s)

    def execute(self, s):
        '''
        Execute the provided SQL string against the underlying DB

        :param s: a SQL string
        :returns: a list of database rows affected, potentially an empty list
        :raises: DatabaseIntegrityError if table constraints are breached
        '''
        curs = self._conn.cursor()

        try:
            #print(s)
            curs.execute(s)
        except IntegrityError as e:
            raise DatabaseIntegrityError(e.args[0])

        rows = curs.fetchall() 
        curs.close()

        return rows

    def begin(self):
        '''
        Begin a database transaction
        '''
        self.execute('begin transaction')

    def commit(self):
        '''
        Commit the active database transaction
        '''
        self._conn.commit()

    def rollback(self):
        '''
        Commit the active database transaction
        '''
        self._conn.rollback()

    def close(self):
        '''
        Close the active database connection
        '''
        self._conn.close()

    def enableForeignKeys(self):
        '''
        Set Foreign Key checks on
        '''
        self.execute('pragma foreign_keys=1')

    def disableForeignKeys(self):
        '''
        Set Foreign Key checks off
        '''
        self.execute('pragma foreign_keys=0')
