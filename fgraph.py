import sqlite3
import random
import string
import os, os.path
import json
import calendar

DB_STRING = 'rfid.db'

_months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
m = ["January", "February", "March", "April", "May", "June", 'July', 'August', 'September', 'October', 'November',
     'December']


# CREATE table if not exists access(_time datetime, attempts int, user int, door int);*/
# /*insert into access values('2016-10-04 23:12:03', 1, 10, 3)*/
##---GET---functions
##
def get_graph_years(a1, a2, door=None, user=None):
    ''' a1 and a2 are numbers year '''
    with sqlite3.connect(DB_STRING) as conn:
        c = conn.cursor()
        # initialize
        x_label = int(a2 - a1 + 1) * ['']
        y_label = int(a2 - a1 + 1) * [0]
        for i in range(0, a2 - a1 + 1):
            x_label[i] = str(a1 + i)
            s1 = x_label[i] + '-01-01'
            s2 = x_label[i] + '-12-31'
            if door == None and user == None:
                c.execute('select count(*) from access where date(_time) >= date(?) and date(_time) <= date(?) ;',
                          (s1, s2))
            elif door == None:
                c.execute(
                    'select count(*) from access where date(_time) >= date(?) and date(_time) <= date(?) and user = ?;',
                    (s1, s2, user))
            elif user == None:
                c.execute(
                    'select count(*) from access where date(_time) >= date(?) and date(_time) <= date(?) and door = ?;',
                    (s1, s2, door))
            else:
                c.execute(
                    'select count(*) from access where date(_time) >= date(?) and date(_time) <= date(?) and user = ? and door=?;',
                    (s1, s2, user, door))
            y_label[i] = c.fetchone()[0]

        return json.dumps({"result": {"x": x_label, "y": y_label}})


def get_graph_year(a1, door=None, user=None):
    ''' a1  are numbers year '''
    with sqlite3.connect(DB_STRING) as conn:
        c = conn.cursor()
        # initialize
        x_label = m
        y_label = 12 * [0]
        for i in range(0, 12):  # month
            s1 = str(a1) + '-' + _months[i] + '-01'
            s2 = str(a1) + '-' + _months[i] + '-' + str(calendar.monthrange(a1, i + 1)[1])
            if door == None and user == None:
                c.execute('select count(*) from access where date(_time) >= date(?) and date(_time) <= date(?) ;',
                          (s1, s2))
            elif door == None:
                c.execute(
                    'select count(*) from access where date(_time) >= date(?) and date(_time) <= date(?) and user = ?;',
                    (s1, s2, user))
            elif user == None:
                c.execute(
                    'select count(*) from access where date(_time) >= date(?) and date(_time) <= date(?) and door = ?;',
                    (s1, s2, door))
            else:
                c.execute(
                    'select count(*) from access where date(_time) >= date(?) and date(_time) <= date(?) and user = ? and door=?;',
                    (s1, s2, user, door))
            y_label[i] = c.fetchone()[0]

        return json.dumps({"result": {"x": x_label, "y": y_label}})


def get_graph_day(a1, door=None, user=None):
    ''' a1  is a string like '2017-01-12' '''
    with sqlite3.connect(DB_STRING) as conn:
        c = conn.cursor()
        # initialize
        x_label = 24 * ['']
        y_label = 24 * [0]
        for i in range(0, 24):  # hour
            x_label[i] = str(i + 1) + ':00'
            s1 = str(a1) + ' ' + str(i + 1) + ':00:00'
            s2 = str(a1) + ' ' + str(i + 1) + ':59:59'
            if door == None and user == None:
                c.execute(
                    'select count(*) from access where datetime(_time) >= datetime(?) and datetime(_time) <= datetime(?) ;',
                    (s1, s2))
            elif door == None:
                c.execute(
                    'select count(*) from access where datetime(_time) >= datetime(?) and datetime(_time) <= datetime(?) and user = ?;',
                    (s1, s2, user))
            elif user == None:
                c.execute(
                    'select count(*) from access where datetime(_time) >= datetime(?) and datetime(_time) <= datetime(?) and door = ?;',
                    (s1, s2, door))
            else:
                c.execute(
                    'select count(*) from access where datetime(_time) >= datetime(?) and datetime(_time) <= datetime(?) and user = ? and door=?;',
                    (s1, s2, user, door))
            y_label[i] = c.fetchone()[0]

        return json.dumps({"result": {"x": x_label, "y": y_label}})


