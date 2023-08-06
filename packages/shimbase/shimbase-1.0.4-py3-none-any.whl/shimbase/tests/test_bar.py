# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from bar import Bar, BarKeys, BarValues
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

class TestBar(TestCase):
    """Bar object tests"""
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
        keys =BarKeys(98)

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.id = 75
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Bar.createAdhoc(None)
        self.assertEqual(l.getTable(), 'bar')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = Bar.create((98, 98, 2.3, 'X'))

        self.assertEqual(obj.getId(), 98)
         
        self.assertEqual(obj.getHeading(), 98)
        self.assertEqual(obj.getSpeed(), 2.3)
        self.assertEqual(obj.getSignal(), 'X')
         

    def test_repr(self):
        obj = Bar(98, 98, 2.3, 'X')
        self.assertEqual(str(obj), "bar : Keys {'id': 98} : Values {'heading': 98, 'speed': 2.3, 'signal': 'X'}")

    def test_select(self):
        objs = TestBar.db.select(Bar())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getHeading(), 98)
        self.assertEqual(objs[0].getSpeed(), 2.3)
        self.assertEqual(objs[0].getSignal(), 'X')
        
        self.assertEqual(objs[1].getId(), 99)
        
        self.assertEqual(objs[1].getHeading(), 99)
        self.assertEqual(objs[1].getSpeed(), 2.4)
        self.assertEqual(objs[1].getSignal(), 'Z')
        
        
        objs = TestBar.db.select(Bar(98))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getHeading(), 98)
        self.assertEqual(objs[0].getSpeed(), 2.3)
        self.assertEqual(objs[0].getSignal(), 'X')
        

        objs = TestBar.db.select(Bar.createAdhoc({'heading': 98, 'speed': 2.3, 'signal': 'X'}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getHeading(), 98)
        self.assertEqual(objs[0].getSpeed(), 2.3)
        self.assertEqual(objs[0].getSignal(), 'X')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestBar.db.disableForeignKeys()

        with TestBar.db.transaction() as t:
            TestBar.db.upsert(
                    Bar(98, 100, 5.6, 'A'))
            objs = TestBar.db.select(Bar(98))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getId(), 98)
            

            d = eval("{'heading': 100, 'speed': 5.6, 'signal': 'A'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestBar.db.transaction() as t:
            bar = TestBar.db.select(Bar(98))[0]
            for k, v in d.items():
                bar.__getattribute__('set' + k.title())(v)

            TestBar.db.upsert(bar)

            objs = TestBar.db.select(Bar(98))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getId(), 98)
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestBar.db.disableForeignKeys()

        with TestBar.db.transaction() as t:
            TestBar.db.upsert(
                    Bar(100, 100, 5.6, 'A'))
            objs = TestBar.db.select(Bar())

            self.assertEqual(len(objs), 3)

            d = eval("{'id': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'heading': 100, 'speed': 5.6, 'signal': 'A'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestBar.db.disableForeignKeys()

        with TestBar.db.transaction() as t:
            TestBar.db.delete(Bar(98))

            objs = TestBar.db.select(Bar())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Bar()
        self.assertTrue(True and obj.isNullable('heading') and obj.isNullable('speed') and obj.isNullable('signal')) 

if __name__ == '__main__':
    import unittest
    unittest.main()
