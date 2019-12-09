try:
    import os
    from flask import Flask, render_template, request
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy import and_
    from sqlalchemy import or_
    from click import File
    import random

    print("found")
except:
    print("not found d")

myApp = Flask(__name__)
project_dir = os.path.abspath(os.path.dirname(__file__))
print("=" * 100)

database_file = "sqlite:///{}".format(os.path.join(project_dir, "school.db"))
myApp.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(myApp)


class User(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=False, nullable=False)
    role = db.Column(db.String(40), unique=False, nullable=False)


# db.create_all()


@myApp.route('/')
def home():
    return render_template("login.html")

@myApp.route('/submit', methods=["POST"])
def Submit():
    user1 = User.query.all()
    user = User()
    user.name = request.form['name']
    user.password =random.randint(1000, 9999)
    user.email = request.form['email']
    user.phone = request.form['phone']
    user.role = request.form['option0']
    if user.email == "Admin@gmail.com":
        return render_template("signUP.html", msg2="Email Exist")

    else:
        for u in user1:
            if (u.name == user.name):
                return render_template("signUP.html",msg1="User Name Exist")
            elif (u.email == user.email):
                return render_template("signUP.html", msg2="Email Exist")
            elif u.phone == user.phone:
                return render_template("signUP.html", msg3="password Exist")
        db.session.add(user)
        db.session.commit()

        return render_template("display.html" ,user=user)


@myApp.route('/Sign_in', methods=["POST", "GET"])
def mylogin():
    Uname="Admin"
    Upassword="1234"
    if request.form['username'] == Uname and request.form['password'] == Upassword:
        return render_template("admit.html", name=Uname)
    else:
        user = User.query.filter_by(name=request.form['username']).first()
        msg1 = " "
        msg2 = " "
        msg = " "
        if user:
            if user.password == request.form['password']:
                if user.role == "Student":
                    msg = "Student Portal"
                    pic = "student (1).jpg"
                    color= "text-light"
                    return render_template("show.html", user=user, msg=msg, pic=pic, colr=color)
                else:
                    msg = "Teacher Portal"
                    pic="teacher.jpg"
                    color = "text-dark"
                    return render_template("show.html", user=user, msg=msg,pic=pic,colr=color)
            else:
                msg1 = "* password incorrect"
                return render_template("login.html", msg1=msg1)
        else:
            msg2 = "* Incorrect Username"
            return render_template("login.html", msg2=msg2)


@myApp.route('/Update', methods=["POST"])
def Update():
    User_id = request.form['user_id']
    get_user = User.query.filter_by(id=User_id).first()
    return render_template("update.html", user=get_user)


@myApp.route('/update1', methods=["POST"])
def update1():
    # print(request.form['username'])


    user = User()
    # if request.method == "POST":
    foud_id = request.form.get("user_id")
    name = request.form.get("New_name")
    password =request.form.get("password")
    email = request.form.get("New_email")
    phone = request.form.get("phone_number")
    change = User.query.filter_by(id=foud_id).first()
    user1 = User.query.filter(User.id != foud_id).all()

    for u in user1:
        if u.name == name:
            return render_template("update.html", user=change, error1="User Name Exist")

    change.name = name
    for u in user1:
         if u.email == email:
            return render_template("update.html", user=change, error2="Email Exist")

    change.email = email
    change.password = password
    change.phone = phone




    # change = User.query.filter_by(email=old_email).first()
    # db.session.add(change)
    # db.session.commit()
    db.session.commit()

    if change.role == "Student":
        return render_template("show.html", user=change, msg="Student Portal" )
    else:
        return render_template("show.html", user=change, msg="Teacher Portal")


@myApp.route('/admin',methods=["POST"])
def admin():
    return render_template("signUP.html")