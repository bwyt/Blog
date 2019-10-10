from threading import Thread

from flask import render_template, current_app
from flask_mail import Message
from app import mail


def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)


"""
sender：发送者
recipients：接收者（可多个），列表[]
"""


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


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

