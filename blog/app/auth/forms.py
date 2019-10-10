from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired()])
    remember_me = BooleanField(label='记住密码')
    submit = SubmitField(label='登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('此用户名已被注册，请重新输入')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱已被注册，请重新输入')


# 请求重置密码表单页面
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('请输入你的邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('密码重置')


# 重置密码的表单
class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('修改密码')