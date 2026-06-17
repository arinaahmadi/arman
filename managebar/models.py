from django.db import models

# Create your models here.
class Barnameh(models.Model):
    shbarnameh = models.CharField(max_length=10)
    Barnameh_date = models.CharField(max_length=10)
    driver_fname = models.CharField(max_length=100)
    driver_lname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=11)
