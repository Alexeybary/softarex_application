from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from application import app
from application.forms import LoginForm, EditProfileForm
from application.models import User, db


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        user = {'username': current_user.name}
    else:
        user={'username': "anonym"}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('log out before loging as another user')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None:
            flash('This user has already signed up ')
            return redirect('/login')
        name = form.username.data
        psw=form.password.data
        new_user = User(name=name, psw=psw)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('signin.html', title='Sign In', form=form)
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(name=username).first_or_404()
    return render_template('user.html', user=user)
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None:
            flash('This user has already signed up ')
            return redirect(url_for('edit_profile'))
        current_user.name = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.name
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)