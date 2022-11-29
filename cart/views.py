from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection

from goods.models import Goods
from utils.constants import SHIPPING_RATE

# Create your views here.

class CartAPIView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        goods_id = request.data.get("goods_id", None)
        num = request.data.get("goods_number", 1)
        try:
            the_goods = Goods.objects.get(pk=goods_id)
        except:
            return Response({"errmsg": "the goods doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        redis = get_redis_connection("cart")
        original_num = redis.hget(f"cart_{user_id}", goods_id) #if the goods is already in cart
        if not original_num:
            original_num = 0
        else:
            original_num = int(original_num.decode())
        redis.hset(f"cart_{user_id}", goods_id, original_num+num)
        cart_total = redis.hlen(f"cart_{user_id}")
        return Response({"errmsg": f"You have successfully added {the_goods.goods_name} in the cart!", "cart_total": cart_total},
                        status=status.HTTP_201_CREATED)

    def get(self, request):
        #http://127.0.0.1:8000/cart/cart_detail?user_id=2
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response({"errmsg": "the user doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        redis = get_redis_connection("cart")
        cart_hash = redis.hgetall(f"cart_{user_id}")
        if len(cart_hash) < 1:
            return Response({"error": "There is no goods in your cart"})
        cart = [(int(key.decode()), int(value.decode())) for key, value in cart_hash.items()]
        """
        cart = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 2)]
        """
        goods_total_amount = 0  #to record the total amount of the goods
        top_outfit_amount  = 0          #to record the amount of the top outfit
        total_price = 0         #to record the total price of all goods
        has_jacket = 0          #if has jacket, change to 1
        has_shoes = 0
        shipping_total = 0
        discount = 0
        shoes_num = 0
        invoice_info = {"Discounts":{}}
        for goods_id, goods_amount in cart:
            goods_total_amount+=goods_amount          #总量
            the_goods = Goods.objects.filter(pk=goods_id).first()
            the_shipping = SHIPPING_RATE.get(the_goods.ship_from)*the_goods.weight*goods_amount*10
            shipping_total += the_shipping
            if the_goods:
                the_goods_price = the_goods.goods_price*goods_amount
                total_price += the_goods_price  #打折前总价
                if goods_id == 1 or goods_id == 2:   #如果上t-shirt或是blouse,记录
                    top_outfit_amount += goods_amount
                if goods_id == 5:
                    has_jacket = 1
                if goods_id == 6:
                    has_shoes = 1
                    shoes_num += 1
        VAT = round(float(total_price)*0.14, 4)
        if goods_total_amount >= 2:
            discount += 10
            invoice_info["Discounts"]["$10 of shipping"] = "-$10"
        if has_shoes:
            shoes_price = Goods.objects.filter(pk=6).first().goods_price
            discount += float(shoes_price)*0.1*shoes_num
            invoice_info["Discounts"]["10% off shoes"] = f"-${float(shoes_price)*0.1*shoes_num}"
        if top_outfit_amount>=2 and has_jacket:
            jacket_price = Goods.objects.filter(pk=5).first().goods_price
            discount += float(jacket_price)*0.5
            invoice_info["Discounts"]["50% off jacket"] = f"-${float(jacket_price)*0.5}"
        all_price = float(total_price)-discount+shipping_total+VAT
        invoice_info["Subtotal"] = f"${total_price}"
        invoice_info["Shipping"] = f"${shipping_total}"
        invoice_info["VAT"] = f"${VAT}"
        invoice_info["Total"] = f"${all_price}"
        if not invoice_info["Discounts"]:
            del invoice_info["Discounts"]
        return Response({"msg": invoice_info}, status=status.HTTP_200_OK)




