from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=250)
    chat_id = models.BigIntegerField()
    name = models.CharField(max_length=350)
    address = models.TextField()
    phone = models.CharField(max_length=11)
    mobile = models.CharField(max_length=11)

    def __str__(self):
        return '{} {}'.format(self.first_name,self.name)
