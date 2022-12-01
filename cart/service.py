from goods.models import Goods
from django_redis import get_redis_connection

from utils.constants import SHIPPING_RATE

def put_goods_in_cart(user_id, goods_id_lst, num):
    the_goods = Goods.objects.filter(pk__in=goods_id_lst).all()
    # return Response({"errmsg": "the goods doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
    if len(the_goods) != len(goods_id_lst):
        return False
    redis = get_redis_connection("cart")
    for goods_id in goods_id_lst:
        original_num = redis.hget(f"cart_{user_id}", goods_id)  # if the goods is already in cart
        if not original_num:
            original_num = 0
        else:
            original_num = int(original_num.decode())
        redis.hset(f"cart_{user_id}", goods_id, original_num + num)
        cart_total = redis.hlen(f"cart_{user_id}")
        return (the_goods, cart_total)


def discount_oper(invoice_info, goods_total_amount, has_shoes, has_jacket, top_outfit_amount, discount, shoes_num):
    #to calculate the discounts
    if goods_total_amount >= 2:  # if goods amount is more than 2, get $10 off for shipping discount
        discount += 10
        invoice_info["Discounts"]["$10 off shipping"] = "-$10"
    if has_shoes:  # shoes get 10% off for each pair
        shoes_price = Goods.objects.filter(goods_name="Shoes").first().goods_price
        discount += float(shoes_price) * 0.1 * shoes_num
        invoice_info["Discounts"]["10% off shoes"] = f"-${float(shoes_price) * 0.1 * shoes_num}"
    if top_outfit_amount >= 2 and has_jacket:  # 2 or more top outfit, get 50% off for one jacket
        jacket_price = Goods.objects.filter(goods_name="Jacket").first().goods_price
        discount += float(jacket_price) * 0.5
        invoice_info["Discounts"]["50% off jacket"] = f"-${float(jacket_price) * 0.5}"
    return discount

def get_goods_from_cart(user_id):
    redis = get_redis_connection("cart")
    cart_hash = redis.hgetall(f"cart_{user_id}")
    if len(cart_hash) < 1:
        return False
    # get goods on the cart
    # cart  = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 2)]
    cart = [(int(key.decode()), int(value.decode())) for key, value in cart_hash.items()]
    goods_total_amount = 0  # to record the total amount of the goods
    top_outfit_amount = 0  # to record the amount of the top outfit
    total_price = 0  # to record the total price of all goods
    has_jacket = 0  # if has jacket, change the value to 1
    has_shoes = 0  # if has shoes, change the value to 1
    shipping_total = 0  # to record shipping fee(before discount)
    discount = 0  # to record discount
    shoes_num = 0  # to record shoes number
    invoice_info = {"Discounts": {}}
    for goods_id, goods_amount in cart:
        goods_total_amount += goods_amount  # the amount of goods
        the_goods = Goods.objects.filter(pk=goods_id).first()
        the_shipping = SHIPPING_RATE.get(the_goods.ship_from) * the_goods.weight * goods_amount * 10
        shipping_total += the_shipping
        if the_goods:
            the_goods_price = the_goods.goods_price * goods_amount
            total_price += the_goods_price  # the price before discount
            if the_goods.goods_name == "T-shirt" or the_goods.goods_name == "Blouse":  # 如果上t-shirt或是blouse,记录
                top_outfit_amount += goods_amount
            if the_goods.goods_name == "Jacket":
                has_jacket = 1
            if the_goods.goods_name == "Shoes":
                has_shoes = 1
                shoes_num += 1
    VAT = round(float(total_price) * 0.14, 4)
    final_discount = discount_oper(invoice_info, goods_total_amount, has_shoes, has_jacket, top_outfit_amount,
                                   discount, shoes_num)
    all_price = float(total_price) - final_discount + shipping_total + VAT
    invoice_info["Subtotal"] = f"${total_price}"
    invoice_info["Shipping"] = f"${shipping_total}"
    invoice_info["VAT"] = f"${VAT}"
    invoice_info["Total"] = f"${all_price}"
    if not invoice_info["Discounts"]:
        del invoice_info["Discounts"]
    return invoice_info

