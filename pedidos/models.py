from django.db import models
from django.utils import timezone

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    
    class Meta:
        managed = False
        db_table = 'customer'
        verbose_name = ("Cliente")
        verbose_name_plural = ("Clientes")
        
    def __unicode__(self):
        return self.name
    

class Orders(models.Model):
    number = models.IntegerField(blank=False, null=False)
    customer = models.ForeignKey('Customer', models.DO_NOTHING, db_column='customer')
    send = models.BooleanField()
    date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        managed = False
        db_table = 'orders'
        verbose_name = ("Pedido")
        verbose_name_plural = ("Pedidos")
        
    def __unicode__(self):
        return self.number