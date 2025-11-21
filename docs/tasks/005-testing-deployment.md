# 任务005: 测试与部署

**状态**: 📋 待开始
**负责人**: 待分配
**优先级**: P1（高）
**预计时间**: 30分钟
**依赖**: [004-core-features.md](004-core-features.md) ✅
**创建时间**: 2025-11-21

---

## 任务目标

完善测试覆盖，创建部署配置，准备生产环境，确保应用可以成功部署到Heroku。

---

## 详细步骤

### 第1步：扩展测试覆盖（10分钟）

#### 创建完整测试套件

`tests/test_models.py`:
```python
"""
测试业务逻辑模型
"""
import unittest
from pathlib import Path
from webapp.models import CardManager, ReadingEngine

class TestCardManager(unittest.TestCase):
    """测试CardManager类"""

    @classmethod
    def setUpClass(cls):
        """类级别的设置"""
        csv_path = Path(__file__).parent.parent / 'data' / 'TarotCards_Full.csv'
        cls.manager = CardManager(csv_path)

    def test_load_cards(self):
        """测试加载卡牌"""
        self.assertIsNotNone(self.manager.cards)
        self.assertEqual(len(self.manager.cards), 78)

    def test_get_card_by_name(self):
        """测试根据名称获取卡牌"""
        card = self.manager.get_card_by_name("The Fool")
        self.assertIsNotNone(card)
        self.assertEqual(card['name'], "The Fool")

    def test_get_card_by_name_case_insensitive(self):
        """测试名称大小写不敏感"""
        card1 = self.manager.get_card_by_name("the fool")
        card2 = self.manager.get_card_by_name("THE FOOL")
        self.assertEqual(card1['name'], card2['name'])

    def test_get_cards_by_type(self):
        """测试按类型获取卡牌"""
        major = self.manager.get_cards_by_type('major')
        self.assertEqual(len(major), 22)


class TestReadingEngine(unittest.TestCase):
    """测试ReadingEngine类"""

    @classmethod
    def setUpClass(cls):
        """类级别的设置"""
        csv_path = Path(__file__).parent.parent / 'data' / 'TarotCards_Full.csv'
        manager = CardManager(csv_path)
        cls.engine = ReadingEngine(manager)

    def test_draw_cards_count(self):
        """测试抽牌数量"""
        cards = self.engine.draw_cards(5)
        self.assertEqual(len(cards), 5)

    def test_draw_cards_no_duplicates(self):
        """测试无重复抽牌"""
        cards = self.engine.draw_cards(10, allow_duplicates=False)
        card_names = [c[0]['name'] for c in cards]
        self.assertEqual(len(card_names), len(set(card_names)))

if __name__ == '__main__':
    unittest.main()
```

#### 运行所有测试

创建 `run_tests.sh`:
```bash
#!/bin/bash

echo "运行所有测试..."
python -m unittest discover tests -v

echo ""
echo "测试覆盖率报告:"
# 需要安装 coverage: pip install coverage
# coverage run -m unittest discover tests
# coverage report
# coverage html
```

### 第2步：创建部署配置（10分钟）

#### `Procfile` - Heroku启动命令

```
web: gunicorn run:app
```

#### `runtime.txt` - Python版本

```
python-3.10.5
```

#### `.gitignore` - Git忽略规则

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
*.egg-info/
dist/
build/

# Flask
instance/
.webassets-cache

# 环境变量
.env
.flaskenv

# IDE
.vscode/
.idea/
*.swp
*.swo

# 系统文件
.DS_Store
Thumbs.db

# 测试
.coverage
htmlcov/
.pytest_cache/

# 日志
*.log

# 数据库
*.db
*.sqlite3
```

#### `README.md` - 更新项目说明

```markdown
# 塔罗牌占卜Web应用

一个功能完整的在线塔罗牌占卜平台，支持多种占卜布局、78张完整牌库、丰富的元数据展示。

## 功能特性

- ✨ 78张完整塔罗牌（22大牌 + 56小牌）
- 🎴 三种占卜模式：单卡/三卡/六卡
- 📚 牌库浏览和学习功能
- 🎨 现代化响应式设计（Bootstrap 5）
- 📱 移动设备友好

## 技术栈

- **后端**: Python 3.10, Flask 2.x, Pandas
- **前端**: Bootstrap 5, Jinja2, HTML5/CSS3
- **部署**: Gunicorn, Heroku

## 本地运行

### 环境要求

- Python 3.10+
- Conda（推荐）

### 安装步骤

1. 克隆项目
   ```bash
   git clone <repository-url>
   cd python-game-master/python-game-master
   ```

2. 创建并激活Conda环境
   ```bash
   conda create -n tarot python=3.10
   conda activate tarot
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

4. 运行应用
   ```bash
   python run.py
   ```

5. 访问 `http://localhost:5000`

## 测试

运行所有测试：
```bash
python -m unittest discover tests
```

运行特定测试：
```bash
python -m unittest tests.test_models
```

## 部署到Heroku

1. 创建Heroku应用
   ```bash
   heroku create your-app-name
   ```

2. 推送代码
   ```bash
   git push heroku main
   ```

3. 打开应用
   ```bash
   heroku open
   ```

## 项目结构

