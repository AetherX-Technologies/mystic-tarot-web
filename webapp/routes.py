"""
Flask路由定义
"""
from flask import Blueprint, render_template, current_app
from webapp.models import CardManager, ReadingEngine

main_bp = Blueprint('main', __name__)

# 全局变量（应用启动时初始化）
card_manager = None
reading_engine = None

@main_bp.record_once
def on_load(state):
    """蓝图加载时初始化卡牌管理器"""
    global card_manager, reading_engine
    app = state.app
    card_manager = CardManager(app.config['CARDS_CSV'])
    reading_engine = ReadingEngine(card_manager)


@main_bp.route('/')
def index():
    """首页"""
    return render_template('index.html')


@main_bp.route('/one-card')
def one_card():
    """单卡占卜"""
    card, reversed = reading_engine.one_card_reading()
    return render_template('one_card.html', card=card, reversed=reversed)


@main_bp.route('/three-cards')
def three_cards():
    """三卡占卜（过去-现在-未来）"""
    readings = reading_engine.three_card_reading()
    return render_template('three_cards.html', readings=readings)


@main_bp.route('/six-cards')
def six_cards():
    """六卡通用占卜"""
    readings = reading_engine.six_card_reading()
    return render_template('six_cards.html', readings=readings)


@main_bp.route('/browse')
def browse_cards():
    """浏览所有牌"""
    cards = card_manager.get_all_cards()
    return render_template('browse_cards.html', cards=cards)


@main_bp.route('/card/<card_url>')
def card_detail(card_url):
    """单张牌详情页"""
    # 查找当前牌
    all_cards = card_manager.get_all_cards()
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
