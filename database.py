import flask
from mongoengine import connect
from flask.ext.mongoengine import MongoEngine

DB_NAME = 'arctic-help'
DB_USERNAME = 'luciaberger'
DB_PASSWORD = 'Happy24Fish'
DB_HOST_ADDRESS = 'ds145128.mlab.com:45128/arctic-help'

def init_db(app):
	app.config["MONGODB_DB"] = DB_NAME
	connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)
	db = MongoEngine(app)