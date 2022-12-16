import pymysql
import json

conn = pymysql.connect(
    host="ezhoop.ceyb9flfxbi4.us-east-1.rds.amazonaws.com",
    port=3306,
    user="admin",
    password="Yp3SQFke17fRB4K5VfgX",
    db="ezhoop"
)


def add_game(uid, target, score, miss):
    cur = conn.cursor()
    cur.execute("INSERT INTO games (uid, target, score, miss) VALUES (%s, %s, %s, %s)", (uid, target, score, miss))
    conn.commit()


def add_user_details(uid, dob, firstName, lastName, gender, country):
    cur = conn.cursor()
    cur.execute("INSERT INTO userDetails (uid, dob, firstName, lastName, gender, country) VALUES (%s, %s, %s, %s, %s, %s)", (uid, dob, firstName, lastName, gender, country))
    conn.commit()


def get_user_details(uid):
    cur = conn.cursor()
    cur.execute("SELECT * FROM userDetails WHERE uid = %s", uid)
    res = cur.fetchone()
    return json.dumps(res, default=str)


# def get_details():
#     cur = conn.cursor()
#     cur.execute("SELECT *  FROM Details")
#     details = cur.fetchall()
#     return details
