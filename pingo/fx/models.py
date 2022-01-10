from django.db import models



class Rate(models.Model):
    """Author."""

    currency_pare = models.CharField(max_length=10,default="USD/JPY")
    bid = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    ask = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    high = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    low = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    created_at = models.DateTimeField()

    class Meta:
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return f"{self.created_at}: {self.currency_pare},ask:{self.ask},bid:{self.bid}"
