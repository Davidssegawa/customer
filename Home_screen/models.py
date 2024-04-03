from django.db import models

# class Meter_data(models.Model):
#     timestamp = models.DateTimeField()     
#     text = models.FloatField(null=True)


#     def __str__(self):
#         return f"Timestamp: {self.timestamp}, Text: {self.text}"


class WaterUnit(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
