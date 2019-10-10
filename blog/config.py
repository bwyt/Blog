import os

basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前.py文件的绝对路径


class Config:
    SECRET_KEY = 'vmskjvn'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 5  # 设置每页查询数量的常量

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = '18423098802@163.com'  # 发件人邮箱
    MAIL_PASSWORD = 'yybwyt0925'  # 发件人邮箱的授权码