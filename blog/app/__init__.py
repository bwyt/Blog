from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config

# 生成一个实例对象
db = SQLAlchemy()  # 数据库对象
migrate = Migrate()  # 迁移引擎对象
login = LoginManager()  # 登录功能
login.login_view = 'auth.login'  # login --> 视图函数
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()

# 创建一个生成app的函数
def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # 给app注册蓝图对象
    from app.errors import errors_blu
    app.register_blueprint(errors_blu)

    from app.auth import auth_blu
    app.register_blueprint(auth_blu)

    from app.main import main_blu
    app.register_blueprint(main_blu)

    return app





# 从app包中导入模块routes
# from app import routes, models, errors
from app import models
