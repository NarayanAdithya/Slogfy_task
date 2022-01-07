from flask import Flask, json,request, render_template, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'{self.data} at {self.timestamp}'

@app.route('/')
@app.route('/home')
def home():
    data = Data.query.all()
    return render_template('home.html',data = data)



@app.route('/receive_data',methods =['POST'])
def receive_data():
    if request.method == 'POST':
        data = request.form['data']
        print(data)
        data_instance = Data()
        data_instance.data = data
        db.session.add(data_instance)
        db.session.commit()
        return json.jsonify({
            'Data Received':data
        })
        


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')

