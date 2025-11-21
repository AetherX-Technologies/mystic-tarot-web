# 任务002: Flask应用架构搭建

**状态**: ✅ 已完成
**负责人**: Claude Code
**优先级**: P0（最高）
**预计时间**: 45分钟
**实际用时**: 约50分钟
**依赖**: [001-data-extraction.md](001-data-extraction.md) ✅
**创建时间**: 2025-11-21
**完成时间**: 2025-11-21

---

## 任务目标

创建Flask Web应用的基础架构，重构现有CLI代码为Web模块，建立符合Flask最佳实践的项目结构。

---

## 详细步骤

### 第1步：创建Flask项目结构（10分钟）

创建以下目录和文件：

```
D:\code\python-game-master\python-game-master/
├── run.py                       # Flask应用启动器 [新建]
├── config.py                    # 配置文件 [新建]
├── requirements.txt             # 依赖管理 [更新]
├── .env                         # 环境变量 [新建]
├── .gitignore                   # Git忽略规则 [新建]
├── webapp/                      # Flask应用包 [新建]
│   ├── __init__.py             # 应用工厂
│   ├── routes.py               # 路由定义
│   ├── models.py               # 业务逻辑模型
│   ├── templates/              # Jinja2模板
│   │   └── base.html           # 基础模板
│   └── static/                 # 静态资源
│       ├── css/
│       ├── js/
│       └── images/             # (已有78张牌图)
└── data/                        # 数据文件
    └── TarotCards_Full.csv     # (已有)
```

### 第2步：编写核心配置文件（5分钟）

#### `run.py` - Flask启动器

```python
"""
Flask应用启动器
运行方式: python run.py
"""
from webapp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### `config.py` - 配置管理

```python
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

    # 静态资源
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'

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
```

#### `.env` - 环境变量

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DEBUG=True
```

#### 更新 `requirements.txt`

```txt
# 核心依赖
Flask==2.3.0
pandas==2.0.0
python-dotenv==1.0.0

# 生产环境
gunicorn==21.2.0

# 开发工具（可选）
pytest==7.4.0
black==23.7.0
flake8==6.1.0
```

### 第3步：重构现有代码为Flask模块（15分钟）

#### `webapp/__init__.py` - 应用工厂

```python
"""
Flask应用工厂
"""
from flask import Flask
from config import config

def create_app(config_name='default'):
    """创建Flask应用实例"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 注册蓝图
    from webapp.routes import main_bp
    app.register_blueprint(main_bp)

    return app
```

#### `webapp/models.py` - 业务逻辑（重构现有类）

```python
"""
核心业务逻辑模型
重构自原项目的 PandasToList 类
"""
import pandas as pd
import random
from pathlib import Path

class CardManager:
    """
    卡牌数据管理器
    重构自 PandasToList 类，负责加载和管理塔罗牌数据
    """
    def __init__(self, csv_path):
        """
        初始化卡牌管理器

        Args:
            csv_path (str): CSV文件路径
        """
        self.csv_path = Path(csv_path)
        self.df = None
        self.cards = []
        self.load_cards()

    def load_cards(self):
        """加载塔罗牌数据"""
        self.df = pd.read_csv(self.csv_path)
        # 转换为字典列表
        self.cards = self.df.to_dict('records')

    def get_all_cards(self):
        """获取所有卡牌"""
        return self.cards

    def get_card_by_name(self, name):
        """根据名称获取卡牌"""
        for card in self.cards:
            if card['name'].lower() == name.lower():
                return card
        return None

    def get_cards_by_type(self, cardtype):
        """根据类型获取卡牌（major/minor/court）"""
        return [c for c in self.cards if c['cardtype'] == cardtype]

    def get_major_arcana(self):
        """获取22张大牌"""
        return self.get_cards_by_type('major')

    def get_minor_arcana(self):
        """获取56张小牌"""
        return [c for c in self.cards if c['cardtype'] != 'major']


class ReadingEngine:
    """
    占卜引擎
    处理各种占卜布局的逻辑
    """
    def __init__(self, card_manager):
        """
        初始化占卜引擎

        Args:
            card_manager (CardManager): 卡牌管理器实例
        """
        self.card_manager = card_manager

    def draw_cards(self, count=1, allow_duplicates=False):
        """
        随机抽牌

        Args:
            count (int): 抽牌数量
            allow_duplicates (bool): 是否允许重复

        Returns:
            list: 抽取的卡牌列表，每个元素为 (card, is_reversed)
        """
        cards = self.card_manager.get_all_cards()

        if allow_duplicates:
            selected = random.choices(cards, k=count)
        else:
            selected = random.sample(cards, min(count, len(cards)))

        # 随机决定正逆位
        result = []
        for card in selected:
            is_reversed = random.choice([True, False])
            result.append((card, is_reversed))

        return result

    def one_card_reading(self):
        """单卡占卜"""
        return self.draw_cards(1)[0]

    def three_card_reading(self):
        """
        三卡占卜（过去-现在-未来）
        保持原逻辑：2张正位 + 1张逆位
        """
        cards = self.card_manager.get_all_cards()

        # 随机选择3张牌
        selected = random.sample(cards, 3)

        # 2张正位，1张逆位
        orientations = [False, False, True]  # False=正位, True=逆位
        random.shuffle(orientations)

        result = [
            {'position': '过去 (The Past)', 'card': selected[0], 'reversed': orientations[0]},
            {'position': '现在 (The Present)', 'card': selected[1], 'reversed': orientations[1]},
            {'position': '未来 (The Future)', 'card': selected[2], 'reversed': orientations[2]},
        ]

        return result

    def six_card_reading(self):
        """
        六卡通用占卜
        保持原逻辑：4张正位 + 2张逆位
        """
        cards = self.card_manager.get_all_cards()

        # 随机选择6张牌
        selected = random.sample(cards, 6)

        # 4张正位，2张逆位
        orientations = [False, False, False, False, True, True]
        random.shuffle(orientations)

        positions = [
            '你对自己的感受 (How you feel about yourself)',
            '你最想要的东西 (What you want most right now)',
            '你的恐惧 (Your fears)',
            '对你有利的因素 (What is going for you)',
            '对你不利的因素 (What is going against you)',
            '可能的结果 (The likely outcome)',
        ]

        result = []
        for i, pos in enumerate(positions):
            result.append({
                'position': pos,
                'card': selected[i],
                'reversed': orientations[i]
            })

        return result
```

