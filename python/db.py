import os
import abc
import datetime
import logging
import sqlite3

##GENERIC DATABASE  CLASS

class Database(object):
    """Just an usual class
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self,):
        """
        """
        self.con = None
        self.cr = None

    @abc.abstractmethod
    def connect(self,):
        """Connects to the db
        """
        return None

    def create_table(self, *args, **kwargs):
        """Creates a table
        """
        query = "CREATE TABLE {} ".format(args[0])
        print(query)

    def executeQuery(self, query):
        """Executes a SQL query
        """
        try:
            self.cr.execute(query)
            return self.cr
        except (Exception,) as e:
            print(e)
            
        return False

    def commit(self,):
        """Commits the  last change
        """
        try:
            self.con.commit()
            self.last_id()
        except (Exception,) as e:
            print(e)

    def last_id(self,):
        """Returns the id of the last affected row
        """
        return self.cr.rowcount
        
## SQLITE CLASS

class MySqlite(Database):
    """Simple SQlite3 class handler
    """

    def __init__(self, dbfile):
        """
        """
        super(MySqlite, self).__init__()
        
        self.dbfile = dbfile

    def connect(self,):
        """Connects to the db
        """
        try:
            self.con = sqlite3.connect(self.dbfile)
            self.cr = self.con.cursor()
            return self.con
        except (Exception,) as e:
            print(e)

        return None
