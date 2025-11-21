# API规范文档

**项目**: 塔罗牌占卜Web应用
**版本**: v1.0
**协议**: HTTP/HTTPS
**数据格式**: HTML (当前版本) / JSON (未来版本)
**更新时间**: 2025-11-21

---

## 路由概览

| 路由 | 方法 | 功能 | 参数 | 返回 |
|------|------|------|------|------|
| `/` | GET | 首页 | - | HTML |
| `/one-card` | GET | 单卡占卜 | - | HTML |
| `/three-cards` | GET | 三卡占卜 | - | HTML |
| `/six-cards` | GET | 六卡占卜 | - | HTML |
| `/browse` | GET | 浏览牌库 | - | HTML |
| `/card/<url>` | GET | 牌详情 | url: 牌URL标识 | HTML |

---

## 详细API规范

### 1. 首页

**端点**: `/`
**方法**: GET
**功能**: 显示首页，提供占卜选项

**请求示例**:
```http
GET / HTTP/1.1
Host: localhost:5000
```

**响应**:
- **状态码**: 200 OK
- **内容类型**: text/html
- **模板**: `index.html`

**响应内容**:
- 显示3种占卜选项（单卡/三卡/六卡）
- 牌库浏览入口
- 导航栏

**错误处理**:
- 无特殊错误场景

---

### 2. 单卡占卜

**端点**: `/one-card`
**方法**: GET
**功能**: 随机抽取1张牌并显示解读

**请求示例**:
```http
GET /one-card HTTP/1.1
Host: localhost:5000
```

**响应**:
- **状态码**: 200 OK
- **内容类型**: text/html
- **模板**: `one_card.html`

**模板变量**:
```python
{
    'card': {
        'name': str,           # 牌名
        'desc': str,           # 正位描述
        'rdesc': str,          # 逆位描述
        'message': str,        # 核心信息
        'meditation': str,     # 冥想文本
        'image': str,          # 图片路径
        'cardtype': str,       # 牌类型
        'sequence': int,       # 序列号
        ...
    },
    'reversed': bool           # 是否逆位
}
```

**业务逻辑**:
1. 调用 `ReadingEngine.one_card_reading()`
2. 随机抽取1张牌
3. 随机决定正逆位（50%概率）
4. 返回牌数据和正逆位标识

**错误处理**:
- 如果CSV数据加载失败，返回500错误

---

### 3. 三卡占卜

**端点**: `/three-cards`
**方法**: GET
**功能**: 抽取3张牌（过去-现在-未来）

**请求示例**:
```http
GET /three-cards HTTP/1.1
Host: localhost:5000
```

**响应**:
- **状态码**: 200 OK
- **内容类型**: text/html
- **模板**: `three_cards.html`

**模板变量**:
```python
{
    'readings': [
        {
            'position': '过去 (The Past)',
            'card': {card_object},
            'reversed': bool
        },
        {
            'position': '现在 (The Present)',
            'card': {card_object},
            'reversed': bool
        },
        {
            'position': '未来 (The Future)',
            'card': {card_object},
            'reversed': bool
        }
    ]
}
```

**业务逻辑**:
1. 调用 `ReadingEngine.three_card_reading()`
2. 随机抽取3张不重复的牌
3. 固定比例：2张正位 + 1张逆位
4. 随机分配到3个位置
5. 返回结构化数据

**正逆位分配**:
```python
orientations = [False, False, True]  # 2正1逆
random.shuffle(orientations)         # 随机打乱
```

---

### 4. 六卡通用占卜

**端点**: `/six-cards`
**方法**: GET
**功能**: 抽取6张牌（通用布局）

**请求示例**:
```http
GET /six-cards HTTP/1.1
Host: localhost:5000
```

**响应**:
- **状态码**: 200 OK
- **内容类型**: text/html
- **模板**: `six_cards.html`

**模板变量**:
```python
{
    'readings': [
        {
            'position': '你对自己的感受 (How you feel about yourself)',
            'card': {card_object},
            'reversed': bool
        },
        {
            'position': '你最想要的东西 (What you want most right now)',
            'card': {card_object},
            'reversed': bool
        },
        {
            'position': '你的恐惧 (Your fears)',
            'card': {card_object},
            'reversed': bool
        },
        {
            'position': '对你有利的因素 (What is going for you)',
            'card': {card_object},
            'reversed': bool
        },
        {
            'position': '对你不利的因素 (What is going against you)',
            'card': {card_object},
            'reversed': bool
        },
        {
            'position': '可能的结果 (The likely outcome)',
            'card': {card_object},
            'reversed': bool
        }
    ]
}
```

**业务逻辑**:
1. 调用 `ReadingEngine.six_card_reading()`
2. 随机抽取6张不重复的牌
3. 固定比例：4张正位 + 2张逆位
4. 分配到6个位置
5. 返回结构化数据

---

### 5. 浏览牌库

**端点**: `/browse`
**方法**: GET
**功能**: 显示所有78张牌

