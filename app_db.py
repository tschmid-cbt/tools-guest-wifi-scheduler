import sqlite3

def connect():
    conn=sqlite3.connect("wifi.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS wifi (id integer PRIMARY KEY, user text, starttime text, endtime text, duration integer, password text)")
    conn.commit()
    conn.close()

def insert(user,starttime,endtime,duration,password):
    conn=sqlite3.connect("wifi.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO wifi VALUES(NULL,?,?,?,?,?)",(user,starttime,endtime,duration,password))
    conn.commit()
    conn.close()

def view():
    conn=sqlite3.connect("wifi.db")
    cur=conn.cursor()
    cur.execute("SELECT * from wifi")
    rows=cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn=sqlite3.connect("wifi.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM wifi WHERE id=?", (id,))
    conn.commit()
    conn.close()

connect()
