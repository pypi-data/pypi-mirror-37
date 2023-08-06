from abc import ABC, abstractmethod

class DatabaseDataError(Exception):
    '''
    Data provided to the database is in error
    '''
    def __init__(self, msg):
        self.msg = msg

class DatabaseIntegrityError(Exception):
    '''
    A database constraint has been breached
    '''
    def __init__(self, msg):
        self.msg = msg

class DatabaseImpl(ABC):
    '''
    Abstract implementation class to be used with the generic Database class
    '''
    @abstractmethod 
    def connect(self, dbname:str):
        '''
        Connect to the named db

        :param dbname: the full path to the database file
        '''
        pass

    @abstractmethod 
    def select(self, table:str, where:dict = None):
        '''
        Select from db the row(s) matching the provided fields or all rows if
        fields are None

        :param table: the table name to select from
        :param where: a dictionary of where clauses, k=v and k1=v1...
        :returns: a list of rows from table
        '''
        pass

    @abstractmethod 
    def insert(self, table:str, inserts:dict):
        '''
        Insert the given data into the database

        :param table: the table name to insert into
        :param inserts: a dictionary of key value pairs to be inserted
        :raises: DatabaseImplError if no inserts
        '''
        pass

    @abstractmethod 
    def update(self, table:str, updates:dict, where:dict = None):
        '''
        Update the fields whose row(s) are identified by the where dict

        :param table: the table name to update
        :param updates: a dictionary of key value pairs to be updated
        :param where: a dictionary of where clauses, k=v and k1=v1...
        :raises: DatabaseImplError if no updates
        '''
        pass

    @abstractmethod 
    def delete(self, table:str, where:dict = None):
        '''
        Delete the row(s) identified by the where dict

        :param table: the table name to delete from
        :param where: a dictionary of where clauses, k=v and k1=v1...
        '''
        pass

    @abstractmethod 
    def execute(self, s):
        '''
        Execute the provided SQL string against the underlying DB

        :param s: a SQL string
        :returns: a list of database rows affected, potentially an empty list
        :raises: DatabaseIntegrityError if table constraints are breached
        '''
        pass

    @abstractmethod 
    def begin(self):
        '''
        Begin a database transaction
        '''
        pass

    @abstractmethod 
    def commit(self):
        '''
        Commit the active database transaction
        '''
        pass

    @abstractmethod 
    def rollback(self):
        '''
        Commit the active database transaction
        '''
        pass

    @abstractmethod 
    def close(self):
        '''
        Close the active database connection
        '''
        pass
        
    @abstractmethod
    def enableForeignKeys(self):
        '''
        Set Foreign Key checks on
        '''
        pass

    @abstractmethod
    def disableForeignKeys(self):
        '''
        Set Foreign Key checks off
        '''
        pass

