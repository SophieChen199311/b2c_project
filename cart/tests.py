from django.test import TestCase
import json, requests

from goods.models import Goods
from requests import Response

# Create your tests here.
class CartTestCase(TestCase):
    BASE_URL = "http://127.0.0.1:8000/cart/cart_detail"
    # def setUp(self):
    #     goods_lst = [{"goods_name":"T-shirt", "goods_price":30.99, "ship_from":"US", "weight":0.2},
    #                 {"goods_name":"Blouse", "goods_price":10.99, "ship_from":"UK", "weight":0.3},
    #                 {"goods_name":"Pants", "goods_price":64.99, "ship_from":"UK", "weight":0.9},
    #                 {"goods_name":"Sweatpants", "goods_price":84.99, "ship_from":"CN", "weight":1.1},
    #                 {"goods_name":"Jacket", "goods_price":199.99, "ship_from":"US", "weight":2.2},
    #                 {"goods_name":"Shoes", "goods_price":79.99, "ship_from":"CN", "weight":1.3}]
    #     for goods in goods_lst:
    #         Goods.objects.create(**goods)
    def get(self):
        params = {
            "user_id":2
        }
        ret = requests.get(self.BASE_URL, params=params)
        self.result = (json.loads(ret.content), ret.status_code)

    def test_get_goods_in_cart(self):
        self.get()
        self.assertEqual(200, self.result[1])
        errmsg = self.result[0].get("errmsg")
        self.assertEqual('$386.95', errmsg.get("Subtotal"))
        self.assertEqual('$110.0', errmsg.get("Shipping"))
        self.assertEqual('$54.173', errmsg.get("VAT"))
        self.assertEqual('$433.129', errmsg.get("Total"))
        self.assertEqual('-$7.999', errmsg.get("Discounts").get("10% off shoes"))
        self.assertEqual('-$99.995', errmsg.get("Discounts").get("50% off jacket"))
        self.assertEqual('-$10', errmsg.get("Discounts").get("$10 off shipping"))


