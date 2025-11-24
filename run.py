"""
Flask应用启动器
运行方式: python run.py
"""
import os
from webapp import create_app

app = create_app()

if __name__ == '__main__':
    # 从环境变量读取端口（Render 会动态分配）
    port = int(os.environ.get('PORT', 5000))

    # 根据环境变量决定 debug 模式（生产环境禁用 debug）
    debug = os.environ.get('FLASK_ENV') == 'development'

    app.run(host='0.0.0.0', port=port, debug=debug)
