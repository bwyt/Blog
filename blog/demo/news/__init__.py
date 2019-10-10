# 生成蓝图对象
from flask import Blueprint
"""
news_blu：蓝图对象
news：蓝图名
"""
news_blu = Blueprint('news', __name__, template_folder='templates', static_folder='static', static_url_path='/news')
# /news/tupian.jpg

from news.views import *