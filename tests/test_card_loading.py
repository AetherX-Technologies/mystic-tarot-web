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
