import sqlite3
conn = sqlite3.connect('rfid.db')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

# Create table
c.execute('''create table if not exists users (_id integer PRIMARY KEY AUTOINCREMENT, name text, email text unique, knock text, password text, uid text unique );''')

c.execute('''CREATE table if not exists access(_time datetime, attempts int, user int, door int , FOREIGN KEY(user) REFERENCES users(_id), FOREIGN KEY(door) REFERENCES doors(_id) );''')
c.execute('''create table if not exists doors(_id integer PRIMARY KEY AUTOINCREMENT, num int, location text);''')
c.execute('''create table if not exists door_to_user(_id integer PRIMARY KEY AUTOINCREMENT, _user int, _door int , FOREIGN KEY(_user) REFERENCES users(_id), FOREIGN KEY(_door) REFERENCES doors(_id) );
	''')

if __name__ == "__main__":
	# Insert a row of data
	#c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
	try:
		c.execute('''insert into users(name , email , knock , password , uid ) values ('daniela', 'email', 'knox','password', 'uid');''')
	except Exception, e:
		print "already exists1", e

	try:
		c.execute('select * from doors where num =? and location =?',( 1, 'atrio'))
		if c.fetchall() == [] :
			c.execute('insert into doors(num , location ) values (?, ?);',( 1, 'atrio'))
		else:
			raise Exception("Unique num and location")
	except Exception, e:
		print "already exists2", e

	# try:
	# 	c.execute('insert into door_to_user(_user , _door) values (?, ?);',( 1, 1))
	
	# except Exception, e:
	# 	print "already exists3", e
	

	

	
	conn.commit()
	#c.execute("SELECT * FROM doors ;")
	#print c.fetchone()

	for row in c.execute('SELECT door_to_user._user, users.email, users.name from door_to_user cross join users where door_to_user._door = ?  and users._id = door_to_user._user', 1):
	
	    
	    print row

	
	

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
