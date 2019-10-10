from threading import Thread

from flask import render_template, current_app
from flask_mail import Message
from app import mail
from app.email import send_email


def send_password_reset_email(user):
    # 通过用户生成jwt
    token = user.get_reset_password_token()
    # 发送邮件
    send_email('[Microblog] Reset Your Password',
               # subject='重置密码',
               sender=current_app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

