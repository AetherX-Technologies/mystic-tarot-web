# 外部资源列表

**项目**: 塔罗牌占卜Web应用
**更新时间**: 2025-11-21

---

## 技术文档

### Python & Flask

- **Flask官方文档**: https://flask.palletsprojects.com/
  - 快速入门: https://flask.palletsprojects.com/en/2.3.x/quickstart/
  - 蓝图教程: https://flask.palletsprojects.com/en/2.3.x/blueprints/
  - 部署指南: https://flask.palletsprojects.com/en/2.3.x/deploying/

- **Jinja2模板引擎**: https://jinja.palletsprojects.com/
  - 模板设计: https://jinja.palletsprojects.com/en/3.1.x/templates/

- **Pandas文档**: https://pandas.pydata.org/docs/
  - CSV读取: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

- **Python官方文档**: https://docs.python.org/3/
  - PEP 8风格指南: https://peps.python.org/pep-0008/

### 前端技术

- **Bootstrap 5文档**: https://getbootstrap.com/docs/5.0/
  - 组件库: https://getbootstrap.com/docs/5.0/components/
  - 网格系统: https://getbootstrap.com/docs/5.0/layout/grid/
  - 工具类: https://getbootstrap.com/docs/5.0/utilities/

- **MDN Web Docs**: https://developer.mozilla.org/
  - HTML: https://developer.mozilla.org/en-US/docs/Web/HTML
  - CSS: https://developer.mozilla.org/en-US/docs/Web/CSS
  - JavaScript: https://developer.mozilla.org/en-US/docs/Web/JavaScript

### 部署相关

- **Heroku文档**: https://devcenter.heroku.com/
  - Python部署: https://devcenter.heroku.com/articles/getting-started-with-python
  - Procfile: https://devcenter.heroku.com/articles/procfile

- **Gunicorn文档**: https://docs.gunicorn.org/
  - 配置: https://docs.gunicorn.org/en/stable/configure.html

### Git & 版本控制

- **Git官方文档**: https://git-scm.com/doc
  - Pro Git书籍: https://git-scm.com/book/zh/v2

- **语义化版本**: https://semver.org/lang/zh-CN/
- **语义化提交**: https://www.conventionalcommits.org/zh-hans/

---

## 塔罗牌资源

### 学习资源

- **Biddy Tarot**: https://www.biddytarot.com/
  - 塔罗牌含义: https://www.biddytarot.com/tarot-card-meanings/

- **Learn Tarot**: https://www.learntarot.com/
  - 在线课程: https://www.learntarot.com/course.htm

- **Labyrinthos**: https://labyrinthos.co/
  - 塔罗牌应用: https://labyrinthos.co/pages/tarot-card-meanings

### 牌组介绍

- **Rider-Waite Tarot**: https://en.wikipedia.org/wiki/Rider%E2%80%93Waite_Tarot
  - 最经典的塔罗牌组，本项目图片基于此

- **塔罗牌历史**: https://en.wikipedia.org/wiki/Tarot

### Qabalah & 神秘学

- **生命之树（Tree of Life）**: https://en.wikipedia.org/wiki/Tree_of_life_(Kabbalah)
- **希伯来字母**: https://en.wikipedia.org/wiki/Hebrew_alphabet

---

## 开发工具

### IDE & 编辑器

- **VS Code**: https://code.visualstudio.com/
  - Python扩展: https://marketplace.visualstudio.com/items?itemName=ms-python.python
  - Flask扩展: https://marketplace.visualstudio.com/items?itemName=cstrap.flask-snippets

- **PyCharm**: https://www.jetbrains.com/pycharm/
  - Flask支持: https://www.jetbrains.com/help/pycharm/flask.html

### 包管理

- **Conda文档**: https://docs.conda.io/
  - 环境管理: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

- **pip文档**: https://pip.pypa.io/
  - requirements.txt: https://pip.pypa.io/en/stable/reference/requirements-file-format/

### 测试工具

- **unittest文档**: https://docs.python.org/3/library/unittest.html
- **pytest**: https://docs.pytest.org/
- **coverage.py**: https://coverage.readthedocs.io/

---

## 设计资源

### UI/UX设计

- **Material Design**: https://material.io/design
- **Dribbble**: https://dribbble.com/search/tarot
  - 塔罗牌UI设计灵感

### 图标库

- **Font Awesome**: https://fontawesome.com/
- **Bootstrap Icons**: https://icons.getbootstrap.com/

### 配色方案

- **Coolors**: https://coolors.co/
- **Adobe Color**: https://color.adobe.com/zh/

---

## 参考项目

### 本项目参考

