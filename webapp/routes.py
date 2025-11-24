"""
Flask路由定义
"""
from flask import Blueprint, render_template, current_app, session, redirect, request
from webapp.models import CardManager, ReadingEngine

main_bp = Blueprint('main', __name__)

# 全局变量（应用启动时初始化）
card_manager_en = None
card_manager_zh = None
reading_engine_en = None
reading_engine_zh = None
card_manager = None
reading_engine = None

@main_bp.record_once
def on_load(state):
    """蓝图加载时初始化卡牌管理器"""
    global card_manager_en, card_manager_zh, reading_engine_en, reading_engine_zh, card_manager, reading_engine
    app = state.app
    card_manager_en = CardManager(app.config['CARDS_CSV'])
    reading_engine_en = ReadingEngine(card_manager_en)
    zh_csv = app.config.get('CARDS_CSV_ZH')
    if zh_csv:
        card_manager_zh = CardManager(zh_csv)
        reading_engine_zh = ReadingEngine(card_manager_zh)
    else:
        card_manager_zh = None
        reading_engine_zh = None
    card_manager = card_manager_en
    reading_engine = reading_engine_en


def _get_current_language():
    lang = session.get('language')
    if lang in ['en', 'zh']:
        return lang
    best_lang = request.accept_languages.best_match(['en', 'zh'])
    if best_lang in ['en', 'zh']:
        return best_lang
    return 'en'


def _get_card_manager():
    lang = _get_current_language()
    if lang == 'zh' and card_manager_zh is not None:
        return card_manager_zh
    return card_manager_en


def _get_reading_engine():
    lang = _get_current_language()
    if lang == 'zh' and reading_engine_zh is not None:
        return reading_engine_zh
    return reading_engine_en


@main_bp.context_processor
def inject_current_lang():
    return {'current_lang': _get_current_language()}


@main_bp.route('/')
def index():
    """首页"""
    return render_template('index.html')


@main_bp.route('/one-card')
def one_card():
    """单卡占卜"""
    engine = _get_reading_engine()
    card, reversed = engine.one_card_reading()
    return render_template('one_card.html', card=card, reversed=reversed)


@main_bp.route('/three-cards')
def three_cards():
    """三卡占卜（过去-现在-未来）"""
    engine = _get_reading_engine()
    readings = engine.three_card_reading()
    return render_template('three_cards.html', readings=readings)


@main_bp.route('/six-cards')
def six_cards():
    """六卡通用占卜"""
    engine = _get_reading_engine()
    readings = engine.six_card_reading()
    return render_template('six_cards.html', readings=readings)


@main_bp.route('/browse')
def browse_cards():
    """浏览所有牌"""
    manager = _get_card_manager()
    cards = manager.get_all_cards()
    return render_template('browse_cards.html', cards=cards)


@main_bp.route('/card/<card_url>')
def card_detail(card_url):
    """单张牌详情页"""
    # 查找当前牌
    manager = _get_card_manager()
    all_cards = manager.get_all_cards()
    card = None
    current_index = -1

    for i, c in enumerate(all_cards):
        if c['url'] == card_url:
            card = c
            current_index = i
            break

    if not card:
        return "Card not found", 404

    # 获取前后牌（用于导航）
    prev_card = all_cards[current_index - 1] if current_index > 0 else None
    next_card = all_cards[current_index + 1] if current_index < len(all_cards) - 1 else None

    return render_template('card_detail.html',
                         card=card,
                         prev_card=prev_card,
                         next_card=next_card)


@main_bp.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return render_template('404.html'), 404


@main_bp.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return render_template('500.html'), 500


@main_bp.route('/set-language/<lang>')
def set_language(lang):
    """设置语言"""
    if lang in ['en', 'zh']:
        session['language'] = lang
    # 重定向回来源页面，如果没有来源则回到首页
    return redirect(request.referrer or '/')
