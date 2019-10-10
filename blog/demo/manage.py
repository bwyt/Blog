
from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/index')
def index():
    return 'index'


@app.route('/user')
def user():
    """
    1. url_for('蓝图名.函数名')
    2. 路由
    """
    return redirect(url_for('news.news'))
    # return redirect('/news')


# 给app注册蓝图对象
from news import news_blu
app.register_blueprint(news_blu)


if __name__ == '__main__':
    app.run(debug=True)