```
├── run.py                  # Flask启动器
├── config.py               # 配置管理
├── requirements.txt        # 依赖列表
├── Procfile                # Heroku配置
├── runtime.txt             # Python版本
├── webapp/                 # Flask应用
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── templates/
│   └── static/
├── data/                   # 数据文件
├── tests/                  # 测试文件
└── docs/                   # 项目文档
```

## 文档

详细文档请查看 `docs/` 目录：

- [ROADMAP.md](docs/ROADMAP.md) - 项目路线图
- [CLAUDE.md](CLAUDE.md) - 开发规范
- [tasks/](docs/tasks/) - 任务管理

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue。
```

### 第3步：性能优化（5分钟）

#### 添加缓存机制

更新 `webapp/models.py`，添加缓存装饰器：

```python
from functools import lru_cache

class CardManager:
    # ... 现有代码 ...

    @lru_cache(maxsize=128)
    def get_card_by_name_cached(self, name):
        """缓存版本的get_card_by_name"""
        return self.get_card_by_name(name)
```

#### 压缩图片（可选）

如果图片过大，使用PIL压缩：

```python
from PIL import Image

def compress_images(image_dir, quality=85):
    """压缩图片以提升加载速度"""
    for img_file in image_dir.glob('*.jpeg'):
        img = Image.open(img_file)
        img.save(img_file, 'JPEG', quality=quality, optimize=True)
```

### 第4步：部署前检查（5分钟）

创建部署前检查脚本 `scripts/deploy_check.py`:

```python
"""
部署前检查清单
"""
import sys
from pathlib import Path

def check_files():
    """检查必需文件是否存在"""
    required_files = [
        'run.py',
        'config.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'webapp/__init__.py',
        'webapp/routes.py',
        'webapp/models.py',
        'data/TarotCards_Full.csv',
    ]

    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)

    if missing:
        print("❌ 缺少以下文件:")
        for f in missing:
            print(f"  - {f}")
        return False
    else:
        print("✅ 所有必需文件存在")
        return True

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import flask
        import pandas
        import gunicorn
        print("✅ 核心依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        return False

def check_data():
    """检查数据完整性"""
    import pandas as pd

    csv_path = Path('data/TarotCards_Full.csv')
    if not csv_path.exists():
        print("❌ 数据文件不存在")
        return False

    df = pd.read_csv(csv_path)
    if len(df) != 78:
        print(f"❌ 数据文件行数错误: {len(df)} (应为78)")
        return False

    print("✅ 数据文件完整")
    return True

def main():
    """运行所有检查"""
    print("=== 部署前检查 ===\n")

    checks = [
        ("文件检查", check_files),
        ("依赖检查", check_dependencies),
        ("数据检查", check_data),
    ]

    all_passed = True
    for name, check_func in checks:
        print(f"\n{name}:")
        if not check_func():
            all_passed = False

    print("\n=== 检查结果 ===")
    if all_passed:
        print("✅ 所有检查通过，可以部署！")
        return 0
    else:
        print("❌ 部分检查失败，请修复后再部署")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

运行检查：
```bash
python scripts/deploy_check.py
```

---

## 验收标准

- [ ] 所有单元测试通过（100%）
- [ ] 测试覆盖率 ≥ 80%
- [ ] 部署配置文件完整（Procfile, runtime.txt）
- [ ] .gitignore 正确配置
- [ ] README.md 更新完整
- [ ] 本地运行无错误
- [ ] 部署前检查全部通过
- [ ] 性能优化生效（页面加载 < 3秒）

---

## 部署流程

### Heroku部署步骤

1. **安装Heroku CLI**
   ```bash
   # Windows: 下载安装包
   # Mac: brew install heroku/brew/heroku
   # Linux: curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **登录Heroku**
   ```bash
   heroku login
   ```

3. **创建应用**
   ```bash
   heroku create tarot-reading-app
   ```

4. **添加环境变量**
   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set FLASK_ENV=production
   ```

5. **部署代码**
   ```bash
   git add .
   git commit -m "feat: Web应用v1.0完成"
   git push heroku main
   ```

6. **查看日志**
   ```bash
   heroku logs --tail
   ```

7. **打开应用**
   ```bash
   heroku open
   ```

### 验证部署成功

- [ ] 首页正常访问
- [ ] 所有占卜功能正常
- [ ] 图片加载正常
- [ ] 无500错误
- [ ] 日志无异常

---

## 输出文件

1. **部署配置**
   - `Procfile`
   - `runtime.txt`
   - `.gitignore`
   - `README.md`（更新）

2. **测试文件**
   - `tests/test_models.py`
   - `run_tests.sh`

3. **工具脚本**
   - `scripts/deploy_check.py`

---

## 性能指标

### 目标指标
- 首页加载时间: < 1秒
- 占卜页面: < 2秒
- 浏览页面: < 5秒
- 服务器响应时间: < 200ms

### 监控建议
- 使用Heroku Metrics查看应用性能
- 配置错误日志监控
- 定期检查数据库连接（如有）

---

## 后续优化建议

### v1.1版本
- [ ] 添加用户反馈功能
- [ ] 实现占卜结果分享
- [ ] 优化移动端体验
- [ ] 添加更多占卜布局

### v1.5版本
- [ ] 用户登录系统
- [ ] 占卜历史记录
- [ ] 数据库集成
- [ ] API接口

---

## 进度记录

| 日期 | 进度 | 备注 |
|------|------|------|
| 2025-11-21 | 任务创建 | 等待004完成 |

---

**最后更新**: 2025-11-21
