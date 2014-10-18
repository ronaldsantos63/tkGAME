#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkGAME - all-in-one Game library for Tkinter

    Copyright (c) 2014+ Raphaël Seban <motus@laposte.net>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""

# lib imports
import os.path as OP
import sqlite3 as DB


# private module member
__database = None


# app-wide unique instance getter
def get_database (**kw):
    """
        retrieves app-wide unique instance;
    """
    global __database
    if not isinstance(__database, TkGameDatabase):
        __database = TkGameDatabase(**kw)
    # end if
    return __database
# end def


class TkGameDatabase:
    """
        TkGame SQLite3 database manager;
    """

    # class constant defs
    ALL = "all"
    DEFAULT_PATH = "data/sqlite3/game.db"


    def __init__ (self, **kw):
        """
            class constructor;
        """
        # mandatory inits
        self.db_path = kw.get("db_path") or self.DEFAULT_PATH
        # hook_method
        self.init_members(**kw)
        # hook method
        self.open_database(**kw)
        # hook method
        self.init_database(**kw)
    # end def


    def close_database (self, *args, **kw):
        """
            event handler;
            closes current database connection, if any;
            raises TkGameDatabaseError otherwise;
        """
        # pending connection?
        if self.connection:
            # commit changes
            self.connection.commit()
            # close database
            self.connection.close()
            # reset members
            self.init_members()
        # no pending connection
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not close database: "
                "no pending connection by now (DB not open?)."
            )
        # end if
    # end def


    def commit (self, *args, **kw):
        """
            event handler;
            commits current pending transaction in database;
            raises TkGameDatabaseError otherwise;
        """
        # pending connection?
        if self.connection:
            # commit transaction
            self.connection.commit()
        # no pending connection
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not commit current transaction in database: "
                "no pending connection by now (DB not open?)."
            )
        # end if
    # end def


    @property
    def db_path (self):
        """
            database pathname (canonized);
        """
        return self.__db_path
    # end def


    @db_path.setter
    def db_path (self, value):
        # got value?
        if value:
            # init absolute canonized path
            self.__db_path = OP.abspath(OP.expanduser(value))
        else:
            # throw exception
            raise TkGameDatabaseError(
                "expected plain string of chars in "
                "'db_path' attribute."
            )
        # end if
    # end def


    @db_path.deleter
    def db_path (self):
        del self.__db_path
    # end def


    def dump_tables (self, *args, limit=100):
        """
            dumps listed tables/views to stdout (CLI);
            debug utility - should be reimplemented in subclass to
            meet your real needs;
        """
        # browse table list
        for _table in args:
            # dump table
            print("\nTable: '{}'".format(_table))
            # get all records along with @limit
            _rows = self.get_all(_table, limit)
            # got a recordset?
            if _rows:
                # show description
                print("Columns:", self.get_column_names())
                # dump rows
                print("Rows:")
                for _idx, _row in enumerate(_rows):
                    print("{:03d}:".format(_idx + 1), tuple(_row))
                # end for
            else:
                print("This table is *empty*.")
            # end if
        # end for
    # end def


    def fetch (self, qty=1, default=None):
        """
            fetches @qty rows resulting from a self.sql_query();
            if @qty < 2, same as self.cursor.fetchone();
            if @qty == "all", same as self.cursor.fetchall();
            if @qty == None, same as self.cursor.fetchmany();
            otherwise, same as self.cursor.fetchmany(size=@qty);
            by default, @qty = 1;
        """
        # enabled?
        if self.cursor:
            # fetch many rows?
            if qty is None:
                return self.cursor.fetchmany() or default
            # fetch all rows?
            elif str(qty).lower() == self.ALL:
                return self.cursor.fetchall() or default
            # fetch one row at a time?
            elif qty < 2:
                return self.cursor.fetchone() or default
            # fetch many rows with size
            else:
                return self.cursor.fetchmany(qty) or default
            # end if
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not retrieve last row id: "
                "no pending cursor by now (DB not open?)."
            )
        # end if
    # end def


    def get_column_names (self):
        """
            retrieves field names of the last SQL query, if any;
        """
        return tuple(c[0] for c in self.cursor.description)
    # end def


    def get_record (self, table_name, row_id):
        """
            retrieves an unique record for table @table_name along
            with @row_id row identifier;
        """
        self.sql_query(
            "select * from '{}' where ROWID = ? limit 1"
            .format(table_name),
            row_id
        )
        return self.fetch()
    # end def


    def get_all (self, table_name, limit=100):
        """
            retrieves all fields in a recordset of max. @limit rows
            for table @table_name;
        """
        self.sql_query(
            "select * from '{}' limit {}".format(table_name, limit)
        )
        return self.fetch(self.ALL)
    # end def


    def init_database (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        pass
    # end def


    def init_members (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        # member inits
        self.connection = None
        self.cursor = None
    # end def


    @property
    def last_row_id (self):
        """
            READ-ONLY attribute;
            returns row id of the last modified row using SQL INSERT
            statement;
            returns None when not relevant;
        """
        # enabled?
        if self.cursor:
            # last row id
            return self.cursor.lastrowid
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not retrieve last row id: "
                "no pending cursor by now (DB not open?)."
            )
        # end if
    # end def


    @last_row_id.setter
    def last_row_id (self, value):
        """
            READ-ONLY attribute;
        """
        # throw exception
        raise TkGameDatabaseError(
            "'last_row_id' is a READ-ONLY attribute."
        )
    # end def


    def open_database (self, *args, **kw):
        """
            event handler;
            opens database along with @db_path pathname;
            falls back to self.DEFAULT_PATH if omitted;
            sets row factory to recommended sqlite3.Row structure;
            initializes a DB self.cursor on-the-fly;
        """
        # open database
        self.connection = DB.connect(
            self.db_path or kw.get("db_path") or self.DEFAULT_PATH
        )
        # set row factory with default sqlite3.Row (recommended)
        self.row_factory = DB.Row
        # get a new db cursor
        self.cursor = self.connection.cursor()
    # end def


    def rollback (self, *args, **kw):
        """
            event handler;
            cancels current pending transaction in database;
            raises TkGameDatabaseError otherwise;
        """
        # pending connection?
        if self.connection:
            # cancel transaction
            self.connection.rollback()
        # no pending connection
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not rollback current transaction in database: "
                "no pending connection by now (DB not open?)."
            )
        # end if
    # end def


    @property
    def row_factory (self):
        """
            gets current row factory;
            raises TkGameDatabaseError otherwise;
        """
        # pending connection?
        if self.connection:
            # get current row factory
            return self.connection.row_factory
        # no pending connection
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not retrieve current row factory: "
                "no pending connection by now (DB not open?)."
            )
        # end if
    # end def


    @row_factory.setter
    def row_factory (self, value):
        """
            sets a new row factory for current database;
            raises TkGameDatabaseError otherwise;
        """
        # pending connection?
        if self.connection and callable(value):
            # set new row factory
            self.connection.row_factory = value
        # no pending connection
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not set up row factory for database: "
                "value is not a callable or "
                "no pending connection by now (DB not open?)."
            )
        # end if
    # end def


    def sql_query (self, query, *args, **kw):
        """
            executes a unique SQL statement;
            use sql_script() instead, if you're looking for many SQL
            statements with no arguments (SQL script);
        """
        # enabled?
        if self.cursor:
            # execute unique SQL statement
            self.cursor.execute(query, args or kw)
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not execute SQL statement: "
                "no pending cursor by now (DB not open?)."
            )
        # end if
    # end def


    def sql_script (self, script):
        """
            executes an SQL multiple statement script;
            use sql_query() instead, if you're looking for only one
            SQL statement with optional arguments;
        """
        # enabled?
        if self.cursor:
            # execute SQL script
            self.cursor.executescript(script)
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not execute SQL script: "
                "no pending cursor by now (DB not open?)."
            )
        # end if
    # end def

# end class TkGameDatabase


# exception handling

class TkGameDatabaseError (Exception):
    """
        exception handler for TkGameDatabase class;
    """
    pass
# end class
