# 任务003: Web界面开发

**状态**: ✅ 已完成
**负责人**: Claude Code
**优先级**: P1（高）
**预计时间**: 60分钟
**实际用时**: 约30分钟
**依赖**: [002-flask-setup.md](002-flask-setup.md) ✅
**创建时间**: 2025-11-21
**完成时间**: 2025-11-21

---

## 任务目标

开发完整的Web界面，包括7个HTML模板、CSS样式、路由实现，提供现代化的用户体验。

---

## 详细步骤

### 第1步：创建静态资源（15分钟）

#### `webapp/static/css/style.css`

```css
/* 自定义样式 */
:root {
    --primary-color: #6f42c1;
    --secondary-color: #ffc107;
    --dark-bg: #2c3e50;
    --light-bg: #ecf0f1;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--light-bg);
}

.navbar-brand {
    font-weight: bold;
    font-size: 1.5rem;
}

.hero-section {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 60px 0;
    text-align: center;
    border-radius: 10px;
    margin-bottom: 30px;
}

.card-option {
    transition: transform 0.3s, box-shadow 0.3s;
    cursor: pointer;
}

.card-option:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.tarot-card-img {
    max-width: 100%;
    height: auto;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.reading-result {
    background: white;
    padding: 30px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-position {
    font-weight: bold;
    color: var(--primary-color);
    font-size: 1.2rem;
    margin-bottom: 10px;
}

.card-name {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 5px;
}

.card-orientation {
    color: #dc3545;
    font-style: italic;
}

.reversed {
    transform: rotate(180deg);
}

footer {
    margin-top: 50px;
    background-color: var(--dark-bg);
    color: white;
}
```

### 第2步：创建首页模板（10分钟）

#### `webapp/templates/index.html`

```html
{% extends "base.html" %}

{% block title %}首页 - 塔罗牌占卜{% endblock %}

{% block content %}
<div class="hero-section">
    <h1 class="display-4">欢迎来到塔罗牌占卜平台</h1>
    <p class="lead">探索78张神秘塔罗牌的智慧，寻找内心的答案</p>
</div>

<div class="row">
    <div class="col-md-4 mb-4">
        <div class="card card-option h-100">
            <div class="card-body text-center">
                <h3 class="card-title">单卡占卜</h3>
                <p class="card-text">快速获取一天的指引，适合每日占卜</p>
                <a href="/one-card" class="btn btn-primary">开始</a>
            </div>
        </div>
    </div>

    <div class="col-md-4 mb-4">
        <div class="card card-option h-100">
            <div class="card-body text-center">
                <h3 class="card-title">三卡占卜</h3>
                <p class="card-text">过去-现在-未来，洞察事件发展脉络</p>
                <a href="/three-cards" class="btn btn-primary">开始</a>
            </div>
        </div>
    </div>

    <div class="col-md-4 mb-4">
        <div class="card card-option h-100">
            <div class="card-body text-center">
                <h3 class="card-title">六卡通用占卜</h3>
                <p class="card-text">全方位分析当前状态与未来走向</p>
                <a href="/six-cards" class="btn btn-primary">开始</a>
            </div>
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-md-6 offset-md-3 text-center">
        <div class="card">
            <div class="card-body">
                <h4>学习塔罗</h4>
                <p>浏览完整的78张塔罗牌库，学习每张牌的含义</p>
                <a href="/browse" class="btn btn-outline-primary">浏览牌库</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 第3步：创建占卜页面模板（20分钟）

#### `webapp/templates/one_card.html`

```html
{% extends "base.html" %}

{% block title %}单卡占卜{% endblock %}

{% block content %}
<h2 class="text-center mb-4">单卡占卜</h2>

<div class="reading-result text-center">
    <div class="mb-4">
        <img src="{{ url_for('static', filename=card['image']) }}"
             alt="{{ card['name'] }}"
             class="tarot-card-img {% if reversed %}reversed{% endif %}"
             style="max-width: 300px;">
    </div>

    <h3 class="card-name">{{ card['name'] }}</h3>
    <p class="card-orientation">
        {% if reversed %}
            逆位 (Reversed)
        {% else %}
            正位 (Upright)
        {% endif %}
    </p>

    <hr>

    <div class="text-start">
        <h5>解读：</h5>
        <p>{{ card['rdesc'] if reversed else card['desc'] }}</p>

        {% if card['message'] %}
        <h5>核心信息：</h5>
        <p>{{ card['message'] }}</p>
        {% endif %}

        {% if card['meditation'] %}
        <h5>冥想文本：</h5>
        <p><em>{{ card['meditation'] }}</em></p>
        {% endif %}
    </div>

    <div class="mt-4">
        <a href="/one-card" class="btn btn-primary">重新抽牌</a>
        <a href="/" class="btn btn-outline-secondary">返回首页</a>
    </div>
