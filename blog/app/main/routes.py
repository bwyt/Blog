from datetime import datetime

from flask import flash, redirect, url_for, request, current_app, render_template
from flask_login import login_required, current_user

from app import db
from app.main import main_blu
from app.main.form import PostForm, EditProfileForm
from app.models import Post, User


@main_blu.route('/', methods=['GET', 'POST'])
@main_blu.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('提交成功')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    # 获取下一页的url，next_num：下一页的页码
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    # 获取上一页的url，prev_num：上一页的页码
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None

    return render_template('index.html', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)


@main_blu.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    # 获取下一页的url，next_num：下一页的页码
    next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
    # 获取上一页的url，prev_num：上一页的页码
    prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


@main_blu.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

@main_blu.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@main_blu.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(original_username=current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('保存成功')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':  # 先将个人信息展示，再渲染
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='修改个人信息 ', form=form)


@main_blu.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:  # 用户不存在
        flash('用户不存在')
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('不能关注自己')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('关注成功')
    return redirect(url_for('main.user', username=username))


@main_blu.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:  # 用户不存在
        flash('用户不存在')
        return redirect(url_for('main.index'))
    if user == current_user:  # 关注自己
        flash('不能关注自己')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('关注成功')
    return redirect(url_for('main.user', username=username))


