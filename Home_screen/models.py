from django.db import models

class Meter_data(models.Model):
    timestamp = models.DateTimeField()     
    Water_consumption = models.FloatField()


