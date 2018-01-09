import sqlite3

conn = sqlite3.connect('rfid.db')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

# Create table
c.execute(
    '''create table if not exists users (_id integer PRIMARY KEY AUTOINCREMENT, name text, email text unique, knock text, password text, uid text unique );''')

c.execute(
    '''CREATE table if not exists access(_time datetime, attempts int,battery real, user int, door int , FOREIGN KEY(user) REFERENCES users(_id), FOREIGN KEY(door) REFERENCES doors(_id) );''')
c.execute('''create table if not exists doors(_id integer PRIMARY KEY AUTOINCREMENT, num int, location text);''')
c.execute('''create table if not exists door_to_user(_id integer PRIMARY KEY AUTOINCREMENT, _user int, _door int , FOREIGN KEY(_user) REFERENCES users(_id), FOREIGN KEY(_door) REFERENCES doors(_id) );
	''')

if __name__ == "__main__":
    #users
    c.execute(
        '''insert into users(name , email , knock , password , uid ) values
         ('daniela sousa', 'dc@ua.pt', '[345, 345]','password', '0412A3F4G4A380');''')
    c.execute(
        '''insert into users(name , email , knock , password , uid ) values
         ('pedro silva', 'ps@ua.pt', '[345, 345]','password', '0412A3D5G4A380');''')
    c.execute(
        '''insert into users(name , email , knock , password , uid ) values
         ('David Maio', 'dm@ua.pt', '[345, 345]','password', '0412A3F5G4A380');''')
    #doors
    c.execute('insert into doors(num , location ) values (?, ?);', (1, 'deti'))
    c.execute('insert into doors(num , location ) values (?, ?);', (10, 'bio'))
    c.execute('insert into doors(num , location ) values (?, ?);', (100, 'deti'))

    #door_tu_users
    c.execute('insert into door_to_user(_user , _door) values (?, ?);', (1, 1))
    c.execute('insert into door_to_user(_user , _door) values (?, ?);', (2, 1))
    c.execute('insert into door_to_user(_user , _door) values (?, ?);', (1, 2))

    #access
    c.execute('''insert into access(_time, user, door, attempts, battery) values (?,?,?, ?,?);''',
              ('2016-05-18 10:57:30', 1, 1, 1, 30.0))
    c.execute('''insert into access(_time, user, door, attempts, battery) values (?,?,?, ?,?);''',
              ('2017-05-18 10:57:30', 1, 1, 1, 40.0))
    c.execute('''insert into access(_time, user, door, attempts, battery) values (?,?,?, ?,?);''',
              ('2018-05-18 10:57:30', 1, 2, 1, 100.0))
    conn.commit()
    conn.close()
