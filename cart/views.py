from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .service import put_goods_in_cart, get_goods_from_cart

# Create your views here.

class CartAPIView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        goods_id_lst = request.data.get("goods_id_lst", None)
        num = request.data.get("goods_number", 1)
        res = put_goods_in_cart(user_id, goods_id_lst, num)
        if res:
            return Response({"errmsg": f"You have successfully added {[g.goods_name for g in res[0]]} in the cart!", "cart_total": res[1]},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"errmsg": "the goods doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        #http://127.0.0.1:8000/cart/cart_detail?user_id=2
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response({"errmsg": "the user doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        res = get_goods_from_cart(user_id)
        if res:
            return Response({"errmsg": res}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "There is no goods in your cart"}, status=status.HTTP_400_BAD_REQUEST)


