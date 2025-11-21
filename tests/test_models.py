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
