from django.db import models


class StockCategory(models.Model):
    category_name = models.CharField(max_length=20)
    category_name_display = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name_display


class Stock(models.Model):
    stock_category = models.ForeignKey(StockCategory, on_delete=models.CASCADE)
    stock_name = models.CharField(max_length=20)
    stock_quote = models.CharField(max_length=10)

    def __str__(self):
        return self.stock_name
