from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    about_me = TextAreaField('个人简介', validators=[Length(min=0, max=140)])
    submit = SubmitField('修改')

    # 验证用户名  保存当前用户的名字
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # super.__init__()
        self.original_username = original_username

    # 避开当前用户名去校验
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('该用户名已存在，请重新输入')


# 提交博客的表单
class PostForm(FlaskForm):
    post = TextAreaField('你的想法：', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('提交')
