from django.db import models

# Create your models here.
class Goods(models.Model):
    goods_name = models.CharField(max_length=255, unique=True)
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ship_from = models.CharField(max_length=255)
    weight = models.FloatField(default=0.0)

    class Meta:
        db_table = "goods_info"
        verbose_name = "Goods"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s"%self.goods_name


