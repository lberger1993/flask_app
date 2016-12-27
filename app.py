import os, time
from flask import Flask, render_template, json, request, Response, jsonify, url_for, session, redirect
from geojson import Point, Feature, FeatureCollection
from werkzeug import generate_password_hash, check_password_hash
from database import init_db
from flask.ext.pymongo import PyMongo
import bcrypt

#----------------------------------------
# database
#----------------------------------------

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'arctic-help'
app.config['MONGO_URI'] = 'mongodb://luciaberger:Happy24Fish@ds145128.mlab.com:45128/arctic-help'
mongo = PyMongo(app)


ACCESS_KEY = os.environ.get('pk.eyJ1IjoibHVjaWFiZXJnZXIiLCJhIjoiY2l4NHE1eHFkMDFpMDJ5b3d2OTVwMTVjdyJ9.WYhHRi5M6jOMpqR2kBXy-g')
IS_VERIFIED = False 

@app.route("/")
def hello():
	return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/add')
def add():
    user = mongo.db.users
    user.insert({'name' : 'Alex'})
    return 'Added users'

@app.route('/showChart')
def showChart():
    locations = mongo.db.locations.find
    print(locations)
    return render_template('chart.html', ACCESS_KEY=ACCESS_KEY)

@app.route('/showTorontoChart')
def showTorontoChart():
    return render_template('torontochart.html', ACCESS_KEY=ACCESS_KEY)

@app.route('/showVanChart')
def showVanChart():
    return render_template('vancouverchart.html', ACCESS_KEY=ACCESS_KEY)

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('showChart'))
    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        print(existing_user)
        if existing_user is None:
            print("This is where I am")
            #hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            print(request.form['username'])
            users.insert({'name' : request.form['username'],'email' : request.form['email'], 'password' : request.form['email']})
            session['username'] = request.form['username']
            return redirect(url_for('showChart', IS_VERIFIED = True ))
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        # validate the received values
        if _name and _email and _password:
            user = mongo.db.users
            user.insert({'name' : _name, 'email': _email, 'password': _password})
            #return render_template('torontochart.html', ACCESS_KEY=ACCESS_KEY)
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        print("EEORRRR")

@app.route('/getChartData',methods=['GET'])
def getChartData():
    print("I get here")

@app.route('/')
def index():
    return render_template('index.html', ACCESS_KEY=ACCESS_KEY)

@app.route('/result')
def process():
    point = Point((-73.56725599999999, 45.5016889))
    feature = Feature(geometry=point)
    feature_collection = FeatureCollection([feature])
    print(jsonify(feature_collection))
    return jsonify(result=feature_collection)

@app.route('/process')
def long_running_process():
      def generate():
        for row in range(1, 10):
            print("this")
      return Response(generate(), mimetype='text/event-stream')  

if __name__ == "__main__":
    app.secret_key = 'mysecret'
    app.run(debug=True)
