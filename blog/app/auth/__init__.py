# 生成蓝图对象
from flask import Blueprint
# 导入接口对象
auth_blu = Blueprint('auth', __name__)


from app.auth import routes