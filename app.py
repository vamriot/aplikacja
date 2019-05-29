from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)

class Formdata(db.Model):
    __tablename__ = 'formdata'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    plec = db.Column(db.String, nullable=False)
    age = db.Column(db.String)
    place = db.Column(db.String)
    income = db.Column(db.String)
    health = db.Column(db.Integer)
    q1 = db.Column(db.String)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)
    q8 = db.Column(db.Integer)
    q9 = db.Column(db.Integer)
    q10 = db.Column(db.Integer)
    q11 = db.Column(db.Integer)
    q12 = db.Column(db.Integer)
    q13 = db.Column(db.Integer)
    q14 = db.Column(db.Integer)
    q15 = db.Column(db.Integer)
    q16 = db.Column(db.String)
    q17 = db.Column(db.Integer)
    q18 = db.Column(db.Integer)
    q19 = db.Column(db.Integer)
    q20 = db.Column(db.String)

    def __init__(self, plec, age, place, income, health, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20):
        self.plec = plec
        self.age = age
        self.place = place
        self.income = income
        self.health = health
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.q6 = q6
        self.q7 = q7
        self.q8 = q8
        self.q9 = q9
        self.q10 = q10
        self.q11 = q11
        self.q12 = q12
        self.q13 = q13
        self.q14 = q14
        self.q15 = q15
        self.q16 = q16
        self.q17 = q17
        self.q18 = q18
        self.q19 = q19
        self.q20 = q20

db.create_all()


@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/form")
def show_form():
    return render_template('form.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(Formdata).all()
    return render_template('raw.html', formdata=fd)


@app.route("/result")
def show_result():
    fd_list = db.session.query(Formdata).all()
    
    # Some simple statistics for sample questions
    #satisfaction = []
    #q1 = []
    #q2 = []
    #for el in fd_list:
    #    satisfaction.append(int(el.satisfaction))
    #    q1.append(int(el.q1))
    #    q2.append(int(el.q2))

    #if len(satisfaction) > 0:
        #mean_satisfaction = statistics.mean(satisfaction)
    #else:
        #mean_satisfaction = 0

    #if len(q1) > 0:
        #mean_q1 = statistics.mean(q1)
    #else:
        #mean_q1 = 0

    #if len(q2) > 0:
        #mean_q2 = statistics.mean(q2)
    #else:
        #mean_q2 = 0

    # Prepare data for google charts
    #data = [['Satisfaction', mean_satisfaction], ['Python skill', mean_q1], ['Flask skill', mean_q2]]
    health = []
    plec = []

    for el in fd_list:
        health.append(int(el.health))
        plec.append(int(el.plec))

    if len(health) > 0:
        mean_health = statistics.mean(health)
    else:
        mean_health = 0
    data=[['Stan zdrowia', mean_health]]

    return render_template('result.html', data=data)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    plec = request.form['plec']
    age = request.form['age']
    place = request.form['place']
    income = request.form['income']
    health = request.form['health']
    q1 = request.form['q1']
    q2 = request.form['q2']
    q3 = request.form['q3']
    q4 = request.form['q4']
    q5 = request.form['q5']
    q6 = request.form['q6']
    q7 = request.form['q7']
    q8 = request.form['q8']
    q9 = request.form['q9']
    q10 = request.form['q10']
    q11 = request.form['q11']
    q12 = request.form['q12']
    q13 = request.form['q13']
    q14 = request.form['q14']
    q15 = request.form['q15']
    q16 = request.form['q16']
    q17 = request.form['q17']
    q18 = request.form['q18']
    q19 = request.form['q19']
    q20 = request.form['q20']

    # Save the data
    fd = Formdata(plec, age, place, income, health, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()