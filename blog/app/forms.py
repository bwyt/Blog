# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, TextAreaField
# from wtforms.validators import DataRequired, Email, EqualTo, Length
#
# from app.models import User
#
#
# class LoginForm(FlaskForm):
#     username = StringField(label='用户名', validators=[DataRequired()])
#     password = PasswordField(label='密码', validators=[DataRequired()])
#     remember_me = BooleanField(label='记住密码')
#     submit = SubmitField(label='登录')
#
#
# class RegistrationForm(FlaskForm):
#     username = StringField('用户名', validators=[DataRequired()])
#     email = StringField('邮箱', validators=[DataRequired(), Email()])
#     password = PasswordField('密码', validators=[DataRequired()])
#     password2 = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('注册')
#
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user is not None:
#             raise ValidationError('此用户名已被注册，请重新输入')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is not None:
#             raise ValidationError('邮箱已被注册，请重新输入')
#
#
# class EditProfileForm(FlaskForm):
#     username = StringField('用户名', validators=[DataRequired()])
#     about_me = TextAreaField('个人简介', validators=[Length(min=0, max=140)])
#     submit = SubmitField('修改')
#
#     # 验证用户名  保存当前用户的名字
#     def __init__(self, original_username, *args, **kwargs):
#         super(EditProfileForm, self).__init__(*args, **kwargs)
#         # super.__init__()
#         self.original_username = original_username
#
#     # 避开当前用户名去校验
#     def validate_username(self, username):
#         if username.data != self.original_username:
#             user = User.query.filter_by(username=self.username.data).first()
#             if user is not None:
#                 raise ValidationError('该用户名已存在，请重新输入')
#
#
# # 提交博客的表单
# class PostForm(FlaskForm):
#     post = TextAreaField('你的想法：', validators=[DataRequired(), Length(min=1, max=140)])
#     submit = SubmitField('提交')
#
#
# # 请求重置密码表单页面
# class ResetPasswordRequestForm(FlaskForm):
#     email = StringField('请输入你的邮箱', validators=[DataRequired(), Email()])
#     submit = SubmitField('密码重置')
#
#
# # 重置密码的表单
# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('密码', validators=[DataRequired()])
#     password2 = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('修改密码')