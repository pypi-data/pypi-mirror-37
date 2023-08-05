# coding:utf8


import sqlite3


# 建一个数据库
def create_sql():
    sql = sqlite3.connect("user_data.db")
    sql.execute("CREATE TABLE IF NOT EXISTS \
            Writers(username, password)")
    sql.close()


def get_cursor():
    create_sql()
    conn = sqlite3.connect("user_data.db")
    return conn.cursor()


def insert_user(username, pwd):

    if (fetch_username() is None) | (fetch_pwd is None):
        sql = sqlite3.connect("user_data.db")
        sql.execute("insert into Writers(username,password) values(?,?)",
                (username, pwd))

        sql.commit()
        # print "添加成功"
        sql.close()


def fetch_username():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    return c.execute("select username from Writers").fetchone()


def fetch_pwd():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    return c.execute("select password from Writers").fetchone()