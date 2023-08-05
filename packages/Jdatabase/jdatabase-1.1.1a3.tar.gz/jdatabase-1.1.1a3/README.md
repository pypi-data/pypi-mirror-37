# JDatabase (JDB)
jdatabase package by [Joshua Widrick](https://joshuawidrick.com "Homepage - Joshua Widrick") <br />

**Documentation:** [docs.jwid.co](https://docs.jwid.co/jdatabase "JDatabase Documentation") <br />
**GitHub (source code):** [GitHub.com/JoshWIdrick/jdb](https://github.com/JoshWidrick/jdb "JDatabase Source Code") <br />
**Version:** 1.1.1-alpha3 <br />
**License:** MIT <br />

Function / Overview:
===
The function of the jdatabase package is to allow easy and fluid connection, control, and use of MySQL, and 
PostgreSQL database systems through one easy to use, concurrent format. The package also allows for logging of data transactions, 
allowing for database roll-back. <br />
The development of this package has been solely for use in many of [my other projects](https://joshuawidrick.com "Homepage - Joshua Widrick"). This package has a lot of default functionality that a normal user will not need. Any feature that you do not need, you can ignore (however understanding it is recommended). <br /> 

Installation:
===
The jdatabase package is available publicly through [PyPi / pip](https://pypi.org/project/jdatabase "jdatabase on pip"), so all you need to do is
`sudo pip install jdatabase`. 
The package can be updated with 
`sudo pip install jdatabase --upgrade`. <br />
From source, run
`sudo python setup.py install`. <br />
    
Instantiation:
===
The instantiation of the Jdatabase object requires a host, user, password(passwd), and database name(db). The optional arguments are
charset, which defaults to `"utf8"`; port, which defaults to `3306`; ssl, which defaults to `True`; and autocommit, which
defaults to `True`. <br />
```python
from jdatabase import Jdatabase
jdb = Jdatabase(host="db_hostname", user="db_username", passwd="db_password", db="db_name" )
``` 

Table Methods:
===

get_table_names()
---
Method to get the names of all the tables in the connected database. <br />
**Returns a list of str table names.** <br />
```python
jdb.get_table_names()
```
> Use of this method also updates self.table_names and self.stable_names for self use. <br />
##### output:
```
['SYSTEM_TABLE', 'table_name', 'table_name2', ...]
```

get_cleaned_table_names()
---
Method to get the names of all non-system tables in the connected database. <br />
**Returns a list of str table names.** <br />
```python
jdb.get_cleaned_table_names()
```
> This method DOES NOT update self.table_names and self.stable_names. <br />
##### output: 
```
['table_name', 'table_name2', ...]
```

check_for_table(name)
---
Method to check for a table, named name, in the database. <br />
**Returns `True` if table found, `False` if not.** <br />
```python
jdb.check_for_table("table_name")
```

create_table(name, {column_name:[parms]})
---
>> [`create_table_if_false_check()`](#create_table_if_false_checkname-column_nameparms) is recommended for all table creation. <br />

Creates a table in the database. <br />
**Returns the rowcount for the query, should be `0`.** <br />
```python
jdb.create_table("table_name", {"jd":["VARCHAR(128)", "PRIMARY KEY"], "column_name":["DATATYPE", "DEFAULT VALUE"]})
```
```python
# with auto primary key insertion
jdb.create_table("table_name", {"column_name":["DATATYPE", "DEFAULT VALUE"], "column2_name":["DATATYPE", "DEFAULT VALUE"]})
```
> The jdatabase package automatically adds a jd column as the primary key column (if a primary key column is not included). <br />

> The recommend DEFAULT VALUE is `NOT NULL`. <br />

create_table_if_not_exists(name, {column_name:[parms]})
---
>> [`create_table_if_false_check()`](#create_table_if_false_checkname-column_nameparms) is recommended for all table creation. <br />

Creates a table in the database, if the table name is not present in the database, with database level existence check. <br />
**Returns the rowcount for the query, should be `0`.** <br />
```python
jdb.create_table_if_not_exists("table_name", {"jd":["VARCHAR(128)", "PRIMARY KEY"], "column_name":["DATATYPE", "DEFAULT VALUE"]})
```
```python
# with auto primary key insertion
jdb.create_table_if_not_exists("table_name", {"column_name":["DATATYPE", "DEFAULT VALUE"], "column2_name":["DATATYPE", "DEFAULT VALUE"]})
```
> The jdatabase package automatically adds a jd column as the primary key column (if a primary key column is not included). <br />

> The recommend DEFAULT VALUE is `NOT NULL`. <br />

create_table_if_false_check(name, {column_name:[parms]})
---
Creates a table in the database, if the table name is not present in the database, with a query call existence check. <br />
**Returns the rowcount for the query, should be `0`.** <br />
```python
jdb.create_table_if_false_check("table_name", {"jd":["VARCHAR(128)", "PRIMARY KEY"], "column_name":["DATATYPE", "DEFAULT VALUE"]})
```
```python
# with auto primary key insertion
jdb.create_table_if_false_check("table_name", {"column_name":["DATATYPE", "DEFAULT VALUE"], "column2_name":["DATATYPE", "DEFAULT VALUE"]})
```
> The jdatabase package automatically adds a jd column as the primary key column (if a primary key column is not included). <br />

> The recommend DEFAULT VALUE is `NOT NULL`. <br />

Data Methods:
===

get_one(name, [fields], (where, [parms]), (order, parms))
---
Gets one row of data from the table in the connected database, named name. <br />
**Returns the row of data.** <br />
```python
row = jdb.get_one("table_name", ["field1", "field2"])
```
```python
# hard-coded condition
row = jdb.get_one("table_name", where=("jd=a1"))
```
```python
# condition
row = jdb.get_one("table_name", where=("jd=%s", ["jd_val"]))
```
```python
# extended condition
row = jdb.get_one("table_name", where=("jd=%s and column1=%s", ["jd_val", "column1_val"]))
```
```python
# ordered by DESC
row = jdb.get_one("table_name", order=("field", "DESC"))
```
> Only the name value is required for get_one(). <br />
##### output:
```
("jd", "col1val", "col2val", ...)
```

get_all(name, [fields], (where, [parms]), (order, parms))
---
Gets all of the data from the table in the connected database, named name. <br />
**Returns the data.** <br />
```python
row = jdb.get_all("table_name", ["field1", "field2"])
```
```python
# hard-coded condition
row = jdb.get_all("table_name", where=("jd=a1"))
```
```python
# condition
row = jdb.get_all("table_name", where=("jd=%s", ["jd_val"]))
```
```python
# extended condition
row = jdb.get_all("table_name", where=("jd=%s and column1=%s", ["jd_val", "column1_val"]))
```
```python
# ordered by DESC
row = jdb.get_all("table_name", order=("field", "DESC"))
```
> Only the name value is required for get_all(). <br />
##### output:
```
(("jd", "col1val", "col2val", ...),
 ("jd", "col1val", "col2val", ...), 
 ...)
```

insert(name, {data})
---
Inserts a row of data into the table, named name, in the connected database. <br />
**Returns the rowcount for query.** <br />
```python
jdb.insert("table_name", {"column1name": val, "column2name": xval})
```
> `vals` should be the same type as the column in the table. <br />

insert_batch(name, [{data1}, {data2}])
---
Inserts a batch of data into the table, named name, in the connected database. <br />
**Returns rowcount for query.** <br />
```python
jdb.insert("table_name", [{"column1name": val, "column2name": xval}, {"column1name": val2, "column2name": xval2}])
```
> `vals` should be the same type as the column in the table. <br />

update(name, {data}, (where))
---
Updates data in the table, named name, in the connected database. <br />
**Returns rowcount for query.** <br />
```python
jdb.update("table_name", {"column1name": val, "column2name": xval}, where=("column1name=%s", ["row_val"]))
```
> `vals` should be the same type as the column in the table. <br />

insert_or_update(name, {data}, key)
---
Insert data into or updates the data in the table, named name, in the connected database using a column, key, as a key for the comparision check between the parameter data and the data in the table. <br />
**Returns rowcount for query.** <br />
```python
jdb.insert_or_update("table_name", {"column1name": val, "column2name": xval}, "column1name")
```
> `vals` should be the same type as the column in the table. <br />

delete(name, (where))
---
Delete row(s) in the table, named name, in the connected database, based on where condition. <br />
**Returns rowcount for query.** <br />
```python
# delete entire table
jdb.delete("table_name")
```
```python
# delete with where condition
jdb.delete("table_name", where=("jd=%s", ["val"]))
```

last_id()
---
Gets the last insert id. <br />
**Returns the last insert id.** <br />
```python
jdb.last_id()
```

last_query()
---
Gets the last executed query. <br />
**Returns the last executed query.** <br />
```python
jdb.last_query()
```


Class Methods:
===

connect()
---
Method to establish a connection to the database. Automatically run on instantiation. <br />
**Returns the database type of either `MySQL` or `PostgreSQL` in the form of a str.** <br />
```python
jdb.connect()
```

is_open()
---
Method to check if the connection object's connection to the database is open. <br />
**Returns `True` if the connection is open, `False` if not.** <br />
```python
jdb.is_open()
```

is_connected()
---
Method to check if the database is open and if not if there is a connection error. <br />
**Returns `True` if the connection is open, or if it was reestablished, or the connection error.** <br />
```python
jdb.is_connected()
```

query(sql, [parms])
---
Method to execute a raw SQL query, with parms replacing `%s`s in the sql. <br />
**Returns the cursor object.** <br />
```python
jdb.query("SELECT * FROM table_name WHERE %s=%s;", ['col1','select_me'])
```
> parms are NOT required. <br />

> parms are required for any variable use, f"" strings DO NOT work. <br />

commit()
---
Method to commit all current pending changes to the database. This method is only needed when autocommit is set to `False` in instantiation. <br />
```python
jdb.commit()
```

close()
---
Method to close the connection to the database. <br />
```python
jdb.close()
```

reconnect()
--- 
Method to close the connection to the database, if it is open, and then reopen the connection. <br />
```python
jdb.reconnect()
```

`__str__`
---
**Returns the name of the database that the jdatabase object is connected to.** <br />
```python
str(jdb)
```
##### output:
```
"database_name"
```

Footnote:
===
This package was inspired by my need for an easier way to interact with databases in Python, and the [simplemysql](https://github.com/knadh/simplemysql "simplemysql") package.
