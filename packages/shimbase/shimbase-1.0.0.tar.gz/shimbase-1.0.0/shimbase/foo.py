from dataclasses import dataclass
from database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class FooKeys(DatabaseKeys):
    '''
    foo database object primary key representation
    '''
    name:str
    

    def __init__(self, name:str):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'name', name)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all FooKeys fields
        '''
        fields = {} if not (self.name) else {'name' : self.name}
        return fields
        
class FooValues(DatabaseValues):
    '''
    foo database object values representation
    '''
    def __init__(self, desc:str, bar_id:int):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'desc', desc)
        object.__setattr__(self, 'bar_id', bar_id)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all FooValues fields
        '''
        fields = {'desc' : self.desc, 'bar_id' : self.bar_id}
        return fields
        
class Foo(DatabaseObject):
    '''
    foo database object representation
    '''

    @classmethod
    def createAdhoc(cls, keys:AdhocKeys):
        '''
        Class method to create a database object with the provided adhoc keys
        list

        :param keys: an AdhocKeys object
        :returns: a Foo object constructed via the provided key
        :raises: None
        '''
        l = Foo()
        l._keys = keys
        return l

    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Private instance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the provided key
        '''
        return Foo.createAdhoc(keys)

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Foo object constructed from row
        '''
        name, desc, bar_id = row
        return Foo(name, desc, bar_id)

    def _createSingle(cls, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Foo object constructed from row
        '''
        return Foo.createSingle(row)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Foo objects constructed from rows
        '''
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def _createMulti(cls, rows:tuple):
        '''
        Private instance method to create database objects from the provided 
        database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Foo objects constructed from rows
        '''
        return Foo.createMulti(rows)

    def __init__(self, name:str = None, desc:str = None, bar_id:int = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = FooKeys(name)
        vals = FooValues(desc, bar_id)

        super().__init__('foo', keys, vals)

    def getTable(self):
        return self._table

    def getName(self):
        return self._keys.name
    
    
    def getDesc(self):
        return self._vals.desc
    
    def getBar_Id(self):
        return self._vals.bar_id
    
    
    def setDesc(self, desc:str):
       self._vals.desc = desc
    
    def setBar_Id(self, bar_id:int):
       self._vals.bar_id = bar_id
    
    

    def isNullable(self, field):
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
