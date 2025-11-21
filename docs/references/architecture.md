# 系统架构设计

**项目**: 塔罗牌占卜Web应用
**版本**: v1.0
**更新时间**: 2025-11-21

---

## 架构概览

本项目采用经典的MVC（Model-View-Controller）架构模式，基于Flask框架构建。

```
┌─────────────────────────────────────────────────────────────┐
│                        用户浏览器                             │
│                   (HTML/CSS/JavaScript)                      │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP Request/Response
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                     Flask Web Server                         │
│                     (Gunicorn/Development)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │        Flask Application       │
        │         (webapp/)              │
        ├────────────────────────────────┤
        │                                │
        │  ┌──────────────────────────┐  │
        │  │   routes.py (Controller) │  │
        │  │  - URL routing           │  │
        │  │  - Request handling      │  │
        │  └──────────┬───────────────┘  │
        │             │                  │
        │             ↓                  │
        │  ┌──────────────────────────┐  │
        │  │   models.py (Model)      │  │
        │  │  - CardManager           │  │
        │  │  - ReadingEngine         │  │
        │  │  - Business Logic        │  │
        │  └──────────┬───────────────┘  │
        │             │                  │
        │             ↓                  │
        │  ┌──────────────────────────┐  │
        │  │   templates/ (View)      │  │
        │  │  - Jinja2 Templates      │  │
        │  │  - HTML Rendering        │  │
        │  └──────────────────────────┘  │
        │                                │
        └────────────────────────────────┘
                        │
                        ↓
        ┌───────────────────────────────┐
        │      Data Layer               │
        ├───────────────────────────────┤
        │  ├── TarotCards_Full.csv      │
        │  └── Static Images (78张)     │
        └───────────────────────────────┘
```

---

## 模块设计

### 1. Controller层（routes.py）

**职责**: 处理HTTP请求，调用业务逻辑，返回视图

**主要路由**:
- `/` - 首页
- `/one-card` - 单卡占卜
- `/three-cards` - 三卡占卜
- `/six-cards` - 六卡占卜
- `/browse` - 浏览牌库
- `/card/<url>` - 牌详情

**设计模式**: Blueprint模式，模块化路由管理

### 2. Model层（models.py）

#### CardManager类

**职责**: 卡牌数据管理

```python
CardManager
├── __init__(csv_path)          # 初始化，加载CSV
├── load_cards()                # 加载数据
├── get_all_cards()             # 获取所有牌
├── get_card_by_name(name)      # 按名称查询
├── get_cards_by_type(type)     # 按类型查询
├── get_major_arcana()          # 获取大牌
└── get_minor_arcana()          # 获取小牌
```

**数据结构**:
```python
{
    'name': str,
    'desc': str,
    'rdesc': str,
    'message': str,
    'qabalah': str,
    'hebrew_letter': str,
    'meditation': str,
    'cardtype': 'major'|'minor'|'court',
    'sequence': int,
    'image': str,
    'url': str
}
```

#### ReadingEngine类

**职责**: 占卜逻辑处理

```python
ReadingEngine
├── __init__(card_manager)      # 注入CardManager依赖
├── draw_cards(count)           # 随机抽牌
├── one_card_reading()          # 单卡占卜
├── three_card_reading()        # 三卡占卜
└── six_card_reading()          # 六卡占卜
```

**占卜逻辑**:
- **正逆位**: 每张牌随机决定正位/逆位
- **无重复**: 一次占卜中不会抽到重复的牌
- **固定比例**:
  - 三卡: 2正1逆
  - 六卡: 4正2逆

### 3. View层（templates/）

**模板继承结构**:

```
base.html (基础模板)
├── index.html (首页)
├── one_card.html (单卡占卜)
├── three_cards.html (三卡占卜)
├── six_cards.html (六卡占卜)
├── browse_cards.html (牌库浏览)
├── card_detail.html (牌详情)
├── 404.html (错误页面)
└── 500.html (错误页面)
```

**Jinja2特性使用**:
- 模板继承 (`{% extends %}`)
- 块定义 (`{% block %}`)
- 循环 (`{% for %}`)
- 条件 (`{% if %}`)
- URL生成 (`{{ url_for() }}`)

---

## 数据流向

### 1. 占卜请求流程

