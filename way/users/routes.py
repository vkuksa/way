from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from way import db, bcrypt
from way.models import User, Article, Resource, TestResult
from way.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             RequestResetForm, ResetPasswordForm)
from way.users.utils import save_picture, send_reset_email
import way.test.utils

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.front'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You were automatically logged in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.front'))


@users.route("/account")
@login_required
def account():
    article_page = request.args.get('article_page', 1, type=int)
    resource_page = request.args.get('resource_page', 1, type=int)

    articles = Article.query.filter_by(author=current_user) \
        .order_by(Article.date_added.desc()) \
        .paginate(page=article_page, per_page=5)
    resources = Resource.query.filter_by(author=current_user) \
        .order_by(Resource.date_added.desc()) \
        .paginate(page=resource_page, per_page=5)

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    test_results = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.id.desc()).all()
    if len(test_results) >= 1:
        recent_result = test_results[0]
        print(recent_result.id)
        recent_data = recent_result.to_dict()

        if len(test_results) >= 2:
            previous_result = test_results[1]
            print(previous_result.id)
            previous_data = previous_result.get_scores()

        results = way.test.utils.get_results(recent_data)

    return render_template('user_info.html', title='Account', articles=articles, resources=resources,
                           image_file=image_file, user=current_user, data=results, previous_data=previous_data, legend='Portrait')


@users.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.settings'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('settings.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_info(username):
    test_result = TestResult.query.join(User, TestResult.user_id == User.id)\
                                    .filter(User.username == username).order_by(TestResult.id.desc()).first()
    test_data = test_result.to_dict()
    results = way.test.utils.get_results(test_data)

    article_page = request.args.get('article_page', 1, type=int)
    resource_page = request.args.get('resource_page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    articles = Article.query.filter_by(author=user) \
        .order_by(Article.date_added.desc()) \
        .paginate(page=article_page, per_page=5)
    resources = Resource.query.filter_by(author=user) \
        .order_by(Resource.date_added.desc()) \
        .paginate(page=resource_page, per_page=5)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user_info.html', articles=articles, resources=resources, user=user, image_file=image_file, data=results)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
