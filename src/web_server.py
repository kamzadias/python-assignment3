from datetime import datetime, timedelta
import datetime
from flask import Flask,redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
import jwt

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost:5432/PythonAss3'
app.config['SECRET_KEY']='Secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)

class users(db.Model):
    user_id=db.Column(db.Integer,primary_key=True)
    login=db.Column(db.VARCHAR(256),nullable=False)
    password=db.Column(db.VARCHAR(256),nullable=False)
    token=db.Column(db.TEXT,nullable=False,default='')


@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        token = request.form['tok']
        return redirect('/protected?token='+ token)
    return render_template('index.html')

@app.route('/login')
def login():
    auth = request.authorization
    
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW-Authenticate': 'Basic realm="login required!"'})
    user = users.query.filter_by(login=auth.username).first()
    
    if not user:
        return make_response('could not verify', 401, {'WWW-Authenticate': 'Basic realm="login required!"'})
    
    if auth and auth.password==user.password:
        token = jwt.encode(
            {'username': user.login, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
            app.config['SECRET_KEY'])
        user = users.query.filter_by(login=auth.username).first()
        user.token = token
        db.session.commit()
        return jsonify({'token':jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])})
    return make_response('could not verify!', 401, {'WWW-Authenticate': 'Basic realm="login required'})

@app.route('/protected')
def protected():
    token = request.args.get('token')
    if not token:
        return '<h1>Hello, token is missing </h1>', 403
    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except:
        return '<h1>Hello, Could not verify the token</h1>', 403

    return '<h1>Hello, token which is provided is correct</h1>'

if __name__=='__main__':
    app.run(debug=True)