```
用户点击"开始占卜"
    ↓
浏览器发送 GET /three-cards
    ↓
Flask接收请求 → routes.three_cards()
    ↓
调用 ReadingEngine.three_card_reading()
    ↓
ReadingEngine 调用 CardManager.get_all_cards()
    ↓
CardManager 从内存返回卡牌列表
    ↓
ReadingEngine 执行随机抽牌逻辑
    ↓
返回 3张牌数据（含正逆位信息）
    ↓
routes 渲染 three_cards.html 模板
    ↓
返回 HTML 响应给浏览器
    ↓
浏览器显示占卜结果
```

### 2. 牌库浏览流程

```
用户访问 /browse
    ↓
routes.browse_cards()
    ↓
CardManager.get_all_cards()
    ↓
返回 78张牌数据
    ↓
渲染 browse_cards.html
    ↓
显示牌库网格
```

---

## 配置管理

### 配置层次结构

```python
Config (基础配置)
├── DevelopmentConfig (开发环境)
├── ProductionConfig (生产环境)
└── TestingConfig (测试环境)
```

### 配置项

**通用配置**:
- `SECRET_KEY` - Flask密钥
- `DATA_DIR` - 数据目录路径
- `CARDS_CSV` - CSV文件路径

**环境特定**:
- `DEBUG` - 调试模式
- `TESTING` - 测试模式
- `ENV` - 环境名称

---

## 依赖关系图

```
run.py
  └── webapp/__init__.py (create_app)
        ├── config.py (配置加载)
        └── routes.py (Blueprint注册)
              ├── models.py
              │     ├── CardManager (依赖 pandas)
              │     └── ReadingEngine (依赖 CardManager)
              └── templates/ (Jinja2)
```

---

## 部署架构

### 开发环境

```
[开发者电脑]
  ├── Python 3.10 (Conda环境: tarot)
  ├── Flask Development Server (端口5000)
  └── 本地文件系统
        ├── CSV数据
        └── 图片资源
```

### 生产环境（Heroku）

```
[Heroku Platform]
  ├── Web Dyno (Gunicorn)
  ├── Python 3.10.5 Runtime
  ├── Buildpack: Python
  └── 文件系统
        ├── 应用代码 (Git部署)
        ├── CSV数据 (包含在代码库)
        └── 静态资源 (Flask static处理)
```

---

## 性能优化策略

### 1. 数据加载优化

- **一次性加载**: 应用启动时加载CSV到内存
- **缓存机制**: 使用`@lru_cache`装饰器缓存查询结果
- **Pandas优化**: 使用`to_dict('records')`高效转换

### 2. 静态资源优化

- **CDN**: Bootstrap通过CDN加载
- **图片压缩**: JPEG质量85%
- **静态资源**: Flask static服务（生产环境可用Nginx）

### 3. 模板渲染优化

- **模板继承**: 减少重复代码
- **条件渲染**: 仅渲染必需内容
- **块缓存**: Jinja2缓存机制（未来实现）

---

## 扩展性设计

### 水平扩展

- 无状态设计，支持多实例部署
- 数据不存储在服务器（无session）
- 可通过Heroku增加Dyno数量

### 垂直扩展

- CardManager支持更大的牌库
- 可扩展至数千张牌而不影响性能

### 功能扩展

- **插件式占卜布局**: 继承BaseReading类
- **多数据源**: 支持JSON/数据库
- **API模式**: 可轻松拆分为前后端分离

---

## 安全性设计

### 1. 输入验证

- Flask自动转义HTML
- URL参数验证（card_url）

### 2. 配置安全

- 敏感信息存储在环境变量
- `.env`文件不提交到Git

### 3. 错误处理

- 自定义404/500页面
- 生产环境隐藏错误堆栈

---

## 技术债务

### 当前已知问题

1. **无数据库**: 所有数据存储在CSV（v1.5解决）
2. **无用户系统**: 无法保存占卜历史（v1.5解决）
3. **无API**: 仅支持Web界面（v1.5解决）

### 改进方向

1. **引入SQLAlchemy**: 数据库ORM
2. **Redis缓存**: 提升查询性能
3. **异步任务**: Celery处理后台任务

---

**最后更新**: 2025-11-21
**审核者**: 开发团队
