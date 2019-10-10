from flask import render_template

from news import news_blu


@news_blu.route('/news')
def news():
    # return 'news.html'
    return render_template('news.html')