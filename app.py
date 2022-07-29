from flask import Flask, render_template

# Create a Flask instance
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


    
# @app.route('/login', methods= ['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit(): #checks if entries are valid 
#     user = User(username= form.username.data, email=form.email.data, password=form.password.data)
#     db.session.add(user)
#     db.session.commit()
#     flash(f' Account created for {form.username.data}!, 'success')
#     return redirect(url_for('home')) #if so-send to home page
#     return render_template('login.html', title= 'Login', form=form)


    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")