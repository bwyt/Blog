# # 从app包中导入 app这个实例
# from datetime import datetime
#
# from flask import render_template, flash, redirect, url_for, request
# from flask_login import current_user, login_user, logout_user, login_required
# from werkzeug.urls import url_parse
#
# from app import app, db
# from app.email import send_password_reset_email
# from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, \
#     ResetPasswordForm
# from app.models import User, Post
#
#
# @app.route('/', methods=['GET', 'POST'])
# @app.route('/index', methods=['GET', 'POST'])
# @login_required
# def index():
#     form = PostForm()
#     # post 请求做验证，生成帖子记录存入数据库，重定向到首页
#     if form.validate_on_submit():
#         # 将博文保存在数据库中
#         post = Post(body=form.post.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash('提交成功')
#         return redirect(url_for('index'))
#
#     # posts = [
#     #     {
#     #         'author': {'username': 'zs'},
#     #         'body': '为你我用了半年的积蓄，飘洋过海的来看你'
#     #     },
#     #     {
#     #         'author': {'username': 'ls'},
#     #         'body': '为了这次相聚，我连见面时的呼吸都曾反复练习'
#     #     },
#     #     {
#     #         'author': {'username': 'ww'},
#     #         'body': '言语从来没能将我的情谊表达千万分之一，为了这个遗憾，我在夜里想了又想不肯睡去'
#     #     }
#     # ]
#     # get 请求返回index和表单
#     # 从数据库中查出所有自己写的博客以及关注人的博客
#     """
#     分页：通过查询字符串获取页码
#     paginate()替换all()
#     在render_template使用.items获取数据列表
#     """
#     # posts = current_user.followed_posts().all()
#     page = request.args.get('page', 1, type=int)
#     posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
#     # 获取下一页的url，next_num：下一页的页码
#     next_url = url_for('index', page=posts.next_num) if posts.has_next else None
#     # 获取上一页的url，prev_num：上一页的页码
#     prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
#
#     return render_template('index.html', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)
#
#
# """
# 显示所有帖子的视图函数，返回index.html
# 首页需要表单而此页面不需要，故修改index.html里的逻辑
# 有表单展示表单，无表单则不展示表单
# 修改_post.html，为每个用户添加a标签跳转到用户界面
# """
# @app.route('/explore')
# @login_required
# def explore():
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
#     # 获取下一页的url，next_num：下一页的页码
#     next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
#     # 获取上一页的url，prev_num：上一页的页码
#     prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
#     return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)
#
#
#
# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     # 用户已经登录
# #     if current_user.is_authenticated:
# #         return redirect(url_for('index'))
# #     form = LoginForm()  # 表单实例化对象
# #     if form.validate_on_submit():
# #         # 从数据库查询此用户，判断密码是否正确
# #         user = User.query.filter_by(username=form.username.data).first()
# #         if user is None or not user.check_password(form.password.data):
# #             flash('你输入用户名或密码不正确，请重新输入')
# #             return redirect(url_for('login'))
# #         login_user(user, remember=form.remember_me.data)
# #         next_page = request.args.get('next')
# #         if not next_page or url_parse(next_page).netloc != '':
# #             next_page = url_for('index')
# #         return redirect(next_page)
# #     return render_template('login.html', title='登录', form=form)
#
#
# # @app.route('/logout')
# # # 用户退出
# # def logout():
# #     logout_user()
# #     return redirect(url_for('login'))
# #
# #
# # @app.route('/register', methods=['GET', 'POST'])
# # # 注册功能
# # def register():
# #     if current_user.is_authenticated:
# #         return redirect(url_for('index'))
# #     form = RegistrationForm()
# #     if form.validate_on_submit():
# #         # 存入数据库
# #         user = User(username=form.username.data, email=form.email.data)
# #         user.set_password(form.password.data)
# #         db.session.add(user)
# #         db.session.commit()
# #         flash('注册成功，请登录!')
# #         return redirect(url_for('login'))
# #     return render_template('register.html', title='注册', form=form)
# #
#
# # 个人信息页面
# @app.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     # posts = [
#     #     {'author': user, 'body': 'Test post #1'},
#     #     {'author': user, 'body': 'Test post #2'}
#     # ]
#     page = request.args.get('page', 1, type=int)
#     posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
#     prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
#     return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)
#
# # 处理记录用户最后访问时间的钩子函数
# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()
#
#
# @app.route('/edit_profile',methods=['GET','POST'])
# @login_required
# def edit_profile():
#     form = EditProfileForm(original_username=current_user.username)
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.about_me = form.about_me.data
#         db.session.commit()
#         flash('保存成功')
#         return redirect(url_for('user', username=current_user.username))
#     elif request.method == 'GET':  # 先将个人信息展示，再渲染
#         form.username.data = current_user.username
#         form.about_me.data = current_user.about_me
#     return render_template('edit_profile.html', title='修改个人信息 ', form=form)
#
#
# # 关注
# @app.route('/follow/<username>')
# @login_required
# def follow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:  # 用户不存在
#         flash('用户不存在')
#         return redirect(url_for('index'))
#     if user == current_user:
#         flash('不能关注自己')
#         return redirect(url_for('user', username=username))
#     current_user.follow(user)
#     db.session.commit()
#     flash('关注成功')
#     return redirect(url_for('user', username=username))
#
#
# # 取消关注
# @app.route('/unfollow/<username>')
# @login_required
# def unfollow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:  # 用户不存在
#         flash('用户不存在')
#         return redirect(url_for('index'))
#     if user == current_user:  # 关注自己
#         flash('不能关注自己')
#         return redirect(url_for('user', username=username))
#     current_user.unfollow(user)
#     db.session.commit()
#     flash('关注成功')
#     return redirect(url_for('user', username=username))
#
#
# # @app.route('/reset_password_request', methods=['GET','POST'])
# # def reset_password_request():
# #     if current_user.is_authenticated:
# #         return redirect(url_for('index'))
# #     form = ResetPasswordRequestForm()
# #     if form.validate_on_submit():
# #         user = User.query.filter_by(email=form.email.data).first()
# #         if user:  # 用户存在
# #             send_password_reset_email(user)
# #         flash('邮件发送成功，请通过邮箱找回密码')
# #         return redirect(url_for('login'))
# #     return render_template('reset_password_request.html', title='Reset Password', form=form)
# #
# # # 重置密码的视图函数
# # @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# # def reset_password(token):
# #     if current_user.is_authenticated:
# #         return redirect(url_for('index'))
# #     # 通过token进行解密user_id获取用户
# #     user = User.verify_reset_password_token(token)
# #     # 判断用户是否存在
# #     if not user:
# #         # 不存在，重定向到登录页面
# #         return redirect(url_for('login'))
# #     # 存在就渲染重置密码的html
# #     form = ResetPasswordForm()
# #     if form.validate_on_submit():
# #         # 如果表单校验成功就进行密码重置的操作
# #         user.set_password(form.password.data)
# #         db.session.commit()
# #         flash('重置密码成功')
# #         return redirect(url_for('login'))
# #     return render_template('reset_password.html', form=form)
