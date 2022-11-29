from django.urls import path
from . import views
urlpatterns = [
    path("cart_detail", views.CartAPIView.as_view())
]
