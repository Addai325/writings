from datetime import datetime
from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from flask_login import current_user, login_user, logout_user, login_required
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog import bcrypt, db
from flaskblog.models import User, Post
from flaskblog.users.utils import save_picture, send_reset_email



users = Blueprint('users', __name__)



@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created.  You can now login', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Register')

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            session.permanent=True
            flash('You have been logged in', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Unsuccessful Login. Please check Email and Password', 'failure')
    return render_template('login.html', form=form, title='Login')

@users.before_request
def session_time_checkout():
    # Only continue if user is authenticated
    if current_user.is_authenticated:
        # Reset session modification time for every request
        session.modified = True
    elif request.endpoint not in ['users.login', 'users.register', 'users.reset_request']:
        # Redirect to login if session expired and user tries to access protected routes
        flash('Your session has expired, please log in again', 'warning')
        return redirect(url_for('users.login'))





@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))




@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file= save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your Account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)





@users.route("/user/<string:username>")
def user_posts(username):
    page=request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=2, page=page)
    return render_template('user_posts.html', posts=posts, user=user)





@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to you with instructions to reset your password', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Request', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_request_reset(token)
    if not user:
        flash('This is an invalid or expired token', 'failure')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash(f'Your password has now been changed.  You can now login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}