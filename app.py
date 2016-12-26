import os, time
from flask import Flask, render_template, json, request, Response,jsonify
from flask.ext.mysql import MySQL
from mongoengine import connect
from flask.ext.mongoengine import MongoEngine
from geojson import Point, Feature, FeatureCollection
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Happy24Fish'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.config['SECRET_KEY']='\x17b\x89\xae\x8bO\x99.Z\xbc\xb0\x05<M\x86\xb9\xb5\x1a\x89\xd2\x92\xa0\xaaR'

#----------------------------------------
# database
#----------------------------------------

DB_NAME = 'arctic-help'
DB_USERNAME = 'luciaberger'
DB_PASSWORD = 'Happy24Fish'
DB_HOST_ADDRESS = 'ds145128.mlab.com:45128/arctic-help'

app.config["MONGODB_DB"] = DB_NAME
connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)
db = MongoEngine(app)
print(db)


ACCESS_KEY = os.environ.get('pk.eyJ1IjoibHVjaWFiZXJnZXIiLCJhIjoiY2l4NHE1eHFkMDFpMDJ5b3d2OTVwMTVjdyJ9.WYhHRi5M6jOMpqR2kBXy-g')


@app.route("/")
def hello():
	return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showChart')
def showChart():
    return render_template('chart.html', ACCESS_KEY=ACCESS_KEY)

@app.route('/showTorontoChart')
def showTorontoChart():
    return render_template('torontochart.html', ACCESS_KEY=ACCESS_KEY)

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            print(_hashed_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password[0:6]))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

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
