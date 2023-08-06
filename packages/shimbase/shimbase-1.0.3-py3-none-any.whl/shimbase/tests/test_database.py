# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from shimbase.database import Database, DatabaseObject, DatabaseInvObjError, \
        AdhocKeys
from shimbase.dbimpl import DatabaseDataError, DatabaseIntegrityError
from shimbase.sqlite3impl import SQLite3Impl
from foo import Foo
from bar import Bar

class TestDatabase(TestCase):
    """Database tests"""
    db = None

    @classmethod
    def setUpClass(cls):
        createName = './db/createdb.sql' 
        testDataName = './db/*_data.sql' 
        dbName = './db/test.db'
        os.system('cat {} | sqlite3 {}'.format(createName, dbName))
        os.system('cat {} | sqlite3 {}'.format(testDataName, dbName))
        cls.db = Database(dbName, SQLite3Impl())

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
    
    def setUp(self):
        TestDatabase.db.enableForeignKeys()

    def tearDown(self):
        pass

    def test_select(self):
        bars = TestDatabase.db.select(Bar())

        self.assertEqual(len(bars), 2)
        self.assertEqual(
                str(bars[0]), "bar : Keys {'id': 98} : Values {'heading': 98, 'speed': 2.3, 'signal': 'X'}")
        self.assertEqual(bars[1].getTable(), 'bar')
        self.assertEqual(bars[1].getId(), 99)
        self.assertEqual(bars[1].getHeading(), 99)
        self.assertEqual(bars[1].getSignal(), 'Z')

        bars = TestDatabase.db.select(Bar(98))
        self.assertEqual(len(bars), 1)
        self.assertEqual(
                str(bars[0]), "bar : Keys {'id': 98} : Values {'heading': 98, 'speed': 2.3, 'signal': 'X'}")

        bars = TestDatabase.db.select(
                Bar.createAdhoc(AdhocKeys({'signal': 'Z'})))
        self.assertEqual(len(bars), 1)
        self.assertEqual(
                str(bars[0]), "bar : Keys {'id': 99} : Values {'heading': 99, 'speed': 2.4, 'signal': 'Z'}")

    def test_foreign_key(self):
        with TestDatabase.db.transaction(), \
                self.assertRaises(DatabaseIntegrityError) as cm:
            # bar id 999 should not exist
            TestDatabase.db.upsert(Foo('my foo', 'a new foo', 999))
        self.assertEqual('FOREIGN KEY constraint failed', cm.exception.args[0])

    def test_transaction(self):
        # test commit
        with TestDatabase.db.transaction():
            TestDatabase.db.upsert(Bar(101, 180, 33.5, 'A'))
            TestDatabase.db.upsert(Bar(102, 270, 50.33, 'B'))
        bars = TestDatabase.db.select(Bar())
        self.assertEqual(len(bars), 4)

        # test rollback on exception
        with TestDatabase.db.transaction(), \
                self.assertRaises(DatabaseIntegrityError) as cm:
            TestDatabase.db.upsert(Foo('a new foo', ))
        self.assertEqual(cm.exception.args[0], 'NOT NULL constraint failed: foo.desc')
        self.assertEqual(len(bars), 4)

        # test a forced rollback
        with TestDatabase.db.transaction() as t:
            TestDatabase.db.upsert(
                    Bar(104, 355, 99.99, 'D'))
            t.fail()
        bars = TestDatabase.db.select(Bar())
        self.assertEqual(len(bars), 4)

        # restore table to pre-test state
        with TestDatabase.db.transaction():
            TestDatabase.db.delete(Bar(101))
            TestDatabase.db.delete(Bar(102))
        bars = TestDatabase.db.select(Bar())
        self.assertEqual(len(bars), 2)

    def test_select_NoRows(self):
        bars = TestDatabase.db.select(Bar(1000))
        self.assertEqual(len(bars), 0)

    def test_upsert(self):
        with TestDatabase.db.transaction() as t:
            TestDatabase.db.upsert(Bar(101, 180, 23.45, 'F'))

            bars = TestDatabase.db.select(Bar())

            self.assertEqual(len(bars), 3)
            self.assertEqual(
                    str(bars[2]), "bar : Keys {'id': 101} : Values {'heading': 180, 'speed': 23.45, 'signal': 'F'}")

            TestDatabase.db.upsert(Bar(98, 270, signal='B'))

            bars = TestDatabase.db.select(Bar(98))

            self.assertEqual(len(bars), 1)
            self.assertEqual(
                    str(bars[0]), "bar : Keys {'id': 98} : Values {'heading': 270, 'speed': None, 'signal': 'B'}")

            # force a rollback
            t.fail()

    def test_null(self):
        with TestDatabase.db.transaction() as t:
            TestDatabase.db.upsert(Bar(999, 90, 120.0, 'C'))

            bars = TestDatabase.db.select(Bar(999))

            self.assertEqual(len(bars), 1)
            self.assertEqual(
                    str(bars[0]), "bar : Keys {'id': 999} : Values {'heading': 90, 'speed': 120.0, 'signal': 'C'}")

            # force a rollback
            t.fail()

    def test_DatabaseObjectError(self):
        with TestDatabase.db.transaction(), \
                self.assertRaises(DatabaseInvObjError) as cm:
            leagues = TestDatabase.db.select(object())
        self.assertEqual(
                cm.exception.msg, 'Not a valid DB object : ' + str(object()))

    def test_upsert_Error(self):
        with TestDatabase.db.transaction(), \
                self.assertRaises(DatabaseDataError) as cm:
            TestDatabase.db.upsert(Bar())
        self.assertEqual(
                cm.exception.msg, 'No keys provided for UPDATE')

    def test_delete(self):
        with TestDatabase.db.transaction():
            TestDatabase.db.upsert(Bar(123, 456, 78.9, 'D'))

        bars = TestDatabase.db.select(Bar())
        self.assertEqual(len(bars), 3)
        self.assertEqual(
                str(bars[2]), "bar : Keys {'id': 123} : Values {'heading': 456, 'speed': 78.9, 'signal': 'D'}")

        with TestDatabase.db.transaction():
            TestDatabase.db.delete(Bar(123))
        bars = TestDatabase.db.select(Bar())
        self.assertEqual(len(bars), 2)

        bars = TestDatabase.db.select(Bar(123))
        self.assertEqual(len(bars), 0)
        
    def test_delete_Error(self):
        with TestDatabase.db.transaction(), \
                self.assertRaises(DatabaseDataError) as cm:
            TestDatabase.db.delete(Bar())
        self.assertEqual(
                cm.exception.msg, 'No keys provided for DELETE')

if __name__ == '__main__':
    import unittest
    unittest.main()
