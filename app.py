from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:user@localhost:5432/healthgenie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserData(db.Model):
    __tablename__ = 'Userdata'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    gmail = db.Column(db.String)
    Password =  db.Column(db.String)

class UserFeedback(db.Model):
    __tablename__='Userfeedback'
    fid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    mail = db.Column(db.String)
    msg =  db.Column(db.String)

@app.route('/')
def index():
    return render_template('index.html')   

@app.route('/contct&fb',methods=['POST','GET'])
def contct():
    if request.method == 'POST':
         user__name = request.form.get('name')
         email_ = request.form.get('email')
         messg = request.form.get('message')
         userfeedback=UserFeedback(name=user__name,mail=email_,msg=messg)  
         db.session.add(userfeedback)    
         db.session.commit()
         insert_fid =userfeedback.fid
         return render_template('contct&fb.html', message="Feedback submitted")
    else:
         return render_template('contct&fb.html')
  
@app.route('/login',methods=['POST','GET'])
def Loginp():
    if request.method == 'POST':
        lemail = request.form.get('email')
        lpsw = request.form.get('password')
        userdata = UserData.query.filter_by(gmail=lemail).first()
        if userdata:
            if userdata.Password == lpsw:
                return render_template('main.html',lpsw=lpsw,email=lemail,u=userdata.Password)
            else:
                return render_template('login.html', message="Incorrect password !")
        else:
            return render_template('login.html', message="User does not exist !")    
    else:
        return render_template('login.html')  

@app.route('/about',methods=['POST','GET'])
def about():
    return render_template('about.html')



@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('name')
        email = request.form.get('email')
        psw = request.form.get('password')
        userdata=UserData(user_name=username,Password=psw,gmail=email)  
        db.session.add(userdata)    
        db.session.commit()
        inserted_id =userdata.id
        return render_template('main.html')
    else:
        return render_template('signup.html')   

@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
    