**请求示例**:
```http
GET /browse HTTP/1.1
Host: localhost:5000
```

**响应**:
- **状态码**: 200 OK
- **内容类型**: text/html
- **模板**: `browse_cards.html`

**模板变量**:
```python
{
    'cards': [
        {card_object_1},
        {card_object_2},
        ...  # 78张牌
    ]
}
```

**前端分类**:
- **全部 (78)**: 所有牌
- **大阿卡纳 (22)**: `cardtype == 'major'`
- **小阿卡纳 (56)**: `cardtype != 'major'`

**显示格式**:
- 网格布局（Bootstrap col-md-3）
- 每张牌显示图片和名称
- 点击进入详情页

---

### 6. 牌详情

**端点**: `/card/<card_url>`
**方法**: GET
**功能**: 显示单张牌的完整信息

**路径参数**:
- `card_url` (string, required): 牌的URL标识符
  - 示例: `the_fool`, `the_magician`

**请求示例**:
```http
GET /card/the_fool HTTP/1.1
Host: localhost:5000
```

**响应**:
- **状态码**: 200 OK
- **内容类型**: text/html
- **模板**: `card_detail.html`

**模板变量**:
```python
{
    'card': {
        'name': str,           # 牌名
        'desc': str,           # 正位描述
        'rdesc': str,          # 逆位描述
        'message': str,        # 核心信息
        'qabalah': str,        # Qabalah路径
        'hebrew_letter': str,  # 希伯来字母
        'meditation': str,     # 冥想文本
        'image': str,          # 图片路径
        'cardtype': str,       # 牌类型
        'sequence': int,       # 序列号
        'url': str             # URL标识
    },
    'prev_card': {card_object} | None,  # 前一张牌
    'next_card': {card_object} | None   # 后一张牌
}
```

**业务逻辑**:
1. 根据 `card_url` 查找牌
2. 获取相邻牌（用于前后导航）
3. 返回完整牌数据

**导航逻辑**:
```python
current_index = 牌在列表中的索引
prev_card = cards[current_index - 1] if current_index > 0 else None
next_card = cards[current_index + 1] if current_index < len(cards) - 1 else None
```

**错误响应**:
- **404 Not Found**: 牌不存在
  ```python
  if not card:
      return "Card not found", 404
  ```

---

## 错误处理

### 404 Not Found

**触发条件**:
- 访问不存在的路由
- 访问不存在的牌详情

**响应**:
- **状态码**: 404
- **模板**: `404.html`

**示例**:
```http
GET /nonexistent HTTP/1.1

HTTP/1.1 404 Not Found
Content-Type: text/html
```

### 500 Internal Server Error

**触发条件**:
- CSV文件加载失败
- 数据处理异常
- 未捕获的Python异常

**响应**:
- **状态码**: 500
- **模板**: `500.html`

**日志**:
```python
app.logger.error(f"Error: {str(e)}")
```

---

## 未来API扩展（v1.5+）

### RESTful JSON API

计划在v1.5版本提供JSON API，支持前后端分离。

#### 示例端点

**GET /api/v1/cards**
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "name": "The Fool",
            "desc": "...",
            "image_url": "https://..."
        }
    ]
}
```

**POST /api/v1/reading/three-cards**
```json
{
    "status": "success",
    "data": {
        "reading_id": "uuid-xxx",
        "cards": [...]
    }
}
```

---

## 版本管理

### 当前版本: v1.0

- 仅支持Web页面（HTML）
- 无API版本号
- 无认证机制

### 计划版本: v1.5

- 引入 `/api/v1/` 前缀
- JSON响应格式
- 统一错误格式
- API认证（JWT）

---

## 性能优化

### 响应时间目标

| 端点 | 目标 | 实际 |
|------|------|------|
| `/` | < 500ms | - |
| `/one-card` | < 1s | - |
| `/three-cards` | < 1s | - |
| `/six-cards` | < 1.5s | - |
| `/browse` | < 3s | - |
| `/card/<url>` | < 1s | - |

### 优化策略

1. **数据预加载**: 应用启动时加载CSV到内存
2. **查询缓存**: 使用`@lru_cache`缓存查询结果
3. **静态资源**: CDN加速Bootstrap
4. **图片优化**: JPEG压缩（质量85%）

---

## 测试用例

### 单元测试

```python
def test_index_route():
    response = client.get('/')
    assert response.status_code == 200

def test_one_card_route():
    response = client.get('/one-card')
    assert response.status_code == 200
    assert b'tarot' in response.data.lower()

def test_card_detail_not_found():
    response = client.get('/card/nonexistent')
    assert response.status_code == 404
```

### 集成测试

```python
def test_reading_flow():
    # 1. 访问首页
    response = client.get('/')
    assert response.status_code == 200

    # 2. 开始三卡占卜
    response = client.get('/three-cards')
    assert response.status_code == 200

    # 3. 返回首页
    response = client.get('/')
    assert response.status_code == 200
```

---

**最后更新**: 2025-11-21
**审核者**: 开发团队
