from __future__ import print_function
import sqlite3
import os


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def db_connect(db_fn, verbosity=1):
    try:
        db = sqlite3.connect(db_fn)
        db.text_factory = str
        db.row_factory = sqlite3.Row
        return db
    except Exception as e:
        if verbosity >= 1:
            print("connect_db exception: %s" % e)
        return False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def db_recreate(db_fn, verbosity=1):
    try:
        if os.path.isfile(db_fn):
            os.remove(db_fn)
        return db_connect(db_fn)
    except Exception as e:
        if verbosity >= 1:
            print("db_recreate_table exception: %s" % e)
        return False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def db_get_table_names(db):
    sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    print(sql)
    res = db_select_query(db, sql)
    tmplist = list()
    for row in res:
        tmplist.append(row[0])
    return tmplist


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def db_create_table(db, sql, verbosity=1):
    try:
        cur = db.cursor()
        cur.execute(sql)

    except Exception as e:
        if verbosity >= 1:
            print("db_create_table exception: %s" % e)
        return False

    return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def db_drop_table(db, tbl_name, verbosity=1):
    try:
        sql="DROP TABLE IF EXISTS %s" % tbl_name
        cur = db.cursor()
        cur.execute(sql)

    except Exception as e:
        if verbosity >= 1:
            print("db_drop_table exception: %s" % e)
        return False

    return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def db_insert_query(db, sql, data, verbosity=1):
    try:
        cur = db.cursor()
        cur.execute(sql, data)
        db.commit()
        i = cur.lastrowid

    except Exception as e:
        print("db_insert_query exception: %s" % e)
        return False

    return i


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def db_insert_query_many(db, sql, data_list, verbosity=1):
    try:
        cur = db.cursor()
        cur.executemany(sql, data_list)
        db.commit()
        i = cur.lastrowid

    except Exception as e:
        if verbosity >= 1:
           print("db_insert_query_many exception: %s" % e)
        return False

    return i


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def db_select_query(db, sql, verbosity=1):
    try:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

    except Exception as e:
        if verbosity >= 1:
            print( "db_select_query exception: %s" % e)
            return False

    return rows


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def db_delete_query(db, sql, verbosity=1):
    try:
        cur = db.cursor()
        cur.execute(sql)
        db.commit()

    except Exception as e:
        if verbosity >= 1:
            print( "db_delete_query exception: %s" % e)
            return False

    return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def db_update_query(db, sql, verbosity=1):
    try:
        cur = db.cursor()
        cur.execute(sql)
        db.commit()

    except Exception as e:
        if verbosity >= 1:
            print( "db_update_query exception: %s" % e)
            return False

    return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def db_is_table(db, tbl_name, verbosity=1):
    sql = """
        SELECT name FROM sqlite_master WHERE type='table' and name='%s'
    """ % tbl_name
    res = db_select_query(db, sql, verbosity)
    if len(res) == 0:
        return False

    return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def run():
    return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
if __name__ == "__main__":
    run()
