# 任务001: 数据提取与整合

**状态**: ✅ 已完成
**负责人**: Claude Code
**优先级**: P0（最高）
**实际时间**: 25分钟
**依赖**: 无
**创建时间**: 2025-11-21
**完成时间**: 2025-11-21

---

## 任务目标

从参考项目 `reference_project/python-tarot-master` 提取78张完整塔罗牌数据和图片资源，转换为CSV格式并整合到当前项目中。

---

## 详细步骤

### 第1步：分析参考项目数据结构（5分钟）

1. 读取 `reference_project/python-tarot-master/webapp/cards.py`
2. 理解数据结构：
   ```python
   {
       "name": "The Magician",
       "url": "the_magician",
       "image": "images/01.jpeg",
       "desc": "正位描述",
       "rdesc": "逆位描述",
       "message": "核心信息",
       "qabalah": "Qabalah路径",
       "hebrew_letter": "希伯来字母",
       "meditation": "冥想文本",
       "sequence": 1,
       "cardtype": "major"
   }
   ```
3. 统计牌数量：
   - 22张大牌（Major Arcana）
   - 56张小牌（Minor Arcana：权杖/圣杯/宝剑/星币各14张）
   - 总计78张

### 第2步：提取牌数据（10分钟）

创建Python脚本 `scripts/extract_cards.py`：

```python
import pandas as pd
import sys
sys.path.append('../reference_project/python-tarot-master/webapp')
from cards import get_deck

# 提取数据
deck = get_deck()

# 转换为DataFrame
df = pd.DataFrame(deck)

# 保存为CSV
df.to_csv('data/TarotCards_Full.csv', index=False, encoding='utf-8')

print(f"成功提取 {len(deck)} 张牌数据")
```

### 第3步：复制图片资源（10分钟）

1. 定位图片目录：
   ```
   reference_project/python-tarot-master/webapp/static/images/
   ```

2. 复制到当前项目：
   ```bash
   mkdir -p webapp/static/images
   cp reference_project/python-tarot-master/webapp/static/images/*.jpeg webapp/static/images/
   ```

3. 验证文件数量：
   ```bash
   ls -l webapp/static/images/ | wc -l  # 应该是78张
   ```

### 第4步：数据验证（5分钟）

创建验证脚本 `scripts/validate_data.py`：

```python
import pandas as pd

# 读取CSV
df = pd.read_csv('data/TarotCards_Full.csv')

# 验证检查
print("数据验证报告:")
print(f"总牌数: {len(df)}")
print(f"大牌数量: {len(df[df['cardtype'] == 'major'])}")
print(f"小牌数量: {len(df[df['cardtype'] == 'minor'])}")

# 检查缺失值
print("\n缺失值检查:")
print(df.isnull().sum())

# 检查必需字段
required_fields = ['name', 'desc', 'rdesc', 'image', 'cardtype']
for field in required_fields:
    assert field in df.columns, f"缺少字段: {field}"
    assert df[field].notnull().all(), f"字段 {field} 存在空值"

print("\n✅ 数据验证通过")
```

---

## 验收标准

- [ ] CSV文件创建成功：`data/TarotCards_Full.csv`
- [ ] CSV包含78行数据（不含表头）
- [ ] 包含所有必需字段：name, desc, rdesc, message, qabalah, hebrew_letter, meditation, cardtype, sequence, image
- [ ] 22张大牌（cardtype='major'）
- [ ] 56张小牌（cardtype='minor' 或 'court'）
- [ ] 78张图片文件复制到 `webapp/static/images/`
- [ ] 图片文件名与CSV中image字段一致
- [ ] 无缺失值（除非字段本身可选）
- [ ] 数据验证脚本运行通过

---

## 输出文件

1. **数据文件**
   - `data/TarotCards_Full.csv` - 完整78张牌数据

2. **图片资源**
   - `webapp/static/images/01.jpeg` ~ `78.jpeg` - 78张牌图

3. **脚本文件**
   - `scripts/extract_cards.py` - 数据提取脚本
   - `scripts/validate_data.py` - 数据验证脚本

---

## 潜在风险

### 风险1：数据格式不兼容
- **描述**: 参考项目数据结构可能与预期不同
- **影响**: 中等
- **缓解**: 先分析数据结构，再编写转换脚本

### 风险2：图片文件路径问题
- **描述**: 图片路径可能相对路径不正确
- **影响**: 低
- **缓解**: 使用绝对路径，验证文件存在性

### 风险3：编码问题
- **描述**: CSV文件可能出现中文乱码
- **影响**: 中等
- **缓解**: 明确指定 UTF-8 编码

---

## 依赖资源

- Python 3.10+
- Pandas库
- 参考项目：`reference_project/python-tarot-master`
- 目标目录：`data/`, `webapp/static/images/`

---

## 后续任务

完成后进入：
- [002-flask-setup.md](002-flask-setup.md) - Flask应用架构搭建

---

## 进度记录

| 日期 | 进度 | 备注 |
|------|------|------|
| 2025-11-21 | 任务创建 | 文档规划阶段 |
| 2025-11-21 | ✅ 已完成 | 成功提取78张牌数据和图片 |

---

## 完成总结

### 交付物清单
- [x] `data/TarotCards_Full.csv` - 78张牌数据 (34.40 KB)
- [x] `webapp/static/images/*.jpeg` - 78张牌图片
- [x] `scripts/extract_cards.py` - 数据提取脚本
- [x] `scripts/validate_data.py` - 数据验证脚本

### 验收结果
- [x] CSV包含78行数据
- [x] 包含11个字段（name, url, image, desc, message, rdesc, sequence, qabalah, hebrew_letter, meditation, cardtype）
- [x] 22张大牌（major）
- [x] 56张其他牌（minor: 36, court: 16, ace: 4）
- [x] 78张图片文件全部存在
- [x] 图片文件名与CSV中image字段一致
- [x] 序列号1~78无重复

### 注意事项
- **缺失值**: 小牌（minor/court/ace）的部分字段为空（message, hebrew_letter, meditation），这是正常的，因为这些是大牌特有的神秘学元数据
- **编码问题**: Windows命令行显示中文乱码（GBK编码），但CSV文件使用UTF-8编码保存，Web应用中可正常显示

---

**最后更新**: 2025-11-21
