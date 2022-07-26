from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import update

from application import app
from application.forms import LoginForm, EditProfileForm, DimensionForm, UploadForm, DeleteForm, Download_pdf, Download_json
from application.models import User, db, Dimension
from application.predictions import loaded_model, check_file, make_prediction
from application.create_files import create_pdf,create_json


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        user = {'username': current_user.name}
    else:
        user = {'username': "anonym"}
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
        psw = form.password.data
        new_user = User(name=name, psw=psw)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('signin.html', title='Sign In', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    download_pdf=Download_pdf()
    download_json=Download_json()
    user = User.query.filter_by(name=username).first_or_404()
    if download_pdf.is_submitted():
        create_pdf(user.name)
    if download_json.is_submitted():
        create_json(user.name)
    return render_template('user.html', user=user,download_pdf=download_pdf,download_json=download_json)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    delete_form = DeleteForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None:
            flash('This user has already signed up ')
            return redirect(url_for('edit_profile'))
        a = Dimension.query.filter_by(name=current_user.name)
        for user_ in a:
            user_.name = form.username.data
        current_user.name = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.name

    if delete_form.is_submitted():
        current_user.count_of_dimension = 0
        Dimension.query.filter_by(name=current_user.name).delete()
        db.session.commit()
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form, delete_form=delete_form)


@app.route('/dimension', methods=['GET', 'POST'])
@login_required
def dimension():
    form = UploadForm()
    if form.is_submitted():
        if (check_file(form.file.data)):
            try:

                predict = make_prediction(form.file.data)
                for i in range(len(predict)):
                    dimens = predict[i]
                    dimension_name = form.dimension_name.data + str(i)
                    new_dimens = Dimension(name=current_user.name, dimension=dimens, dimension_name=dimension_name)
                    current_user.count_of_dimension += 1
                    db.session.add(new_dimens)
                    db.session.commit()
                flash('file upload succesfully')
            except:
                flash('Invalid Data')
    else:
        flash('please load .csv file')
    return render_template('dimension.html', title='To Calculate', form=form)
