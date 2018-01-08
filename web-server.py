import cherrypy
import sqlite3
import random
import string
import os, os.path
import json
from Server.db import *
from fgraph import *

DB_STRING = 'rfid.db'

SESSION_KEY = '_cp_username'

def check_credentials(username, password):
	print "ola1"
	"""Verifies credentials for username and password.
	Returns None on success or a string describing the error on failure"""
	# Adapt to your needs
	if username in ('joe', 'steve') and password == 'secret':
		return None
	else:
		return u"Incorrect username or password."
	
	# An example implementation which uses an ORM could be:
	# u = User.get(username)
	# if u is None:
	#     return u"Username %s is unknown to me." % username
	# if u.password != md5.new(password).hexdigest():
	#     return u"Incorrect password"

def check_auth(*args, **kwargs):
	print "ola2"
	"""A tool that looks in config for 'auth.require'. If found and it
	is not None, a login is required and the entry is evaluated as a list of
	conditions that the user must fulfill"""
	conditions = cherrypy.request.config.get('auth.require', None)
	if conditions is not None:
		username = cherrypy.session.get(SESSION_KEY)
		if username:
			cherrypy.request.login = username
			for condition in conditions:
				# A condition is just a callable that returns true or false
				if not condition():
					raise cherrypy.HTTPRedirect("/auth/login")
		else:
			raise cherrypy.HTTPRedirect("/auth/login")
	
cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)

def require(*conditions):
	print "ola3"
	"""A decorator that appends conditions to the auth.require config
	variable."""
	def decorate(f):
		if not hasattr(f, '_cp_config'):
			f._cp_config = dict()
		if 'auth.require' not in f._cp_config:
			f._cp_config['auth.require'] = []
		f._cp_config['auth.require'].extend(conditions)
		return f
	return decorate
# Conditions are callables that return True
# if the user fulfills the conditions they define, False otherwise
#
# They can access the current username as cherrypy.request.login
#
# Define those at will however suits the application.

def member_of(groupname):
	def check():
		# replace with actual check if <username> is in <groupname>
		return cherrypy.request.login == 'joe' and groupname == 'admin'
	return check

def name_is(reqd_username):
	return lambda: reqd_username == cherrypy.request.login

# These might be handy

def any_of(*conditions):
	"""Returns True if any of the conditions match"""
	def check():
		for c in conditions:
			if c():
				return True
		return False
	return check

# By default all conditions are required, but this might still be
# needed if you want to use it inside of an any_of(...) condition
def all_of(*conditions):
	"""Returns True if all of the conditions match"""
	def check():
		for c in conditions:
			if not c():
				return False
		return True
	return check

# Controller to provide login and logout actions
class AuthController(object):
	
	def on_login(self, username):
		"""Called on successful login"""
	
	def on_logout(self, username):
		"""Called on logout"""
	
	def get_loginform(self, username, msg="Enter login information", from_page="/"):
	    return """<html><body>
	        <form method="post" action="/auth/login">
	        <input type="hidden" name="from_page" value="%(from_page)s" />
	        %(msg)s<br />
	        Username: <input type="text" name="username" value="%(username)s" /><br />
	        Password: <input type="password" name="password" /><br />
	        <input type="submit" value="Log in" />
	    </body></html>""" % locals()
	
	@cherrypy.expose
	def login(self, username=None, password=None, from_page="/"): 
		print '\n\n ola \n\n'
		if username is None or password is None:
			return self.get_loginform("", from_page=from_page)
		
		error_msg = check_credentials(username, password)
		if error_msg:
			return self.get_loginform(username, error_msg, from_page)
		else:
			cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
			self.on_login(username)
			raise cherrypy.HTTPRedirect(from_page or "/")
	
	@cherrypy.expose
	def logout(self, from_page="/"):
		sess = cherrypy.session
		username = sess.get(SESSION_KEY, None)
		sess[SESSION_KEY] = None
		if username:
			cherrypy.request.login = None
			self.on_logout(username)
		raise cherrypy.HTTPRedirect(from_page or "/")




@cherrypy.expose

class WebService(object): #restricted
	_cp_config = {
		'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
		'tools.response_headers.on': True,
		'tools.response_headers.headers': [('Content-Type', 'text/plain')],
		'auth.require': [member_of('admin')]
	}
	
	# all methods in this controller (and subcontrollers) is
	# open only to members of the admin group
	@cherrypy.tools.accept(media='text/plain')
	def GET(self,  t = None, doorId=None,_=None,  email= None, user=None, d1= None, d2= None):
		t = int(t)
		if t == 1 :
			return get_table_all_doors()
		if t == 2 :
			return get_table_users_to_door(doorId)
		if t == 3 :
			return get_id_from_email(email)
		if t == 4 :
			return get_table_users()
		if t == 5 :
			return get_graph_years(int(d1), int(d2), doorId, user)
		if t == 6 :
			return get_graph_year(int(d1), doorId, user)
		if t == 7 :
			return get_graph_month(str(d1), doorId, user)
		if t == 8 :
			return get_graph_day(str(d1), doorId, user)
		if t== 9:
			return get_table_all_access()
		if t== 10:
			return get_home()

	def POST(self, length=8):
		some_string = ''.join(random.sample(string.hexdigits, int(length)))
		cherrypy.session['mystring'] = some_string
		some_string = {"result": [some_string] }
		return json.dumps(some_string)

	def POST(self, door, user):
		db = DataBase()
		print door
		print user
		res, msg = db.insert_door_to_user(user, door)
		return json.dumps({"result" : msg})
		db.conn.close()

	def PUT(self, _id, num, loc):
		with sqlite3.connect(DB_STRING) as conn:
			c= conn.cursor()
			try:
				c.execute("UPDATE doors SET num=?, location=? WHERE _id=?",
				  (num, loc, _id))
				conn.commit()
				return json.dumps({"result" : [1, "Successful!"]})
			except Exception, e:
				return json.dumps({"result" : [0, "ERROR:" + str(e)]})
			

	def DELETE(self, user, door):
		db = DataBase()

		print door
		print user
		res, msg = db.remove_user_from_door(user, door)
		return json.dumps({"result" : msg})
		db.conn.close()

class WebPage(object): #Root
	_cp_config = {
		'tools.sessions.on': True,
		'tools.auth.on': True,
		'tools.staticdir.root': os.path.abspath(os.getcwd())
	}

	"""This page is open to everyone"""
	@cherrypy.expose
	def login(self):
		return open('./admin-page/login.html')
		

	@cherrypy.expose
	@require()
	def index(self):
		return open('./admin-page/index.html')
			

class Public(object):
	_cp_config = {
		
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './admin-page'
		
	}
		

if __name__ == '__main__':

	webapp = WebPage()
	webapp.generator = WebService() #restricted
	webapp.auth = AuthController()
	webapp.static = Public()
	cherrypy.server.socket_host = 'localhost'
	cherrypy.server.socket_port = 8080
	cherrypy.quickstart(webapp , '/')

# '/auth': {
# 		'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
# 		'tools.response_headers.on': True,
# 		'tools.response_headers.headers': [('Content-Type', 'text/plain')],
# 		},