</div>
{% endblock %}
```

#### `webapp/templates/three_cards.html`

```html
{% extends "base.html" %}

{% block title %}三卡占卜{% endblock %}

{% block content %}
<h2 class="text-center mb-4">三卡占卜 - 过去·现在·未来</h2>

{% for reading in readings %}
<div class="reading-result">
    <div class="row">
        <div class="col-md-4 text-center">
            <img src="{{ url_for('static', filename=reading['card']['image']) }}"
                 alt="{{ reading['card']['name'] }}"
                 class="tarot-card-img {% if reading['reversed'] %}reversed{% endif %}"
                 style="max-width: 200px;">
        </div>
        <div class="col-md-8">
            <p class="card-position">{{ reading['position'] }}</p>
            <h4 class="card-name">{{ reading['card']['name'] }}</h4>
            <p class="card-orientation">
                {% if reading['reversed'] %}逆位{% else %}正位{% endif %}
            </p>
            <hr>
            <p>{{ reading['card']['rdesc'] if reading['reversed'] else reading['card']['desc'] }}</p>
        </div>
    </div>
</div>
{% endfor %}

<div class="text-center mt-4">
    <a href="/three-cards" class="btn btn-primary">重新抽牌</a>
    <a href="/" class="btn btn-outline-secondary">返回首页</a>
</div>
{% endblock %}
```

#### `webapp/templates/six_cards.html`

```html
{% extends "base.html" %}

{% block title %}六卡通用占卜{% endblock %}

{% block content %}
<h2 class="text-center mb-4">六卡通用占卜</h2>

<div class="row">
    {% for reading in readings %}
    <div class="col-md-6 mb-4">
        <div class="reading-result">
            <p class="card-position">{{ reading['position'] }}</p>
            <div class="text-center mb-3">
                <img src="{{ url_for('static', filename=reading['card']['image']) }}"
                     alt="{{ reading['card']['name'] }}"
                     class="tarot-card-img {% if reading['reversed'] %}reversed{% endif %}"
                     style="max-width: 150px;">
            </div>
            <h5 class="card-name">{{ reading['card']['name'] }}</h5>
            <p class="card-orientation">
                {% if reading['reversed'] %}逆位{% else %}正位{% endif %}
            </p>
            <p>{{ reading['card']['rdesc'] if reading['reversed'] else reading['card']['desc'] }}</p>
        </div>
    </div>
    {% endfor %}
</div>

<div class="text-center mt-4">
    <a href="/six-cards" class="btn btn-primary">重新抽牌</a>
    <a href="/" class="btn btn-outline-secondary">返回首页</a>
</div>
{% endblock %}
```

### 第4步：创建牌库浏览页面（10分钟）

#### `webapp/templates/browse_cards.html`

```html
{% extends "base.html" %}

{% block title %}浏览牌库{% endblock %}

{% block content %}
<h2 class="text-center mb-4">塔罗牌库</h2>

<!-- 分类标签 -->
<ul class="nav nav-tabs mb-4" id="cardTypeTabs" role="tablist">
    <li class="nav-item">
        <a class="nav-link active" data-bs-toggle="tab" href="#all">全部 (78)</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" data-bs-toggle="tab" href="#major">大阿卡纳 (22)</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" data-bs-toggle="tab" href="#minor">小阿卡纳 (56)</a>
    </li>
</ul>

