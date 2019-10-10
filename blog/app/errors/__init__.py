# 生成蓝图对象
from flask import Blueprint
# 导入接口对象
errors_blu = Blueprint('errors', __name__)

from app.errors import handlers