def get_graph_month(a1, door=None, user=None):
    ''' a1  is a string like '2017-01' '''
    with sqlite3.connect(DB_STRING) as conn:
        c = conn.cursor()
        # initialize
        n_days = calendar.monthrange(int(a1.split('-')[0]), int(a1.split('-')[1]))[1]  # number of days in this month
        x_label = n_days * ['']
        y_label = n_days * [0]
        for i in range(0, n_days):  # day
            x_label[i] = str(i + 1)
            if i + 1 < 10:
                s1 = a1 + '-0' + str(i + 1) + ' 00:00:00'
                s2 = a1 + '-0' + str(i + 1) + ' 24:00:00'
            else:
                s1 = a1 + '-' + str(i + 1) + ' 00:00:00'
                s2 = a1 + '-' + str(i + 1) + ' 24:00:00'
            if door == None and user == None:
                c.execute(
                    "select count(*) from access where datetime(_time) >= datetime(?) and datetime(_time) < datetime(?) ;",
                    (s1, s2))
            elif door == None:
                c.execute(
                    'select count(*) from access where datetime(_time) >= datetime(?) and datetime(_time) < datetime(?) and user = ?;',
                    (s1, s2, user))
            elif user == None:
                c.execute(
                    'select count(*) from access where datetime(_time) >= datetime(?) and datetime(_time) < datetime(?) and door = ?;',
                    (s1, s2, door))
            else:
                c.execute(
                    'select count(*) from access where datetime(_time) >= datetime(?) and datetime(_time) < datetime(?) and user = ? and door=?;',
                    (s1, s2, user, door))
            y_label[i] = c.fetchone()[0]

        return json.dumps({"result": {"x": x_label, "y": y_label}})


def get_table_all_doors():
    with sqlite3.connect(DB_STRING) as con:
        c = con.cursor()
        result = []
        for _id, num, location in c.execute('SELECT _id, num, location FROM doors ;'):
            with sqlite3.connect(DB_STRING) as con2:
                c2 = con2.cursor()
                c2.execute('SELECT _user from door_to_user where _door = ? ', str(_id))
                f = []
                res = c2.fetchall()
                if len(res) > 0:
                    for x in res :
                        f = f + [x[0]]
                    result = result + [[num, _id, location, len(f), f,
                                        '<input class="btn" type="button" value="See Users" onClick="selectDoor(' + str(
                                            _id) + ')" />' '<input style="margin-left:10px" class="btn" type="button" value="Add User" onClick="add_user(' + str(
                                            _id) + ')" />' '<input style="margin-left:10px" class="btn" type="button" value="Edit" onClick="edit_door(' + str(
                                            _id) + ')" />']]
                else:
                    result = result + [[num, _id, location, len(f), f,
                                        '<input class="btn" type="button" value="Add User" onClick="add_user(' + str(
                                            _id) + ')" />' '<input style="margin-left:10px" class="btn" type="button" value="Edit" onClick="edit_door(' + str(
                                            _id) + ')" />']]


        return json.dumps({"data": result})


def get_table_all_access():
    with sqlite3.connect(DB_STRING) as con:
        c = con.cursor()
        result = []
        for _time, email, num, location in c.execute(
                'SELECT access._time, users.email, doors.num, doors.location FROM doors cross join users cross join access where access.user = users._id and access.door = doors._id ;'):
            result = result + [[_time, email, num, location]]

        return json.dumps({"data": result})


def get_table_users_to_door(doorId):
    with sqlite3.connect(DB_STRING) as con:
        c = con.cursor()
        result = []
        for _id, email, name in c.execute(
                'SELECT door_to_user._user, users.email, users.name from door_to_user cross join users where door_to_user._door = ?  and users._id = door_to_user._user',
                str(doorId)):
            result = result + [[_id, email, name,
                                '<button class="btn" > <img class="delete" src="/static/img/delete.png" height="20" > </button>']]

        return json.dumps({"data": result})


def get_id_from_email(email):
    with sqlite3.connect(DB_STRING) as con:
        c = con.cursor()
        result = []
        print
        email
        for _id, name in c.execute('SELECT _id, name from  users where email = ?  ', (email,)):
            result = result + [_id, name]

        return json.dumps({"result": result})


def get_table_users():
    with sqlite3.connect(DB_STRING) as con:
        c = con.cursor()
        result = []
        for _id, name, email, knock, password, uid in c.execute('SELECT * FROM users ;'):
            result = result + [[email, _id, name, knock, uid, password,
                                '<input  class="btn" type="button" value="Edit" onClick="edit_user(' + str(
                                    _id) + ')" />']]
        return json.dumps({"data": result})


def get_home():
    with sqlite3.connect(DB_STRING) as con:
        c = con.cursor()
        result = {"users": 0, "active_u": 0, "doors": 0, "active_d": 0}
        for count in c.execute('select count(*) from users;'):
            result["users"] = count
        for count in c.execute('select count(distinct _user) from door_to_user ;   '):
            result["active_u"] = count
        for count in c.execute('select count(*) from doors;'):
            result["doors"] = count
        for count in c.execute('select count(distinct _door) from door_to_user ;   '):
            result["active_d"] = count

        return json.dumps({"result": result})


if __name__ == '__main__':
    conn = sqlite3.connect('rfid.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON")
    # c.execute('insert into access values(\'2016-10-04 23:12:03\', 1, 1, 1)')
    # c.execute('insert into access values(\'2016-10-05 23:12:03\', 1, 1, 1)')
    # c.execute('insert into access values(\'2016-10-06 23:12:03\', 1, 1, 1)')
    # c.execute('insert into access values(\'2016-10-04 22:12:03\', 1, 1, 1)')
    # conn.commit()
    # conn.close()
    print
    get_graph_year(2016)
    print
    get_graph_years(2015, 2017)

    print
    get_graph_month('2016-10')

    print
    get_graph_day('2016-10-04')