- **python-tarot-master**: `reference_project/python-tarot-master`
  - GitHub: https://github.com/tanyaofei/python-tarot（假设）
  - 功能: 完整的78张牌Web应用
  - 技术栈: Flask, Bootstrap 3

### GitHub相关项目

- **Tarot Card Reading APIs**:
  - https://github.com/ekelen/tarot-api
  - https://github.com/heyitsolivia/tarot-api

- **塔罗牌数据集**:
  - https://github.com/dariusk/corpora（包含塔罗牌JSON数据）

---

## 有用的代码片段

### 1. CSV数据加载

```python
import pandas as pd

def load_tarot_cards(csv_path):
    """加载塔罗牌数据"""
    df = pd.read_csv(csv_path)
    return df.to_dict('records')
```

### 2. Flask蓝图注册

```python
from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return "Hello, Tarot!"

# 在 app 中注册
app.register_blueprint(main_bp)
```

### 3. Jinja2条件渲染

```html
{% if reversed %}
    <p class="reversed">逆位</p>
{% else %}
    <p class="upright">正位</p>
{% endif %}
```

### 4. Bootstrap网格布局

```html
<div class="row">
    {% for card in cards %}
    <div class="col-md-3 col-sm-6 mb-4">
        <div class="card">
            <img src="{{ card.image }}" class="card-img-top">
            <div class="card-body">
                <h5>{{ card.name }}</h5>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
```

### 5. 随机抽牌逻辑

```python
import random

def draw_cards(deck, count=3, orientations=None):
    """
    随机抽牌

    Args:
        deck: 牌库列表
        count: 抽牌数量
        orientations: 正逆位列表，如 [False, False, True] 表示2正1逆
    """
    selected = random.sample(deck, count)

    if orientations is None:
        orientations = [random.choice([True, False]) for _ in range(count)]
    else:
        random.shuffle(orientations)

    return list(zip(selected, orientations))
```

---

## 在线工具

### 开发工具

- **JSON在线编辑器**: https://jsoneditoronline.org/
- **正则表达式测试**: https://regex101.com/
- **Markdown编辑器**: https://stackedit.io/

### 测试工具

- **Postman**: https://www.postman.com/
  - 用于测试API（v1.5+）

- **BrowserStack**: https://www.browserstack.com/
  - 跨浏览器测试

### 性能工具

- **PageSpeed Insights**: https://pagespeed.web.dev/
- **GTmetrix**: https://gtmetrix.com/

---

## 社区资源

### Stack Overflow

- **Flask标签**: https://stackoverflow.com/questions/tagged/flask
- **Pandas标签**: https://stackoverflow.com/questions/tagged/pandas
- **塔罗牌标签**: https://stackoverflow.com/questions/tagged/tarot

### Reddit

- **r/flask**: https://www.reddit.com/r/flask/
- **r/Python**: https://www.reddit.com/r/Python/
- **r/tarot**: https://www.reddit.com/r/tarot/

### Discord服务器

- **Python Discord**: https://discord.gg/python
- **Flask Discord**: https://discord.gg/pallets

---

## 学习路径

### Flask入门（1周）

1. Flask官方快速入门教程
2. Jinja2模板基础
3. Blueprint模块化
4. 部署到Heroku

**推荐课程**:
- Corey Schafer的Flask系列: https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH

### 塔罗牌知识（2周）

1. 22张大阿卡纳含义
2. 56张小阿卡纳含义
3. 常见占卜布局
4. Qabalah基础

**推荐书籍**:
- 《塔罗全书》- 瑞秋·波拉克
- 《学习塔罗》- 琼·班纳

### Web开发进阶（持续）

1. Bootstrap高级组件
2. JavaScript交互
3. RESTful API设计
4. 数据库设计

---

## 常见问题（FAQ）

### Q1: 如何更新塔罗牌数据？

**A**: 编辑 `data/TarotCards_Full.csv`，然后重启应用。

### Q2: 如何添加新的占卜布局？

**A**: 在 `ReadingEngine` 类中添加新方法，如 `celtic_cross_reading()`。

### Q3: 如何更换牌图？

**A**: 替换 `webapp/static/images/` 中的图片文件，保持文件名一致。

### Q4: 如何支持多语言？

**A**: 使用Flask-Babel扩展，参考: https://flask-babel.tkte.ch/

---

## 持续更新

本文档会随着项目发展持续更新。如果发现有用的资源，请通过以下方式贡献：

1. 在GitHub上提交Issue
2. 直接编辑本文档并提交PR
3. 在团队讨论中分享

---

**最后更新**: 2025-11-21
**维护者**: 开发团队
**贡献者**: 欢迎补充
