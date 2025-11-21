"""
测试Flask路由
"""
import unittest
from webapp import create_app

class TestRoutes(unittest.TestCase):
    """测试路由功能"""

    def setUp(self):
        """设置测试环境"""
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_index_page(self):
        """测试首页"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # 检查页面包含塔罗牌相关内容
        self.assertIn(b'\xe5\xa1\x94\xe7\xbd\x97\xe7\x89\x8c', response.data)  # "塔罗牌"的UTF-8编码

    def test_one_card_page(self):
        """测试单卡占卜页面"""
        response = self.client.get('/one-card')
        self.assertEqual(response.status_code, 200)

    def test_three_cards_page(self):
        """测试三卡占卜页面"""
        response = self.client.get('/three-cards')
        self.assertEqual(response.status_code, 200)

    def test_six_cards_page(self):
        """测试六卡占卜页面"""
        response = self.client.get('/six-cards')
        self.assertEqual(response.status_code, 200)

    def test_browse_page(self):
        """测试浏览牌库页面"""
        response = self.client.get('/browse')
        self.assertEqual(response.status_code, 200)

    def test_404_page(self):
        """测试404页面"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
