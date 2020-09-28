# -*- encoding: utf-8 -*-
from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model): #si es de hombre, mujer, niño
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'category'
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias de productos")
    
    def __unicode__(self):
        return self.name




class Products(models.Model):
    reference = models.CharField(max_length=45, blank=False, null=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    category = models.ForeignKey('Category', models.DO_NOTHING, db_column='category')
    price = models.FloatField()
    stock =  models.BooleanField()
    image = models.CharField(max_length=50)
    
    class Meta:
        managed = False
        db_table = 'products'
        verbose_name = ("Producto")
        verbose_name_plural = ("Productos")
    
    def __unicode__(self):
        return self.name