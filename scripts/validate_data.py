"""
数据验证脚本
验证提取的塔罗牌数据完整性和图片资源
"""
import pandas as pd
import os
from pathlib import Path

def main():
    print("=" * 70)
    print("塔罗牌数据验证报告")
    print("=" * 70)

    # 获取路径
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    csv_path = project_root / 'data' / 'TarotCards_Full.csv'
    img_dir = project_root / 'webapp' / 'static' / 'images'

    # 检查CSV文件存在
    if not csv_path.exists():
        print(f"\n[ERROR] CSV文件不存在: {csv_path}")
        return False

    # 读取CSV
    try:
        df = pd.read_csv(csv_path)
        print(f"\n[OK] CSV文件读取成功: {csv_path}")
    except Exception as e:
        print(f"\n[ERROR] CSV文件读取失败: {e}")
        return False

    # 1. 基本统计
    print("\n" + "-" * 70)
    print("【1. 基本统计】")
    print("-" * 70)
    total_cards = len(df)
    major_count = len(df[df['cardtype'] == 'major'])
    other_count = total_cards - major_count

    print(f"总牌数: {total_cards} {'[OK]' if total_cards == 78 else '[WARN] (预期78)'}")
    print(f"大牌数量: {major_count} {'[OK]' if major_count == 22 else '[WARN] (预期22)'}")
    print(f"其他牌数量: {other_count} {'[OK]' if other_count == 56 else '[WARN] (预期56)'}")

    # 2. 字段检查
    print("\n" + "-" * 70)
    print("【2. 字段检查】")
    print("-" * 70)
    expected_fields = ['name', 'url', 'image', 'desc', 'rdesc',
                       'message', 'qabalah', 'hebrew_letter',
                       'meditation', 'sequence', 'cardtype']
    actual_fields = list(df.columns)

    print(f"预期字段数: {len(expected_fields)}")
    print(f"实际字段数: {len(actual_fields)}")

    missing = set(expected_fields) - set(actual_fields)
    extra = set(actual_fields) - set(expected_fields)

    if missing:
        print(f"[WARN] 缺少字段: {missing}")
    if extra:
        print(f"[INFO] 额外字段: {extra}")
    if not missing and not extra:
        print("[OK] 字段完全匹配")

    print(f"\n实际字段列表:")
    for i, field in enumerate(actual_fields, 1):
        print(f"  {i:2d}. {field}")

    # 3. 缺失值检查
    print("\n" + "-" * 70)
    print("【3. 缺失值检查】")
    print("-" * 70)
    null_counts = df.isnull().sum()
    total_nulls = null_counts.sum()

    if total_nulls == 0:
        print("[OK] 无缺失值")
    else:
        print(f"[WARN] 存在 {total_nulls} 个缺失值:")
        for field, count in null_counts[null_counts > 0].items():
            print(f"  - {field}: {count}个")

    # 4. 牌类型分布
    print("\n" + "-" * 70)
    print("【4. 牌类型分布】")
    print("-" * 70)
    type_counts = df['cardtype'].value_counts()
    for cardtype, count in type_counts.items():
        print(f"  {cardtype}: {count}张")

    # 5. 图片文件验证
    print("\n" + "-" * 70)
    print("【5. 图片文件验证】")
    print("-" * 70)

    if not img_dir.exists():
        print(f"[WARN] 图片目录不存在: {img_dir}")
    else:
        img_files = list(img_dir.glob('*.jpeg'))
        print(f"图片目录: {img_dir}")
        print(f"图片文件数量: {len(img_files)}")

        # 检查CSV中的图片路径是否存在
        missing_images = []
        existing_images = 0

        for idx, row in df.iterrows():
            # 处理图片路径 (可能是 "images/01.jpeg" 或 "01.jpeg")
            img_filename = row['image'].replace('images/', '')
            img_path = img_dir / img_filename

            if img_path.exists():
                existing_images += 1
            else:
                missing_images.append(row['image'])

        print(f"CSV中引用的图片: {len(df)}张")
        print(f"成功找到的图片: {existing_images}张")

        if missing_images:
            print(f"\n[WARN] 缺少 {len(missing_images)} 张图片:")
            for img in missing_images[:10]:  # 只显示前10个
                print(f"   - {img}")
            if len(missing_images) > 10:
                print(f"   ... 还有 {len(missing_images) - 10} 张")
        else:
            print("[OK] 所有图片文件存在")

    # 6. 数据样例
    print("\n" + "-" * 70)
    print("【6. 数据样例】(前5张牌)")
    print("-" * 70)
    sample_cols = ['name', 'cardtype', 'sequence']
    if all(col in df.columns for col in sample_cols):
        print(df[sample_cols].head(5).to_string(index=False))
    else:
        print(df.head(5).to_string(index=False))

    # 7. 序列号检查
    if 'sequence' in df.columns:
        print("\n" + "-" * 70)
        print("【7. 序列号检查】")
        print("-" * 70)
        sequences = df['sequence'].sort_values().tolist()
        print(f"序列号范围: {min(sequences)} ~ {max(sequences)}")
        print(f"是否有重复: {'是 [WARN]' if len(sequences) != len(set(sequences)) else '否 [OK]'}")

    # 最终结论
    print("\n" + "=" * 70)
    all_pass = (
        total_cards == 78 and
        major_count == 22 and
        total_nulls == 0 and
        len(missing_images) == 0
    )

    if all_pass:
        print("[OK] 数据验证全部通过! 可以进入下一步开发。")
    else:
        print("[WARN] 数据验证存在问题，请检查上述报告。")
    print("=" * 70)

    return all_pass

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
