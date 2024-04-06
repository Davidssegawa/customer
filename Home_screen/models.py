from django.db import models

# class Meter_data(models.Model):
#     timestamp = models.DateTimeField()     
#     text = models.FloatField(null=True)


#     def __str__(self):
#         return f"Timestamp: {self.timestamp}, Text: {self.text}"


# class WaterUnit(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return self.name

# class PrepaymentOption(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return self.name

# class Transaction(models.Model):
#     option = models.ForeignKey(PrepaymentOption, on_delete=models.CASCADE)
#     transaction_date = models.DateTimeField(auto_now_add=True)
#     confirmation_code = models.CharField(max_length=20)

#     def __str__(self):
#         return f"Transaction {self.id}: {self.option.name}"
