"""
Flask应用配置
"""
import os
from pathlib import Path

class Config:
    """基础配置"""
    # 项目根目录
    BASE_DIR = Path(__file__).parent

    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # 数据文件路径
    DATA_DIR = BASE_DIR / 'data'
    CARDS_CSV = DATA_DIR / 'TarotCards_Full.csv'
    CARDS_CSV_ZH = DATA_DIR / 'tarot_chinese.csv'

    # 静态资源
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'

    # Babel国际化配置
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_SUPPORTED_LOCALES = ['en', 'zh']
    BABEL_TRANSLATION_DIRECTORIES = str(BASE_DIR / 'translations')

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    ENV = 'production'

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    WTF_CSRF_ENABLED = False

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
