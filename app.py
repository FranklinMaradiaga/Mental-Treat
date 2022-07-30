from flask import Flask, render_template, request
import secrets
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask instance
app = Flask(__name__)
# Secret Key
app.config['SECRET_KEY'] = secrets.token_hex(16)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#Initialize the Database
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.email

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    # return request.method 
    if request.method == "POST":
        email = request.form.get("myemail")
        password = request.form.get("password")

        if request.form.get("button") == "Clicked":
            user = Users.query.filter_by(email=email).first()

            if user is None:
                user = Users(email=email)
                db.session.add(user)
                db.session.commit()
            
                flash("You know it", user)
            return meditation()
        our_users = Users.query.order_by(Users.date_added)
    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/meditation')
def meditation():
    return render_template('meditation.html')

    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")