<div class="tab-content">
    <!-- 全部牌 -->
    <div class="tab-pane fade show active" id="all">
        <div class="row">
            {% for card in cards %}
            <div class="col-md-3 col-sm-6 mb-4">
                <div class="card h-100">
                    <img src="{{ url_for('static', filename=card['image']) }}"
                         class="card-img-top" alt="{{ card['name'] }}">
                    <div class="card-body text-center">
                        <h6>{{ card['name'] }}</h6>
                        <a href="/card/{{ card['url'] }}" class="btn btn-sm btn-outline-primary">查看详情</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- 大阿卡纳 -->
    <div class="tab-pane fade" id="major">
        <div class="row">
            {% for card in cards if card['cardtype'] == 'major' %}
            <div class="col-md-3 col-sm-6 mb-4">
                <div class="card h-100">
                    <img src="{{ url_for('static', filename=card['image']) }}"
                         class="card-img-top" alt="{{ card['name'] }}">
                    <div class="card-body text-center">
                        <h6>{{ card['name'] }}</h6>
                        <a href="/card/{{ card['url'] }}" class="btn btn-sm btn-outline-primary">查看详情</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- 小阿卡纳 -->
    <div class="tab-pane fade" id="minor">
        <div class="row">
            {% for card in cards if card['cardtype'] != 'major' %}
            <div class="col-md-3 col-sm-6 mb-4">
                <div class="card h-100">
                    <img src="{{ url_for('static', filename=card['image']) }}"
                         class="card-img-top" alt="{{ card['name'] }}">
                    <div class="card-body text-center">
                        <h6>{{ card['name'] }}</h6>
                        <a href="/card/{{ card['url'] }}" class="btn btn-sm btn-outline-primary">查看详情</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

#### `webapp/templates/card_detail.html`

```html
{% extends "base.html" %}

{% block title %}{{ card['name'] }} - 牌详情{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-4 text-center">
        <img src="{{ url_for('static', filename=card['image']) }}"
             alt="{{ card['name'] }}"
             class="tarot-card-img mb-3"
             style="max-width: 100%;">

        <!-- 导航按钮 -->
        <div class="d-flex justify-content-between mt-3">
            {% if prev_card %}
            <a href="/card/{{ prev_card['url'] }}" class="btn btn-outline-secondary">
                ← {{ prev_card['name'] }}
            </a>
            {% else %}
            <span></span>
            {% endif %}

            {% if next_card %}
            <a href="/card/{{ next_card['url'] }}" class="btn btn-outline-secondary">
                {{ next_card['name'] }} →
            </a>
            {% else %}
            <span></span>
            {% endif %}
        </div>
    </div>

    <div class="col-md-8">
        <h2>{{ card['name'] }}</h2>
        <p class="text-muted">序列: {{ card['sequence'] }} | 类型: {{ card['cardtype']|upper }}</p>

        <hr>

        <h4>正位解读</h4>
        <p>{{ card['desc'] }}</p>

        <h4>逆位解读</h4>
        <p>{{ card['rdesc'] }}</p>

        {% if card['message'] %}
        <h4>核心信息</h4>
        <p>{{ card['message'] }}</p>
        {% endif %}

        {% if card['qabalah'] %}
        <h4>Qabalah路径</h4>
        <p>{{ card['qabalah'] }}</p>
        {% endif %}

        {% if card['hebrew_letter'] %}
        <h4>希伯来字母</h4>
        <p style="font-size: 2rem;">{{ card['hebrew_letter'] }}</p>
        {% endif %}

        {% if card['meditation'] %}
        <h4>冥想文本</h4>
        <p><em>{{ card['meditation'] }}</em></p>
        {% endif %}

        <hr>

        <a href="/browse" class="btn btn-primary">返回牌库</a>
        <a href="/" class="btn btn-outline-secondary">返回首页</a>
    </div>
</div>
{% endblock %}
```

### 第5步：实现路由（5分钟）

更新 `webapp/routes.py`，添加所有路由实现（代码见任务004）。

---

## 验收标准

- [ ] 7个HTML模板全部创建
- [ ] CSS样式文件创建并生效
- [ ] 所有页面响应式设计正常
- [ ] Bootstrap组件正常工作
- [ ] 图片路径正确显示
- [ ] 导航栏链接可点击
- [ ] 模板继承关系正确
- [ ] 移动端显示友好

---

## 输出文件

1. **模板文件（7个）**
   - `webapp/templates/index.html`
   - `webapp/templates/one_card.html`
   - `webapp/templates/three_cards.html`
   - `webapp/templates/six_cards.html`
   - `webapp/templates/browse_cards.html`
   - `webapp/templates/card_detail.html`
   - `webapp/templates/base.html`（已有）

2. **静态资源**
   - `webapp/static/css/style.css`

---

## 后续任务

完成后进入：
- [004-core-features.md](004-core-features.md) - 核心功能实现

---

## 进度记录

| 日期 | 进度 | 备注 |
|------|------|------|
| 2025-11-21 | 任务创建 | 等待002完成 |
| 2025-11-21 | 任务完成 | 7个HTML模板+CSS样式全部创建 |

---

**最后更新**: 2025-11-21
