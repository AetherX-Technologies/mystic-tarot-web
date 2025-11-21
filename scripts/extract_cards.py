"""
数据提取脚本
从参考项目提取78张塔罗牌数据并转换为CSV格式
"""
import pandas as pd
import sys
import os

# 添加参考项目路径到sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
ref_path = os.path.join(project_root, 'reference_project', 'python-tarot-master', 'webapp')
sys.path.insert(0, ref_path)

try:
    from cards import get_deck
except ImportError as e:
    print(f"错误：无法导入cards模块: {e}")
    print(f"请确保参考项目存在于: {ref_path}")
    sys.exit(1)

def main():
    print("=" * 60)
    print("塔罗牌数据提取工具")
    print("=" * 60)

    # 提取数据
    print("\n正在从参考项目提取数据...")
    try:
        deck = get_deck()
        print(f"[OK] 成功获取 {len(deck)} 张牌")
    except Exception as e:
        print(f"[ERROR] 提取失败: {e}")
        sys.exit(1)

    # 转换为DataFrame
    print("\n正在转换数据格式...")
    df = pd.DataFrame(deck)

    # 数据统计
    print("\n[数据统计]")
    print(f"总牌数: {len(df)}")
    print(f"大牌数量: {len(df[df['cardtype'] == 'major'])}")

    # 统计其他牌类型
    other_types = df[df['cardtype'] != 'major']['cardtype'].value_counts()
    if len(other_types) > 0:
        print("其他牌类型分布:")
        for cardtype, count in other_types.items():
            print(f"  - {cardtype}: {count}张")

    print(f"字段数量: {len(df.columns)}")
    print(f"字段列表: {', '.join(df.columns)}")

    # 保存为CSV
    output_path = os.path.join(project_root, 'data', 'TarotCards_Full.csv')
    print(f"\n正在保存到: {output_path}")

    try:
        df.to_csv(output_path, index=False, encoding='utf-8')
        print("[OK] CSV文件保存成功")
    except Exception as e:
        print(f"[ERROR] 保存失败: {e}")
        sys.exit(1)

    # 文件大小
    file_size = os.path.getsize(output_path)
    print(f"文件大小: {file_size / 1024:.2f} KB")

    print("\n" + "=" * 60)
    print("[OK] 数据提取完成!")
    print("=" * 60)

if __name__ == '__main__':
    main()
