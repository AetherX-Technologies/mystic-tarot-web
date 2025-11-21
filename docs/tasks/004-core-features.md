# 任务004: 核心功能实现

**状态**: ✅ 已完成
**负责人**: Claude Code
**优先级**: P0（最高）
**预计时间**: 45分钟
**实际用时**: 约35分钟
**依赖**: [003-web-interface.md](003-web-interface.md) ✅
**创建时间**: 2025-11-21
**完成时间**: 2025-11-21

---

## 任务目标

实现所有Flask路由的业务逻辑，连接前端模板与后端数据，确保占卜功能和牌库浏览正常工作。

---

## 详细步骤

### 第1步：完善路由实现（25分钟）

更新 `webapp/routes.py`，完整代码如下：

```python
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
```

### 第2步：添加错误处理页面（5分钟）

#### `webapp/templates/404.html`

```html
{% extends "base.html" %}

{% block title %}404 - 页面未找到{% endblock %}

{% block content %}
<div class="text-center">
    <h1 style="font-size: 5rem;">404</h1>
    <h3>页面未找到</h3>
    <p class="lead">抱歉，您访问的页面不存在</p>
    <a href="/" class="btn btn-primary">返回首页</a>
</div>
{% endblock %}
```

#### `webapp/templates/500.html`

```html
{% extends "base.html" %}

{% block title %}500 - 服务器错误{% endblock %}

{% block content %}
<div class="text-center">
    <h1 style="font-size: 5rem;">500</h1>
    <h3>服务器错误</h3>
    <p class="lead">抱歉，服务器遇到了问题</p>
    <a href="/" class="btn btn-primary">返回首页</a>
</div>
{% endblock %}
```

### 第3步：数据加载测试（10分钟）

创建测试脚本 `tests/test_card_loading.py`：

```python
"""
测试卡牌数据加载
"""
import unittest
from pathlib import Path
from webapp.models import CardManager, ReadingEngine

class TestCardLoading(unittest.TestCase):
    """测试卡牌加载功能"""

    def setUp(self):
        """设置测试环境"""
        csv_path = Path(__file__).parent.parent / 'data' / 'TarotCards_Full.csv'
        self.card_manager = CardManager(csv_path)
        self.reading_engine = ReadingEngine(self.card_manager)

    def test_total_cards(self):
        """测试总卡牌数量"""
        cards = self.card_manager.get_all_cards()
        self.assertEqual(len(cards), 78, "应该有78张牌")

    def test_major_arcana(self):
        """测试大阿卡纳牌数量"""
        major_cards = self.card_manager.get_major_arcana()
        self.assertEqual(len(major_cards), 22, "应该有22张大牌")

    def test_minor_arcana(self):
        """测试小阿卡纳牌数量"""
        minor_cards = self.card_manager.get_minor_arcana()
        self.assertEqual(len(minor_cards), 56, "应该有56张小牌")

    def test_card_fields(self):
        """测试卡牌必需字段"""
        cards = self.card_manager.get_all_cards()
        required_fields = ['name', 'desc', 'rdesc', 'image', 'cardtype']

        for card in cards:
            for field in required_fields:
                self.assertIn(field, card, f"卡牌缺少字段: {field}")
                self.assertIsNotNone(card[field], f"字段 {field} 不能为空")

    def test_one_card_reading(self):
        """测试单卡占卜"""
        card, reversed = self.reading_engine.one_card_reading()
        self.assertIsNotNone(card)
        self.assertIn('name', card)
        self.assertIsInstance(reversed, bool)

    def test_three_card_reading(self):
        """测试三卡占卜"""
        readings = self.reading_engine.three_card_reading()
        self.assertEqual(len(readings), 3, "应该返回3张牌")

        positions = [r['position'] for r in readings]
        self.assertIn('过去', positions[0])
        self.assertIn('现在', positions[1])
        self.assertIn('未来', positions[2])

    def test_six_card_reading(self):
        """测试六卡占卜"""
        readings = self.reading_engine.six_card_reading()
        self.assertEqual(len(readings), 6, "应该返回6张牌")

        # 验证正逆位比例（4张正位，2张逆位）
        reversed_count = sum(1 for r in readings if r['reversed'])
        self.assertEqual(reversed_count, 2, "应该有2张逆位牌")

if __name__ == '__main__':
    unittest.main()
```

