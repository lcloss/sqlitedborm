<<<<<<< HEAD
# sqlitedborm
SQLite DB ORM for Python
=======
# sqlitedborm Package
====================

Provides an easy way to handle with SQLite3 databases.

## Source
------

See `Project's Github <https://github.com/lcloss/sqlitedborm>`_.

## Installation
------------

```python
python3 -m pip install sqlitedborm
```

## Usage
-----

### Import
```python
import sqlitedborm
```

### Connection
```python
    db = sqlitedborm.Database('databasename')
```
The command above will connect to databasename.sqlite3 database, located on the same path.
If you want another extension, you can specify:
```python
    db = sqlitedborm.Database('databasename.db')
```
The command above will connect to databasename.db database.

### Tables
```python
    tbContacts = sqlitedborm.Table('contacts')
```
The command above will create a model for 'contacts' table.


### SQL Operations

#### Insert
```python
    contact = {'name': 'Contact name', 'email': 'contact@example.com', 'phone': '999-999-999'}
    tbContacts.insert(contact)
```

### Update
```python
    id = 3
    contact = {'name': 'Contact name', 'email': 'contact@example.com', 'phone': '999-999-999'}
    tbContacts.update(id, contact)
```

### Delete
```python
    id = 3
    tbContacts.delete(id)
```

### Select by ID
```python
    id = 1
    res = tbContacts.get(id)
    if len(res) > 0:
        print(res[0])
    else:
        print('Not found')
```

### Select All
```python
    res = tbContacts.listAll()
    if len(res) > 0:
        for row in res:
            print(row)
    else:
        print('Not found')
```

Documentation
--------------

>>>>>>> Initial version