#### `webapp/routes.py` - 路由定义（基础框架）

```python
"""
Flask路由定义
"""
from flask import Blueprint, render_template
from webapp.models import CardManager, ReadingEngine
from config import Config

main_bp = Blueprint('main', __name__)

# 初始化卡牌管理器（稍后完善）
# card_manager = CardManager(Config.CARDS_CSV)
# reading_engine = ReadingEngine(card_manager)

@main_bp.route('/')
def index():
    """首页"""
    return render_template('index.html')

# 其他路由将在任务003中实现
```

### 第4步：创建基础模板（10分钟）

#### `webapp/templates/base.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}塔罗牌占卜{% endblock %}</title>

    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- 自定义CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">塔罗牌占卜</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/">首页</a></li>
                    <li class="nav-item"><a class="nav-link" href="/one-card">单卡占卜</a></li>
                    <li class="nav-item"><a class="nav-link" href="/three-cards">三卡占卜</a></li>
                    <li class="nav-item"><a class="nav-link" href="/six-cards">六卡占卜</a></li>
                    <li class="nav-item"><a class="nav-link" href="/browse">浏览牌库</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- 主内容区 -->
    <main class="container my-5">
        {% block content %}{% endblock %}
    </main>

    <!-- 页脚 -->
    <footer class="bg-light text-center py-3 mt-5">
        <p class="mb-0">&copy; 2025 塔罗牌占卜平台 | 仅供娱乐参考</p>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 第5步：安装依赖并测试（5分钟）

```bash
# 激活conda环境
conda activate tarot

# 安装依赖
pip install -r requirements.txt

# 测试Flask应用启动
python run.py

# 访问 http://localhost:5000 验证
```

---

## 验收标准

- [ ] Flask项目结构创建完成
- [ ] `run.py` 能够成功启动应用
- [ ] `config.py` 配置正确加载
- [ ] `CardManager` 类能够加载CSV数据
- [ ] `ReadingEngine` 类能够执行占卜逻辑
- [ ] 基础路由 `/` 可访问
- [ ] `base.html` 模板正常渲染
- [ ] 所有依赖安装成功
- [ ] 无Python语法错误

---

## 输出文件

1. **应用文件**
   - `run.py`
   - `config.py`
   - `.env`
   - `.gitignore`

2. **Flask模块**
   - `webapp/__init__.py`
   - `webapp/routes.py`
   - `webapp/models.py`

3. **模板**
   - `webapp/templates/base.html`

4. **配置**
   - `requirements.txt`（更新）

---

## 潜在风险

### 风险1：依赖冲突
- **描述**: Flask版本与Pandas可能存在依赖冲突
- **影响**: 中等
- **缓解**: 使用虚拟环境，固定版本号

### 风险2：路径问题
- **描述**: CSV文件路径在不同环境可能不一致
- **影响**: 低
- **缓解**: 使用Path对象，相对路径处理

---

## 后续任务

完成后进入：
- [003-web-interface.md](003-web-interface.md) - Web界面开发

---

## 进度记录

| 日期 | 进度 | 备注 |
|------|------|------|
| 2025-11-21 | 任务创建 | 等待001完成 |
| 2025-11-21 | 任务完成 | Flask架构搭建完成，应用测试通过 |

---

**最后更新**: 2025-11-21
