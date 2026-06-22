from django.db import models

# Create your models here.
class Bank(models.Model):
    bank_name = models.CharField(max_length=100)
    account_code = models.CharField(max_length=30)
    account_holder = models.CharField(max_length=100)

    def __str__(self):
        return self.account_holder
    
class Receiver(models.Model):
    owner_code = models.CharField(max_length=15)
    owner_name = models.CharField(max_length=150)

    def __str__(self):
        return self.owner_name
    

class Barnameh(models.Model):
    shbarnameh = models.CharField(max_length=10)
    barnameh_date = models.CharField(max_length=10)
    driver_fname = models.CharField(max_length=100)
    driver_lname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=11)
    plate_number = models.CharField(max_length=7,default='')
    amount_base = models.IntegerField(default=0)
    amount_total = models.IntegerField(default=0)
    purpose = models.CharField(max_length=100,default='')
    type_pay = models.CharField(max_length=1,default='')
    receiver = models.ForeignKey(Receiver,models.SET_NULL,null=True)
    bank = models.ForeignKey(Bank,models.SET_NULL,null=True)
    pay_date = models.CharField(max_length=10,default='1405/03/30')
    status = models.CharField(max_length=1,default='1')

