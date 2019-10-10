

from flask import redirect, url_for, flash, request, render_template
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import auth_blu
from app.auth.email import send_password_reset_email
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User



@auth_blu.route('/login', methods=['GET', 'POST'])
def login():
    # 用户已经登录
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()  # 表单实例化对象
    if form.validate_on_submit():
        # 从数据库查询此用户，判断密码是否正确
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('你输入用户名或密码不正确，请重新输入')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='登录', form=form)


@auth_blu.route('/logout')
# 用户退出
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_blu.route('/register', methods=['GET', 'POST'])
# 注册功能
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # 存入数据库
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='注册', form=form)


@auth_blu.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:  # 用户存在
            send_password_reset_email(user)
        flash('邮件发送成功，请通过邮箱找回密码')
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

# 重置密码的视图函数
@auth_blu.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # 通过token进行解密user_id获取用户
    user = User.verify_reset_password_token(token)
    # 判断用户是否存在
    if not user:
        # 不存在，重定向到登录页面
        return redirect(url_for('auth.login'))
    # 存在就渲染重置密码的html
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # 如果表单校验成功就进行密码重置的操作
        user.set_password(form.password.data)
        db.session.commit()
        flash('重置密码成功')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)


