from flask import Flask, render_template, request,redirect,url_for,session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

##postgress
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:0000@localhost:3306/stud_books"
app.config['SECRET_KEY'] = "random string"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
# db.init_app(app)

db = SQLAlchemy(app)


class Rtrn(db.Model):
    __tablename__ = "b_return"
    id = db.Column(db.Integer, primary_key=True)
    St_Roll = db.Column(db.String(150), nullable=False)
    Bo_id = db.Column(db.String(150), nullable=False)
    Date = db.Column(db.DATE, default=datetime.now())
    # token_no = db.Column(db.String(15), nullable=False)
    charges = db.Column(db.Integer)

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    Book_id = db.Column(db.String(150),nullable = False)
    Title = db.Column(db.String(150), nullable=False)
    Edition = db.Column(db.String(150), nullable=False)
    Author = db.Column(db.String(50))
    Num_of_copies = db.Column(db.Integer,nullable=False)


class Borrow(db.Model):
    __tablename__ = "borrow"
    id = db.Column(db.Integer, primary_key=True)
    S_Roll = db.Column(db.Integer, nullable=False)
    B_id = db.Column(db.String(150), nullable=False)
    Date = db.Column(db.DATE, default=datetime.now())
    # token_no = db.Column(db.String(15), nullable=False)
    due = db.Column(db.String(12))

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    Roll_no = db.Column(db.Integer,nullable=False)
    Name = db.Column(db.String(50), nullable=False)
    Department = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(13), nullable=False)
    gender = db.Column(db.String(7))
    date = db.Column(db.DATE, default=datetime.now())

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return redirect(url_for('show'))
    else:
        return render_template('login.html', error='Invalid username or password')
    
@app.route('/register')
def register():
    return render_template('register.html')
    

@app.route('/create_account', methods=['GET','POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('register.html', error='Username already taken')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html',error = "You've Successfully Registered")
        
    return render_template('register.html')


@app.route('/logout')
def logout():
    return render_template('login.html')

@app.route('/cancel')
def cancel():
    return render_template('login.html')


@app.route("/show", methods=['GET'])
def show():
    students = Borrow.query.all()
    return render_template("intro.html", students=students)

@app.route("/insert", methods=['GET', 'POST'])
def insert():
    if request.method == "POST":
        
        roll_no = request.form.get("roll_no")
        name = request.form.get("name")
        Dpt = request.form.get("dpt")
        Cnt = request.form.get("cnt")
        gend = request.form.get("gender")

        # Creat new record
        stud = Student(Name = name, Department=Dpt, contact=Cnt, gender=gend,Roll_no = roll_no)
        db.session.add(stud)
        db.session.commit()

    students = Student.query.all()
    return render_template("insert_new_student.html", students=students)

@app.route("/book", methods=['GET', 'POST'])
def book():
    if request.method == "POST":

        book_id = request.form.get('bi')
        title = request.form.get("bt")
        edition = request.form.get("be")
        author = request.form.get("ba")
        num_of_copies = request.form.get("bc")

        # Creat new record
        stud = Book(Book_id = book_id ,Title = title, Edition=edition, Author=author,Num_of_copies = num_of_copies)
        db.session.add(stud)
        db.session.commit()

    cla = Book.query.all()
    return render_template("book.html", cla=cla)

@app.route("/borrow_book", methods=['GET', 'POST'])
def borrow():
    if request.method == "POST":

        name = request.form.get("sm")
        BT = request.form.get("bt")
        VN = request.form.get("vn")
        DA = request.form.get("date")

        # Creat new record
        stud = Borrow(S_Roll = name, B_id=BT, due=DA)
        db.session.add(stud)
        db.session.commit()

        students = Borrow.query.all()
        return render_template("intro.html", students=students)

    c = db.session.query(Student.Name).all()
    b = db.session.query(Book.Title).all()
    return render_template("borrow.html", c=c, b=b)


@app.route("/return_book", methods=['GET', 'POST'])
def rtrn():
    if request.method == "POST":

        name = request.form.get("sm")
        BT = request.form.get("bt")
        DT = request.form.get("dt")
        # VN = request.form.get("vn")
        DA = request.form.get("ch")

        # Creat new record
        stud = Rtrn(St_Roll = name, Bo_id=BT, Date=DT,charges=DA)
        db.session.add(stud)
        db.session.commit()

    students = Rtrn.query.all()
    c = db.session.query(Borrow.S_Roll).all()
    b = db.session.query(Borrow.B_id).all()
    return render_template("return.html", c=c, b=b, students=students)

@app.route("/deletebook/<string:id>",methods = ['GET','POST'])
def deletebook(id):
    db.engine.execute(f"delete from books where books.id={id}")
    # return render_template('book.html')
    return redirect(url_for("book"))

@app.route("/deletestudent/<string:id>",methods = ['GET','POST'])
def deletestudent(id):
    db.engine.execute(f"delete from students where students.id={id}")
    # return render_template('book.html')
    return redirect(url_for("insert"))




# @app.route("/search", methods=['GET','POST'])
# def search():
#     if request.method == 'POST':
#         Name = request.form.get('S_Name')
#         bio = Borrow.query.filter_by(S_Name = Name).first()
#         return render_template('intro.html',bio=bio)
#     students = Borrow.query.all()
#     return render_template("search.html",students = students)


@app.route("/api", methods=['GET','POST'])
def api():
    if request.method == 'POST':
        form = request.form
        search_value = form['tag']
        print(search_value)
        search = "%{0}%".format(search_value)
        results = Borrow.query.filter(Borrow.S_Roll.like(search)).all()
        return render_template('search.html',students = results)
    
    return render_template('results.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)