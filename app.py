from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from apis import get_daily_quote, get_author

# Create a Flask instance
app = Flask(__name__)
# Secret Key
app.config['SECRET_KEY'] = '3dcd42e793260e135ac9bc75ac72d80e'

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///create_account.db'

#Initialize the Database
db = SQLAlchemy(app)

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Create Model (Table in database)
class Create_Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')


    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    # Create A String
    def __repr__(self):
        return '<Username %r>' % self.email


def get_data():
        our_users = Create_Account.query.order_by(Create_Account.date_added)
        for user in our_users:
            print("id: ", user.id)
            print("password: ", user.password_hash)
            print("email: ", user.email)
            print("username: ", user.username)
    
        print("Are we here:", Create_Account.query.all())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("myemail")
        password = request.form.get("password")

        if request.form.get("button") == "Clicked":
            user = Create_Account.query.filter_by(email=email).first()

            if user:
                # Check if the hashed password matches the user's input
                if check_password_hash(user.password_hash, password):
                    print(user, "Password!!!: ", check_password_hash(user.password_hash, password))
                    login_user(user)
                    flash("Login Successfull!!")
                    return redirect(url_for('home1'))
                else:
                    flash("Wrong password!")
            else:
                flash("That User Doesn't Exist! - Try Again...")

    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    get_data()
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        # When user clicks the submit button
        if request.form.get("button") == "Clicked":
            username_exists = Create_Account.query.filter_by(username=username).first()
            email_exists = Create_Account.query.filter_by(email=email).first()

            # Checks if the username and emails are unique (not in the database)
            if username_exists is None and email_exists is None:
                
                # Hashed password
                hashed_pw = generate_password_hash(password, "sha256")

                user = Create_Account(username=username, email=email, password_hash=hashed_pw)
                db.session.add(user)
                db.session.commit()

                our_users = Create_Account.query.order_by(Create_Account.date_added)

                for user in our_users:
                    print(user.email, user.password_hash)

                print("In If:", Create_Account.query.all())

                return redirect(url_for('login'))

            else:
                flash("Username or Email already exists")
                our_users = Create_Account.query.order_by(Create_Account.date_added)

                for user in our_users:
                    print("In the else:", user.email, " ", user.password_hash)

    return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out! Thanks For Stopping By...")
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/')
@login_required
def home1():
    daily_quote = get_daily_quote()
    author = get_author()
    print(daily_quote, author)
    return render_template('home.html', daily_quote=daily_quote, author=author)

@app.route('/meditation')
@login_required
def meditation():
    return render_template('meditation.html')

@app.route('/taskmanager', methods=['GET', 'POST'])
@login_required
def task_manager():
    return redirect('https://dnb7l6.csb.app/')

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@login_manager.user_loader
def load_user(user_id):
    return Create_Account.query.get(int(user_id))


# Delete All Records From Database
def delete_db():
    db.session.query(Create_Account).delete()
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
