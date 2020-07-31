#!/usr/bin/env python3
#coding: utf-8
import sqlite3
from datetime import datetime

class Database:

    def __init__(self, dbname: str):
        self._lastid = 0
        self._rowscount = 0
        
        if (dbname[-8:] != ".sqlite3"):
            dbname += ".sqlite3"

        self._dbname = dbname

        try:
            self._conn = sqlite3.connect(self._dbname, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
            self._cur = self._conn.cursor()

        except sqlite3.Error as e:
            raise Exception("Error on making db connection: %s" % e.args[0])

    def execQuery(self, sql, values = []):
        try:
            self._cur.execute(sql, values)
            self._lastid = self._cur.lastrowid
            self._rowscount = self._cur.rowcount
        except sqlite3.Error as e:
            raise Exception("Error on %s: %s" % (sql, e.args[0]))

        self._values = []
        return self._rowscount

    def execSelect(self, sql, values = []):
        try:
            print(values)
            self._cur.execute(sql, values)
            self._values = []
            return self._cur.fetchall()

        except sqlite3.Error as e:
            raise Exception("Error on %s: %s" % (sql, e.args[0]))

    def getLastId(self):
        return self._lastid

    def getRowsAffected(self):
        return self._rowscount

    def getCursor(self):
        return self._cur

    def create(self, table, columns = []):
        sql = f'CREATE TABLE "{table}" (\n'

        first = True
        for column in columns:
            if not first:
                sql += ', \n'
            first = False

            sql += f"\t`{column['name']}` {column['type']}"

            if 'size' in column.keys():
                sql += f"({column['size']}) "
            else:
                sql += " "

            if 'default' in column.keys():
                sql += f"DEFAULT {column['default']} "

            if 'extra' in column.keys():
                for attr in column['extra']:
                    sql += f"{attr} "

        sql += '\n\t)'
        self.execQuery(sql)

    def drop(self, tbname):
        sql = f'DROP TABLE "{tbname}"'
        self.execQuery(sql)
        tbSequence = Table(self, 'sqlite_sequence')
        rows = tbSequence.delete().where({'name': tbname}).exec()
        return rows

    def truncate(self, tbname):
        tb = Table(self, tbname)
        rows = tb.delete().exec()
        tbSequence = Table(self, 'sqlite_sequence')
        tbSequence.update({'seq': 0}).where({'name': tbname}).exec()
        return rows

    def get(self):
        return self._cur

    def commit(self):
        self._conn.commit()

    def close(self):
        self.commit()
        self._conn.close()

class Table:

    def __init__(self, dbobj, tbname: str):
        self._dbobj = dbobj
        self._rows = []
        self._tbname = tbname
        self._columnNames = []
        self._values = []
        self._statement = ''
        self._where = ''
        self._group = ''
        self._having = ''
        self._order = ''
        self.columnNames()

    def select(self, columns = ''):
        self._statement = f'SELECT {columns} FROM {self._tbname} '
        return self

    def update(self, columns = []):
        self._statement = f'UPDATE "{self._tbname}" SET '

        if ('updated_at' in self._columnNames and 'updated_at' not in columns.keys()):
            columns['updated_at'] = datetime.today()

        update_columns = ''
        for column in columns.keys():
            if (update_columns != ''):
                update_columns += ', '

            update_columns += f'`{column}` = ?' 
    
        self._statement += f'{update_columns} '
        self.setValues(columns.values())

        return self

    def delete(self):
        self._statement = f'DELETE FROM "{self._tbname}" '
        return self

    def insert(self, columns = {}):
        if len(columns) == 0:
            return self

        self._statement = f'INSERT INTO "{self._tbname}" (\n'
        col_str = ''
        val_str = ''

        if ('created_at' in self._columnNames and 'created_at' not in columns.keys()):
            columns['created_at'] = datetime.today()

        if ('updated_at' in self._columnNames and 'updated_at' not in columns.keys()):
            columns['updated_at'] = datetime.today()

        first = True
        for column in columns.keys():
            if not first:
                col_str += ', \n'
                val_str += ', '
            first = False

            col_str += f'\t`{column}`'
            val_str += '?'

        self._statement += f'{col_str}\n\t) VALUES (\n{val_str}) '
        self.setValues(columns.values())
        return self

    def group(self, group = []):
        if len(group) == 0:
            return self

        self._group = 'GROUP BY '
        first = True
        for col in group:
            if not first:
                self._group += ', '
            first = False

            self._group += f'`{col}`'

        return self

    def having(self, having = {}, op = '=', cont = 'AND'):
        if len(having) == 0:
            return self

        if self._having == '':
            self._having = 'HAVING '
        else:
            self._having += f'{cont} '

        first = True
        for col in having.keys():
            if not first:
                self._having += f'{cont} '
            first = False
            
            self._having += f'{col} {op} ?'
        
        self.setValues(having.values())
        return self

    def order(self, order = {}):
        if len(order) == 0:
            return self

        self._order = 'ORDER BY '
        first = True
        for col in order.keys():
            if not first:
                self._order += ', '
            first = False

            self._order += f'`{col}` {order[col]} '

        return self

    def get(self, id):
        where = {}
        where['id'] = id
        return self.select('*').where(where).exec()

    def getAll(self):
        return self.select('*').exec()

    def columnNames(self):
        if len(self._columnNames) == 0:
            sql = f'SELECT * FROM "{self._tbname}" LIMIT 1'
            res = self.execSelect(sql)
            if res is None:
                row = {}
            else:
                if len(res) == 0:
                    row = {}
                else:
                    row = res[0]

            cur = self._dbobj.getCursor()

            for i, col in enumerate(cur.description):
                if isinstance(col, tuple):
                    self._columnNames.append(col[0])
                else:
                    self._columnNames.append(col)

    def getColumnNames(self):
        self.columnNames()
        return self._columnNames

    def exec(self):
        sql = self.getSQL()
        self._statement = ''
        self._where = ''
        self._order = ''
        
        if sql.startswith('SELECT'):
            rows = self._dbobj.execSelect(sql, self._values)
            self.setRows(rows)
            res = self._rows

        else:
            res = self._dbobj.execQuery(sql, self._values)

        self._values = []
        return res

    def execSelect(self, sql, values = []):
        return self._dbobj.execSelect(sql, values)

    def setValues(self, values):
        self._values += values

    def setRows(self, rows):
        self._rows = []
        columns = self.getColumnNames()

        for row in rows:
            new_row = {}
            for i, value in enumerate(row):
                new_row[columns[i]] = value

            self._rows.append(new_row)

    def where(self, cond = {}, op = '=', cont = 'AND'):
        if self._where == '':
            self._where = 'WHERE '
        else:
            self._where += f'{cont} '

        self._where += '( '
        first = True
        for col in cond.keys():
            if not first:
                self._where += f'{cont} '
            first = False

            self._where += f'`{col}` {op} ? '
        self._where += ') '
        
        self.setValues(cond.values())
        return self

    def whereLike(self, cond = {}, cont = 'AND'):
        values = {}
        for col in cond.keys():
            values[col] = f'%{cond[col]}%'

        self.where(values, 'LIKE', cont)
        return self

    def whereNotEqual(self, cond = {}, cont = 'AND'):
        self.where(cond, '<>', cont)
        return self

    def getSQL(self):
        sql = self._statement
        sql += self._where
        sql += self._order

        return sql

    def commit(self):
        self._dbobj.commit()