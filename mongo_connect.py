from flask import Flask 
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'arctic-help'
app.config['MONGO_URI'] = 'mongodb://luciaberger:Happy24Fish@ds145128.mlab.com:45128/arctic-help'

mongo = PyMongo(app)

@app.route('/add')
def app():
	user = mongo.db.users
	user.insert({'name' : 'Alex'})
	return 'Added users'

if __name__ == "__main__":
    app.run()