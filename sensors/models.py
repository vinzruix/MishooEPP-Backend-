from symtable import Class

from django.db import models

# Create your models here.

class Temperature(models.Model):
    date = models.DateTimeField(auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=6)

class Humidity(models.Model):
    date = models.DateTimeField(auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=6)

class Pressure(models.Model):
    date = models.DateTimeField(auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=6)

class CO2(models.Model):
    date = models.DateTimeField(auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=6)

class TVOC(models.Model):
    date = models.DateTimeField(auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=6)


