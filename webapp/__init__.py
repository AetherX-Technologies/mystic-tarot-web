"""
Flask应用工厂
"""
from flask import Flask, request, session
from flask_babel import Babel
from config import config

def get_locale():
    """获取当前语言设置"""
    # 优先从session获取
    if 'language' in session:
        return session['language']
    # 从浏览器Accept-Language头获取
    return request.accept_languages.best_match(['en', 'zh'])

def create_app(config_name='default'):
    """创建Flask应用实例"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化Babel
    babel = Babel(app, locale_selector=get_locale)

    # 注册蓝图
    from webapp.routes import main_bp
    app.register_blueprint(main_bp)

    return app