运行测试：
```bash
python -m unittest tests/test_card_loading.py
```

### 第4步：路由集成测试（5分钟）

创建路由测试 `tests/test_routes.py`：

```python
"""
测试Flask路由
"""
import unittest
from webapp import create_app

class TestRoutes(unittest.TestCase):
    """测试路由功能"""

    def setUp(self):
        """设置测试环境"""
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_index_page(self):
        """测试首页"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'tarot', response.data.lower())

    def test_one_card_page(self):
        """测试单卡占卜页面"""
        response = self.client.get('/one-card')
        self.assertEqual(response.status_code, 200)

    def test_three_cards_page(self):
        """测试三卡占卜页面"""
        response = self.client.get('/three-cards')
        self.assertEqual(response.status_code, 200)

    def test_six_cards_page(self):
        """测试六卡占卜页面"""
        response = self.client.get('/six-cards')
        self.assertEqual(response.status_code, 200)

    def test_browse_page(self):
        """测试浏览牌库页面"""
        response = self.client.get('/browse')
        self.assertEqual(response.status_code, 200)

    def test_404_page(self):
        """测试404页面"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
```

---

## 验收标准

- [ ] 所有路由正常访问（返回200）
- [ ] 单卡占卜显示1张牌
- [ ] 三卡占卜显示3张牌（过去-现在-未来）
- [ ] 六卡占卜显示6张牌
- [ ] 浏览页面显示78张牌
- [ ] 牌详情页显示完整信息
- [ ] 前后导航按钮工作正常
- [ ] 404/500错误页面正常显示
- [ ] 所有单元测试通过
- [ ] 图片路径正确加载

---

## 测试清单

### 功能测试
- [ ] 刷新页面时抽到不同的牌
- [ ] 三卡占卜中2正1逆的比例正确
- [ ] 六卡占卜中4正2逆的比例正确
- [ ] 牌详情页Qabalah/希伯来字母正确显示
- [ ] 导航按钮在首尾牌时正确隐藏

### 性能测试
- [ ] 首页加载 < 1秒
- [ ] 占卜页面加载 < 2秒
- [ ] 浏览页面（78张图）加载 < 5秒

### 兼容性测试
- [ ] Chrome浏览器正常
- [ ] Firefox浏览器正常
- [ ] Safari浏览器正常（Mac）
- [ ] Edge浏览器正常
- [ ] 移动设备（响应式）正常

---

## 输出文件

1. **路由代码**
   - `webapp/routes.py`（完整实现）

2. **错误页面**
   - `webapp/templates/404.html`
   - `webapp/templates/500.html`

3. **测试文件**
   - `tests/test_card_loading.py`
   - `tests/test_routes.py`

---

## 潜在风险

### 风险1：CSV数据字段不匹配
- **描述**: 参考项目的字段名可能与模板中使用的不一致
- **影响**: 高
- **缓解**: 提前验证字段名，统一命名规范

### 风险2：图片路径错误
- **描述**: 图片相对路径可能在模板中无法加载
- **影响**: 中等
- **缓解**: 使用Flask的url_for函数动态生成路径

### 风险3：占卜逻辑错误
- **描述**: 正逆位比例可能不符合原设计
- **影响**: 中等
- **缓解**: 编写单元测试验证逻辑

---

## 后续任务

完成后进入：
- [005-testing-deployment.md](005-testing-deployment.md) - 测试与部署

---

## 进度记录

| 日期 | 进度 | 备注 |
|------|------|------|
| 2025-11-21 | 任务创建 | 等待003完成 |
| 2025-11-21 | 任务完成 | 所有路由实现，13个测试全部通过 |

---

**最后更新**: 2025-11-21
