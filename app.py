from flask import Flask, render_template, request, flash, redirect, url_for
import secrets
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

# Create a Flask instance
app = Flask(__name__)
# Secret Key
app.config['SECRET_KEY'] = secrets.token_hex(16)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signup.db'

#Initialize the Database
db = SQLAlchemy(app)

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return SignUp.query.get(int(user_id))


# Delete All Records From Database
def delete_db():
    db.session.query(Users).delete()
    db.session.commit()


# Get data from database
def get_data():
    return Users.query.all()


# Create Model (Table in database)
class SignUp(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create A String
    def __repr__(self):
        return '<Username %r>' % self.username


@app.route('/login', methods=['GET', 'POST'])
def login():

    # return request.method 
    if request.method == "POST":
        email = request.form.get("myemail")
        password = request.form.get("password")

        if request.form.get("button") == "Clicked":
            user = SignUp.query.filter_by(email=email).first()

            if user:
                # Check the hash (Not hashed yet)
                login_user(user)
                flash("Login Successfull!!")
                return redirect(url_for('meditation'))
            else:
                flash("That User Doesn't Exist! - Try Again...")

            # return meditation()

    return render_template('signin.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out! Thanks For Stopping By...")
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    # return request.method 
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        # When user clicks the submit button
        if request.form.get("button") == "Clicked":
            username_exists = SignUp.query.filter_by(username=username).first()
            email_exists = SignUp.query.filter_by(email=email).first()
            print(username_exists)
            print(email_exists)

            # Checks if the username and emails are unique (not in the database)
            if username_exists is None and email_exists is None:
                user = SignUp(username=username, email=email, password=password)
                db.session.add(user)
                db.session.commit()

                our_users = SignUp.query.order_by(SignUp.date_added)

                for user in our_users:
                    print(user.email, user.password)

                print("In If:", SignUp.query.all())

                return login()

            else:
                print("Username or Email already exists")
                our_users = SignUp.query.order_by(SignUp.date_added)

                for user in our_users:
                    print("Are we here:", user.email, " ", user.password)

    return render_template('signup.html')


@app.route('/meditation')
@login_required
def meditation():
    return render_template('meditation.html')


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    # print(get_data())
