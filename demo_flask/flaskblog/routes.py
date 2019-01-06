
from flask import render_template, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post

posts = [

    {
        'author' : 'Eleanor Roosevelt',
        'title': 'Blog Post - 1',
        'content': 'Great minds discuss ideas; average minds discuss events; small minds discuss people.',
        'date_posted': 'April 20, 2018'
    },

    {
        'author' : 'Abraham Lincoln',
        'title': 'Blog Post - 2',
        'content': 'I’m a success today because I had a friend who believed in me and I didn’t have the heart to let him down',
        'date_posted': 'April 22, 2018'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your credentials', 'danger')
    return render_template('login.html', title='Login', form=form)