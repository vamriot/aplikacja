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
    plec = db.Column(db.String)
    age = db.Column(db.String)
    place = db.Column(db.String)
    income = db.Column(db.String)
    health = db.Column(db.String)
    q1 = db.Column(db.String)
    q2 = db.Column(db.String)
    q3 = db.Column(db.String)
    q4 = db.Column(db.String)
    q5 = db.Column(db.String)
    q12 = db.Column(db.String)
    q13 = db.Column(db.String)
    q14 = db.Column(db.String)
    q15 = db.Column(db.String)
    q16 = db.Column(db.String)

    def __init__(self, plec, age, place, income, health, q1, q2, q3, q4, q5, q12, q13, q14, q15, q16):
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
        self.q12 = q12
        self.q13 = q13
        self.q14 = q14
        self.q15 = q15
        self.q16 = q16

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

    # Prepare data for google charts

    plecKobieta=0
    plecMezczyzna=0
    for el in fd_list:
        if(el.plec=="Kobieta"):
            plecKobieta=plecKobieta+1
        if(el.plec=="Mężczyzna"):
            plecMezczyzna=plecMezczyzna+1

    data_plec=[['Kobiety', plecKobieta], ['Mężczyźni', plecMezczyzna]]
    
    wiek1=0
    wiek2=0
    wiek3=0
    wiek4=0
    wiek5=0
    wiek6=0
    for el in fd_list:
        if(el.age=="18-24"):
            wiek1=wiek1+1
        if(el.age=="25-34"):
            wiek2=wiek2+1
        if(el.age=="35-44"):
            wiek3=wiek3+1
        if(el.age=="45-54"):
            wiek4=wiek4+1
        if(el.age=="55-64"):
            wiek5=wiek5+1
        if(el.age=="65+"):
            wiek6=wiek6+1

    data_age=[['18-24', wiek1],['25-34', wiek2],['35-44', wiek3],['45-54', wiek4],['55-64', wiek5],['65+', wiek6]]
    
    place1=0
    place2=0
    place3=0
    place4=0
    place5=0
    place6=0
    for el in fd_list:
        if(el.place=="Wieś"):
            place1=place1+1
        if(el.place=="Miasto do 19 999"):
            place2=place2+1
        if(el.place=="Miasto 20 000 - 49 999"):
            place3=place3+1
        if(el.place=="Miasto 50 000 - 99 999"):
            place4=place4+1
        if(el.place=="Miasto 100 000 - 499 999"):
            place5=place5+1
        if(el.place=="Miasto 500 000 i więcej mieszkańców"):
            place6=place6+1

    data_place=[['Wieś', place1],['Miasto do 19 999', place2],['Miasto 20 000 - 49 999', place3],['Miasto 50 000 - 99 999', place4],['Miasto 100 000 - 499 999', place5],['Miasto 500 000 i więcej mieszkańców', place6]]
    
    income1=0
    income2=0
    income3=0
    income4=0
    income5=0
    income6=0
    income7=0
    for el in fd_list:
        if(el.income=="Odmawiam odpowiedzi"):
            income1=income1+1
        if(el.income=="do 999 zł"):
            income2=income2+1
        if(el.income=="1000 - 1499 zł"):
            income3=income3+1
        if(el.income=="1500 - 1999 zł"):
            income4=income4+1
        if(el.income=="2000 - 2499 zł"):
            income5=income5+1
        if(el.income=="2500 - 2999 zł"):
            income6=income6+1
        if(el.income=="3000 + zł"):
            income7=income7+1

    data_income=[['Odmawiam odpowiedzi', income1],['do 999 zł', income2],['1000 - 1499 zł', income3],['1500 - 1999 zł', income4],['2000 - 2499 zł', income5],['2500 - 2999 zł', income6], ['3000 + zł', income7] ]
    
    health1=0
    health2=0
    health3=0
    for el in fd_list:
        if(el.health=="Dobrze"):
            health1=health1+1
        if(el.health=="Tak sobie"):
            health2=health2+1
        if(el.health=="Źle"):
            health3=health3+1

    data_health=[['Dobrze', health1], ['Tak sobie', health2], ['Źle', health3]]

    q1_1=0
    q1_2=0
    q1_3=0
    q1_4=0
    q1_5=0
    q1_6=0
    for el in fd_list:
        if(el.q1=="Ograniczam się do zastosowania wypróbowanych domowych sposobów"):
            q1_1=q1_1+1
        if(el.q1=="Od razu idę do lekarza i stosuję przepisane leki"):
            q1_2=q1_2+1
        if(el.q1=="Nie idę do lekarza, stosuję leki lub środki farmaceutyczne dostępne bez recepty"):
            q1_3=q1_3+1
        if(el.q1=="Korzystam z usług medycyny niekonwencjonalnej"):
            q1_4=q1_4+1
        if(el.q1=="Nic nie robię - staram się przeczekać dolegliwości"):
            q1_5=q1_5+1
        if(el.q1=="Postępuję w inny sposób"):
            q1_6=q1_6+1

    data_q1=[['Ograniczam się do zastosowania wypróbowanych domowych sposobów', q1_1],['Od razu idę do lekarza i stosuję przepisane leki', q1_2], ['Nie idę do lekarza, stosuję leki lub środki farmaceutyczne dostępne bez recepty', q1_3],['Korzystam z usług medycyny niekonwencjonalnej', q1_4],['Nic nie robię - staram się przeczekać dolegliwości', q1_5],['Postępuję w inny sposób', q1_6],]
   
    q2_1=0
    q2_2=0
    q2_3=0
    q2_4=0
    for el in fd_list:
        if(el.q2=="TAK, wielokrotnie"):
            q2_1=q2_1+1
        if(el.q2=="TAK, kilka razy"):
            q2_2=q2_2+1
        if(el.q2=="TAK, 1-2 razy"):
            q2_3=q2_3+1
        if(el.q2=="NIE, ani razu"):
            q2_4=q2_4+1

    data_q2=[['TAK, wielokrotnie', q2_1],['TAK, kilka razy', q2_2],['TAK, 1-2 razy', q2_3],['NIE, ani razu', q2_4]]
    
    q3_1=0
    q3_2=0
    q3_3=0
    q3_4=0
    for el in fd_list:
        if(el.q3=="TAK, wielokrotnie"):
            q3_1=q3_1+1
        if(el.q3=="TAK, kilka razy"):
            q3_2=q3_2+1
        if(el.q3=="TAK, 1-2 razy"):
            q3_3=q3_3+1
        if(el.q3=="NIE, ani razu"):
            q3_4=q3_4+1

    data_q3=[['TAK, wielokrotnie', q3_1],['TAK, kilka razy', q3_2],['TAK, 1-2 razy', q3_3],['NIE, ani razu', q3_4]]
    
    q4_1=0
    q4_2=0
    q4_3=0
    q4_4=0
    for el in fd_list:
        if(el.q4=="TAK, wielokrotnie"):
            q4_1=q4_1+1
        if(el.q4=="TAK, kilka razy"):
            q4_2=q4_2+1
        if(el.q4=="TAK, 1-2 razy"):
            q4_3=q4_3+1
        if(el.q4=="NIE, ani razu"):
            q4_4=q4_4+1

    data_q4=[['TAK, wielokrotnie', q4_1],['TAK, kilka razy', q4_2],['TAK, 1-2 razy', q4_3],['NIE, ani razu', q4_4]]
    
    q5_1=0
    q5_2=0
    q5_3=0
    q5_4=0
    for el in fd_list:
        if(el.q5=="TAK, wielokrotnie"):
            q5_1=q5_1+1
        if(el.q5=="TAK, kilka razy"):
            q5_2=q5_2+1
        if(el.q5=="TAK, 1-2 razy"):
            q5_3=q5_3+1
        if(el.q5=="NIE, ani razu"):
            q5_4=q5_4+1

    data_q5=[['TAK, wielokrotnie', q5_1],['TAK, kilka razy', q5_2],['TAK, 1-2 razy', q5_3],['NIE, ani razu', q5_4]]

    q12_1=0
    q12_2=0
    q12_3=0
    q12_4=0
    q12_5=0
    q12_6=0
    for el in fd_list:
        if(el.q12=="0 zł"):
            q12_1=q12_1+1
        if(el.q12=="do 19 zł"):
            q12_2=q12_2+1
        if(el.q12=="20 - 49 zł"):
            q12_3=q12_3+1
        if(el.q12=="50 - 99 zł"):
            q12_4=q12_4+1
        if(el.q12=="powyżej 100 zł"):
            q12_5=q12_5+1
        if(el.q12=="powyżej 200 zł"):
            q12_6=q12_6+1

    data_q12=[['0 zł', q12_1],['do 19 zł', q12_2],['20 - 49 zł', q12_3],['50 - 99 zł', q12_4], ['powyżej 100 zł', q12_5], ['powyżej 200 zł', q12_6] ]
    
    q13_1=0
    q13_2=0
    q13_3=0
    q13_4=0
    for el in fd_list:
        if(el.q13=="TAK, zawsze"):
            q13_1=q13_1+1
        if(el.q13=="TAK, często"):
            q13_2=q13_2+1
        if(el.q13=="TAK, rzadko"):
            q13_3=q13_3+1
        if(el.q13=="NIE, nigdy"):
            q13_4=q13_4+1

    data_q13=[['TAK, zawsze', q13_1],['TAK, często', q13_2],['TAK, rzadko', q13_3],['NIE, nigdy', q13_4]]

    q14_1=0
    q14_2=0
    q14_3=0
    q14_4=0
    for el in fd_list:
        if(el.q14=="TAK, zawsze"):
            q14_1=q14_1+1
        if(el.q14=="TAK, często"):
            q14_2=q14_2+1
        if(el.q14=="TAK, rzadko"):
            q14_3=q14_3+1
        if(el.q14=="NIE, nigdy"):
            q14_4=q14_4+1

    data_q14=[['TAK, zawsze', q14_1],['TAK, często', q14_2],['TAK, rzadko', q14_3],['NIE, nigdy', q14_4]]

    q15_1=0
    q15_2=0
    q15_3=0
    q15_4=0
    for el in fd_list:
        if(el.q15=="TAK, zawsze"):
            q15_1=q15_1+1
        if(el.q15=="TAK, często"):
            q15_2=q15_2+1
        if(el.q15=="TAK, rzadko"):
            q15_3=q15_3+1
        if(el.q15=="NIE, nigdy"):
            q15_4=q15_4+1

    data_q15=[['TAK, zawsze', q15_1],['TAK, często', q15_2],['TAK, rzadko', q15_3],['NIE, nigdy', q15_4]]

    q16_1=0
    q16_2=0
    q16_3=0
    q16_4=0
    q16_5=0
    for el in fd_list:
        if(el.q16=="Zdecydowanie tak"):
            q16_1=q16_1+1
        if(el.q16=="Raczej tak"):
            q16_2=q16_2+1
        if(el.q16=="Trudno powiedzieć"):
            q16_3=q16_3+1
        if(el.q16=="Raczej nie"):
            q16_4=q16_4+1
        if(el.q16=="Zdecydowanie nie"):
            q16_5=q16_5+1

    data_q16=[['Zdecydowanie tak', q16_1],['Raczej tak', q16_2],['Trudno powiedzieć', q16_3],['Raczej nie', q16_4], ['Zdecydowanie nie', q16_5]]


    return render_template('result.html', data_plec=data_plec, data_age=data_age, data_place=data_place, data_income=data_income, data_health=data_health, data_q1=data_q1, data_q2=data_q2, data_q3=data_q3, data_q4=data_q4, data_q5=data_q5, data_q12=data_q12, data_q13=data_q13, data_q14=data_q14, data_q15=data_q15, data_q16=data_q16)  

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
    q12 = request.form['q12']
    q13 = request.form['q13']
    q14 = request.form['q14']
    q15 = request.form['q15']
    q16 = request.form['q16']
   

    # Save the data
    fd = Formdata(plec, age, place, income, health, q1, q2, q3, q4, q5, q12, q13, q14, q15, q16)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()