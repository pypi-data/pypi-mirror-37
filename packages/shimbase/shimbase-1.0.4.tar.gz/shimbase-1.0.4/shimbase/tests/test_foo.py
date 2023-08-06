# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from foo import Foo, FooKeys, FooValues
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

class TestFoo(TestCase):
    """Foo object tests"""
    db = None

    @classmethod
    def setUpClass(cls):
        createName = './db/createdb.sql'
        testDataName = './db/' + '*_data.sql' 
        dbName = './db/test.db'
        os.system('cat {} | sqlite3 {}'.format(createName, dbName))
        os.system('cat {} | sqlite3 {}'.format(testDataName, dbName))
        cls.db = Database(dbName, SQLite3Impl())

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_keys_Immutablility(self):
        keys =FooKeys('foo name TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.name = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Foo.createAdhoc(None)
        self.assertEqual(l.getTable(), 'foo')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = Foo.create(('foo name TD', 'foo desc TD', 98))

        self.assertEqual(obj.getName(), 'foo name TD')
         
        self.assertEqual(obj.getDesc(), 'foo desc TD')
        self.assertEqual(obj.getBar_Id(), 98)
         

    def test_repr(self):
        obj = Foo('foo name TD', 'foo desc TD', 98)
        self.assertEqual(str(obj), "foo : Keys {'name': 'foo name TD'} : Values {'desc': 'foo desc TD', 'bar_id': 98}")

    def test_select(self):
        objs = TestFoo.db.select(Foo())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getName(), 'foo name TD')
        
        self.assertEqual(objs[0].getDesc(), 'foo desc TD')
        self.assertEqual(objs[0].getBar_Id(), 98)
        
        self.assertEqual(objs[1].getName(), 'foo name TD2')
        
        self.assertEqual(objs[1].getDesc(), 'foo desc TD2')
        self.assertEqual(objs[1].getBar_Id(), 99)
        
        
        objs = TestFoo.db.select(Foo('foo name TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getName(), 'foo name TD')
        
        self.assertEqual(objs[0].getDesc(), 'foo desc TD')
        self.assertEqual(objs[0].getBar_Id(), 98)
        

        objs = TestFoo.db.select(Foo.createAdhoc({'desc': 'foo desc TD', 'bar_id': 98}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getName(), 'foo name TD')
        
        self.assertEqual(objs[0].getDesc(), 'foo desc TD')
        self.assertEqual(objs[0].getBar_Id(), 98)
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestFoo.db.disableForeignKeys()

        with TestFoo.db.transaction() as t:
            TestFoo.db.upsert(
                    Foo('foo name TD', 'foo desc TD UPD', 100))
            objs = TestFoo.db.select(Foo('foo name TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getName(), 'foo name TD')
            

            d = eval("{'desc': 'foo desc TD UPD', 'bar_id': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestFoo.db.transaction() as t:
            foo = TestFoo.db.select(Foo('foo name TD'))[0]
            for k, v in d.items():
                foo.__getattribute__('set' + k.title())(v)

            TestFoo.db.upsert(foo)

            objs = TestFoo.db.select(Foo('foo name TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getName(), 'foo name TD')
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestFoo.db.disableForeignKeys()

        with TestFoo.db.transaction() as t:
            TestFoo.db.upsert(
                    Foo('foo name TD INS', 'foo desc TD UPD', 100))
            objs = TestFoo.db.select(Foo())

            self.assertEqual(len(objs), 3)

            d = eval("{'name': 'foo name TD INS'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'desc': 'foo desc TD UPD', 'bar_id': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestFoo.db.disableForeignKeys()

        with TestFoo.db.transaction() as t:
            TestFoo.db.delete(Foo('foo name TD'))

            objs = TestFoo.db.select(Foo())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Foo()
        self.assertTrue(True) 

if __name__ == '__main__':
    import unittest
    unittest.main()
