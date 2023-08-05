import MySQLdb
import psycopg2
from collections import namedtuple
from itertools import repeat

# class to access and control MySQL or PostgreSQL based databases
class Jdatabase():
    conn = None
    cur = None
    conf = None
    database_type = "MySQL"

    """ INSTANTIATION method """
    # sets default arguments, and establishes a connection to the database
    def __init__(self, **kwargs):
        self.conf = kwargs
        self.conf["charset"] = kwargs.get("charset", "utf8")
        self.conf["port"] = kwargs.get("port", 3306)
        self.conf["ssl"] = kwargs.get("ssl", False)
        self.conf["autocommit"] = kwargs.get("autocommit", True)
        self.database_type = self.connect()
    """ end INSTANTIATION method """

    """ TABLE methods """
    def _get_table_names_data(self, sql):
        self.query(sql)
        data = str(self.cur.fetchall()).replace("(('", "").replace("',))", "")
        # try to split data
        try:
            data = data.split("',), ('")
        # if can't split, it is itself
        except:
            data = data
        return data

    def _get_table_names(self):
        sql = "SELECT table_name FROM information_schema.tables"
        return self._get_table_names_data(sql)

    def _get_system_table_names(self):
        sql = "SELECT table_name FROM information_schema.tables WHERE TABLE_TYPE = 'SYSTEM VIEW'"
        return self._get_table_names_data(sql)

    def get_table_names(self):
        final = []
        data = self._get_table_names()
        sdata = self._get_system_table_names()
        for item in data:
            if item not in sdata:
                final.append(str(item))
        # set info for self use
        self.table_names = final
        self.stable_names = sdata
        return data

    def get_cleaned_table_names(self):
        final = []
        data = self._get_table_names()
        sdata = self._get_system_table_names()
        for item in data:
            if item not in sdata:
                final.append(str(item))
        return final

    def check_for_table(self, table):
        data = self.get_table_names()
        if table in data:
            return True
        return False

    # method to process columns entry for no primary key entry
    def _process_column_entry(self, column_entry):
        # empty columns entry process
        if column_entry.__len__() == 0:
            column_entry = {"col1": ["VARCHAR(32)", "NOT NULL"]}
        column_entry_str = str(column_entry)
        if "PRIMARY KEY" not in column_entry_str:
            column_entry = self._add_dicts({"jd": ["VARCHAR(128)", "PRIMARY KEY"]}, column_entry)
        return column_entry

    def create_table(self, table, columns):
        columns = self._process_column_entry(columns)
        query = self._serialize_columns(columns)
        sql = "CREATE TABLE %s (%s)" % (table, query)
        return self.query(sql).rowcount

    def create_table_if_not_exists(self, table, columns):
        columns = self._process_column_entry(columns)
        query = self._serialize_columns(columns)
        sql = "CREATE TABLE IF NOT EXISTS %s (%s)" % (table, query)
        return self.query(sql).rowcount

    def create_table_if_false_check(self, table, columns):
        if not self.check_for_table(table):
            columns = self._process_column_entry(columns)
            query = self._serialize_columns(columns)
            sql = "CREATE TABLE %s (%s)" % (table, query)
            return self.query(sql).rowcount
        else:
            return False
    """ end TABLE methods """

    """ DATA methods """
    def get_one(self, table=None, fields="*", where=None, order=None):
        scratch_val = self.is_connected()
        if not scratch_val == True:
            # if not connected / error connecting return error
            return scratch_val
        cur = self._select(table=table, fields=fields, where=where, order=order)
        result = cur.fetchone()
        row = None
        if result:
            row = result
        return row

    def get_all(self, table=None, fields='*', where=None, order=None):
        scratch_val = self.is_connected()
        if not scratch_val == True:
            # if not connected / error connecting return error
            return scratch_val
        cur = self._select(table, fields, where, order)
        result = cur.fetchall()
        data = None
        if result:
            data = result
        return data

    def insert(self, table, data):
        query = self._serialize_insert(data)
        sql = "INSERT INTO %s (%s) VALUES(%s)" % (table, query[0], query[1])
        return self.query(sql, data.values()).rowcount

    def insert_batch(self, table, data):
        query = self._serialize_batch_insert(data)
        sql = "INSERT INTO %s (%s) VALUES %s" % (table, query[0], query[1])
        vals = [v for sublist in data for k, v in sublist.items()]
        return self.query(sql, vals).rowcount

    def update(self, table, data, where=None):
        query = self._serialize_update(data)
        sql = "UPDATE %s SET %s" % (table, query)
        if where and len(where) > 0:
            sql += " WHERE %s" % where[0]
        return self.query(sql, list(data.values()) + where[1] if where and len(where) > 1 else data.values()).rowcount

    def insert_or_update(self, table, data, keys):
        insert_data = data.copy()
        data = {k: data[k] for k in data if k not in keys}
        insert = self._serialize_insert(insert_data)
        update = self._serialize_update(data)
        sql = "INSERT INTO %s (%s) VALUES(%s) ON DUPLICATE KEY UPDATE %s" % (table, insert[0], insert[1], update)
        return self.query(sql, list(insert_data.values()) + list(data.values())).rowcount

    def delete(self, table, where=None):
        sql = "DELETE FROM %s" % table
        if where and len(where) > 0:
            sql += " WHERE %s" % where[0]
        return self.query(sql, where[1] if where and len(where) > 1 else None).rowcount

    def last_id(self):
        return self.cur.lastrowid

    def last_query(self):
        # try to get cur statement
        try:
            return self.cur.statement
        # attribute error, get cur last executed
        except AttributeError:
            return self.cur._last_executed
    """ end DATA methods"""

    """ CLASS methods """
    def _mysql_connect(self):
        # no ssl
        if not self.conf["ssl"]:
            self.conn = MySQLdb.connect(host=self.conf["host"], user=self.conf["user"], passwd=self.conf["passwd"],
                                        db=self.conf["db"], charset=self.conf["charset"], port=self.conf["port"])
        # ssl
        else:
            self.conn = MySQLdb.connect(host=self.conf["host"], user=self.conf["user"], passwd=self.conf["passwd"],
                                        db=self.conf["db"], charset=self.conf["charset"], port=self.conf["port"],
                                        ssl=self.conf["ssl"])
        self.cur = self.conn.cursor()
        self.conn.autocommit(self.conf["autocommit"])
        return "MySQL"

    def _postgresql_connect(self):
        self.conn = psycopg2.connect(host=self.conf["host"], database=self.conf["db"], user=self.conf["user"],
                                     password=self.conf["passwd"])
        self.cur = self.conn.cursor()
        self.conn.autocommit(self.conf["autocommit"])
        return "PostgreSQL"

    def connect(self):
        e = None
        # try to connect to the database through MySQLdb
        try:
            return self._mysql_connect()
        except (Exception, MySQLdb.DatabaseError) as error:
            e = error
            print(error)
        # try to connect to the database through PostgreSQL
        try:
            return self._postgresql_connect()
        except (Exception, psycopg2.DatabaseError) as error:
            e = error
            print(error)
        return e if e != None else False

    def is_open(self):
        try:
            return self.conn.open
        except:
            return False

    def is_connected(self):
        if not self.is_open():
            error = self.connect()
            if not error == True:
                return error
        return True

    def query(self, sql, parms=None):
        try:
            self.cur.execute(sql, parms)
        except (Exception, MySQLdb.DatabaseError) as error:
            if error[0] == 2006:
                self.connect()
                self.cur.execute(sql, parms)
            else:
                raise
        except:
            print("Query failed")
            raise
        return self.cur

    def commit(self):
        return self.conn.commit()

    def close(self):
        try:
            self.cur.close()
            self.conn.close()
            return True
        except (Exception, MySQLdb.DatabaseError) as error:
            return error

    def reconnect(self):
        self.close()
        self.database_type = self.connect()
        return True

    def __str__(self):
        return str(self.conf["db"])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    """ end CLASS methods """

    """ RESTRICTED methods """
    def _select(self, table=None, fields=(), where=None, order=None):
        sql = "SELECT %s FROM %s" % (",".join(fields), table)
        if where and len(where) > 0:
            sql += " WHERE %s" % where[0]
        if order:
            sql += " ORDER BY %s" % order[0]
            if len(order) > 1:
                sql += " %s" % order[1]
        return self.query(sql, where[1] if where and len(where) > 1 else None)

    def _serialize_insert(self, data):
        keys = ",".join(data.keys())
        vals = ",".join(["%s" for k in data])
        return [keys, vals]

    def _serialize_batch_insert(self, data):
        keys = ",".join(data[0].keys())
        v = "(%s)" % ",".join(tuple("%s".rstrip(',') for v in range(len(data[0]))))
        l = ','.join(list(repeat(v, len(data))))
        return [keys, l]

    def _serialize_update(self, data):
        return "=%s,".join(data.keys()) + "=%s"

    def _serialize_columns(self, data):
        if len(data) > 1:
            return ", ".join(f"{column} {data[column][0]} {data[column][1]}" for column in data)
        else:
            return ", ".join(f"{column} {data[column]}" for column in data)

    # method to add dict2 to dict1, does not add duplicates
    def _add_dicts(self, dict1, dict2):
        for item in dict2:
            if item not in dict1:
                dict1[item] = dict2[item]
        return dict1

    # method to add dict2 to dict1, and update duplicates
    def _add_and_update_dicts(self, dict1, dict2):
        for item in dict2:
            dict1[item] = dict2[item]
        return dict1
    """ end RESTRICTED methods """