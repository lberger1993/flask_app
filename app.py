import os, time
from flask import Flask, render_template, json, request, Response,jsonify
from geojson import Point, Feature, FeatureCollection
from werkzeug import generate_password_hash, check_password_hash
from database import init_db
from flask.ext.pymongo import PyMongo


#----------------------------------------
# database
#----------------------------------------

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'arctic-help'
app.config['MONGO_URI'] = 'mongodb://luciaberger:Happy24Fish@ds145128.mlab.com:45128/arctic-help'
mongo = PyMongo(app)

ACCESS_KEY = os.environ.get('pk.eyJ1IjoibHVjaWFiZXJnZXIiLCJhIjoiY2l4NHE1eHFkMDFpMDJ5b3d2OTVwMTVjdyJ9.WYhHRi5M6jOMpqR2kBXy-g')

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
    return jsonify(result=feature_collection)

@app.route('/process')
def long_running_process():
      def generate():
        for row in range(1, 10):
            yield 'data: Processing \n\n'
            time.sleep(2)
      return Response(generate(), mimetype='text/event-stream')  

if __name__ == "__main__":
    app.run(threaded=True)
