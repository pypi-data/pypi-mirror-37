from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class BarKeys(DatabaseKeys):
    '''
    bar database object primary key representation
    '''
    id:int
    

    def __init__(self, id:int):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'id', id)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all BarKeys fields
        '''
        fields = {} if not (self.id) else {'id' : self.id}
        return fields
        
class BarValues(DatabaseValues):
    '''
    bar database object values representation
    '''
    def __init__(self, heading:int = None, speed:float = None, signal:str = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'heading', heading)
        object.__setattr__(self, 'speed', speed)
        object.__setattr__(self, 'signal', signal)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all BarValues fields
        '''
        fields = {'heading' : self.heading, 'speed' : self.speed, 'signal' : self.signal}
        return fields
        
class Bar(DatabaseObject):
    '''
    bar database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param keys: a dictionary of fields
        :returns: Bar object constructed via an AdhocKey of fields
        '''
        l = Bar()
        l._keys = AdhocKeys(fields) 
        return l

    def _createAdhoc(self, fields:dict):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param keys: a dictionary of fields
        :returns: Bar object constructed via an AdhocKey of fields
        '''
        return Bar.createAdhoc(keys)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Bar object constructed from row
        '''
        id, heading, speed, signal = row
        return Bar(id, heading, speed, signal)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Bar object constructed from row
        '''
        return Bar.create(row)

    def __init__(self, id:int = None, heading:int = None, speed:float = None, signal:str = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = BarKeys(id)
        vals = BarValues(heading, speed, signal)

        super().__init__('bar', keys, vals)

    def getTable(self):
        return self._table

    def getId(self):
        return self._keys.id
    
    
    def getHeading(self):
        return self._vals.heading
    
    def getSpeed(self):
        return self._vals.speed
    
    def getSignal(self):
        return self._vals.signal
    
    
    def setHeading(self, heading:int):
       self._vals.heading = heading
    
    def setSpeed(self, speed:float):
       self._vals.speed = speed
    
    def setSignal(self, signal:str):
       self._vals.signal = signal
    
    

    def isNullable(self, field):
        if field == 'heading':
            return True
        elif field == 'speed':
            return True
        elif field == 'signal':
            return True
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
