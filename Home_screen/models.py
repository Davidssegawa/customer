from django.db import models

class Meter_data(models.Model):
    timestamp = models.DateTimeField()     
    text = models.FloatField(null=True)


    def __str__(self):
        return f"Timestamp: {self.timestamp}, Text: {self.text}"

