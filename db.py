import sqlite3

class DataBase(object):
	"""docstring for DataBase"""
	def __init__(self, file_path='rfid.db' ):
				
		#connect to database
		self.conn = sqlite3.connect(file_path)
		self.c = self.conn.cursor()
		self.c.execute("PRAGMA foreign_keys = ON")
		
	def validate(self, list_knock , _pass, door_id):
		self.c.execute('select _id, knock from users where uid=?', _pass)
		r = self.c.fetchone()
		if r ==None:
			return (False, "UID" + _pass + "not in database" )

		db_user_id = r[0]
		db_knock = r[1]
		self.c.execute('select _id from door_to_user where _user =? and _door =?',(db_user_id, door_id))
		r = self.c.fetchone()
		if r ==None:
			return (False, "User has no access to door " + door_id )
		db_door_id = r[0]
		if not self.validate_knock(db_knock, list_knock) :
			return (False, "Wrong knock sequence" + list_knock  )

		self.insert_access('time', db_user_id , db_door_id, 1 )
		return (True, "Successful!" ) 


	def validate_knock(self, k_stored , k1):
		return True

	def insert_user(self,name, email, knock, _pass, uid):
		try:
			self.c.execute('insert into users(name , email , knock , password , uid ) values (?, ?, ?,?, ?);', name, email, knock, _pass, uid)
			self.conn.commit()
			return(1, 'Successful!')
		except Exception, e:
			print e
			return (0, 'ERROR: '+str(e))

	def insert_door(self,num, location):
		try:
			self.c.execute('select * from doors where num =? and location =?',( num , location))
			if self.c.fetchall() == [] :
				self.c.execute('insert into doors(num , location ) values (?, ?);',( num , location))
				self.conn.commit()
				return(1, 'Successful!')
			else:
				raise Exception("Unique num and location")
		except Exception, e:
			print e
			return (0, 'ERROR: '+str(e))

	def insert_door_to_user(self,user, door):
		try:
			self.c.execute('select * from door_to_user where _user =? and _door =?',(user, door))
			if self.c.fetchall() == [] :
				self.c.execute('''insert into door_to_user(_user, _door) values (?,?);''', (user, door))
				self.conn.commit()
				return(1, 'Successful!')
			else:
				raise Exception("Unique (_user, _door)")
		except Exception, e:
			print e
			return (0, 'ERROR: '+str(e))

	def insert_access(self,_time, user, door, attempts= None):
		try:
			self.c.execute('select * from access where user =? and door =? amd _time=?',(user, door, _time))
			if self.c.fetchall() == [] :
				self.c.execute('''insert into access(_time, user, door, attempts) values (?,?);''', (_time, user, door, attempts))
				self.conn.commit()
				return(1, 'Successful!')
			else:
				raise Exception("Unique (user, door, time)")
		except Exception, e:
			print e
			return (0, 'ERROR: '+str(e))
	
	def remove_user_from_door(self,user, door):
		try:
			self.c.execute('''delete from door_to_user where _user=? and _door=? ''', (user, door))
			self.conn.commit()
			return(1, 'Successful!')
		except Exception, e:
			print e
			return (0, 'ERROR: '+str(e))
	
