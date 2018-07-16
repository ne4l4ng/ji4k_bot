#!/usr/bin/env python

import sqlite3


class DBHelper:
    def __init__(self, dbname="ji4k.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        self.setup_makan_places()
        jiak_session_tblstmt = \
            "CREATE TABLE IF NOT EXISTS jiak_sessions (venue text, chat_id int, date text)"
        tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(jiak_session_tblstmt)
        self.conn.execute(tblstmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def add_vote(self, venue, chat_id, date):
        stmt = "INSERT INTO jiak_sessions (venue, chat_id, date) VALUES (?, ?, ?)"
        args = (venue, chat_id, date)
        self.conn.execute(stmt, args)
        self.conn.commit()

    ##TODO refactor
    def setup_makan_places(self):
        makan_tblstmt = "CREATE TABLE IF NOT EXISTS makan_places (id int, name text)"
        self.conn.execute(makan_tblstmt)
        if (len(self.get_makan_places())) == 0:
            insert_makan_stmt = "INSERT INTO makan_places (id, name) VALUES (1, 'Cafeteria'),(2, 'Opposite')," \
                            "(3, 'Fish Soup'),(4,'Collins')"
            self.conn.execute(insert_makan_stmt)
        self.conn.commit()

    def get_makan_places(self):
        stmt = "SELECT name FROM makan_places"
        return [x[0] for x in self.conn.execute(stmt)]

    def get_jiak_sessions(self, date):
        print("date = {}".format(date))
        stmt = "SELECT venue FROM jiak_sessions WHERE date = (?)"
        args = (date,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def tally_jiak_sessions(self, date):
        print("date = {}".format(date))
        stmt = "SELECT venue, count(venue) as 'votes' FROM jiak_sessions" \
               " WHERE date = (?) group by venue order by votes DESC"
        args = (date,)
        c = self.conn.cursor()
        votes = []
        for rows in c.execute(stmt, args):
            print(rows)
            votes.append([rows[0], rows[1]])
        return votes
