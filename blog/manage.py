# 导入一个app
# 从app包中导入变量app）
# from app import app

from app import create_app
app = create_app()
# 跑起来
if __name__ == '__main__':
    app.run(debug=True)