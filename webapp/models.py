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
        # 将NaN替换为空字符串
        self.df = self.df.fillna('')
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
            {'position': 'The Past', 'card': selected[0], 'reversed': orientations[0]},
            {'position': 'The Present', 'card': selected[1], 'reversed': orientations[1]},
            {'position': 'The Future', 'card': selected[2], 'reversed': orientations[2]},
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
            'How you feel about yourself',
            'What you want most right now',
            'Your fears',
            'What is going for you',
            'What is going against you',
            'The likely outcome',
        ]

        result = []
        for i, pos in enumerate(positions):
            result.append({
                'position': pos,
                'card': selected[i],
                'reversed': orientations[i]
            })

        return result
