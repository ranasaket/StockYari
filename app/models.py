from django.db import models

class Index(models.Model):
    name = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name

class DailyPrice(models.Model):
    index = models.ForeignKey(Index, on_delete=models.CASCADE, related_name='index')
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    shares_traded = models.BigIntegerField()
    turnover = models.DecimalField(max_digits=15, decimal_places=2)
    
    class Meta:
        unique_together = ('index', 'date')
    
    def __str__(self):
        return f"{self.index.name} - {self.date}"