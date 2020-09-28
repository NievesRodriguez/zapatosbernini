# -*- encoding: utf-8 -*-
from catalogo.models import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,date
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.mail.backends.smtp import EmailBackend

from .utilidades.Utils import *
from .utilidades.Excel import *

util = Utils()
excel = Excel()

now = datetime.now()

"""
    Envia el pedido del cliente por correo electronico
"""

@csrf_exempt 
def enviarpedido(request):
    if "is_auth" not in request.session and "user_id" not in request.session:
        return render(request,'index.html',None)
    else:
        customer = Customer.objects.get(pk=request.session['user_id'])
        
        response={'status':'success'}
        if request.is_ajax():
            jsondata=json.loads(request.body)
            
            productos = jsondata['productos']
            
            for prod in productos:
                producto = Products.objects.get(pk = prod['id'])
                prod['total'] = producto.price * prod['cantidad']
                prod['name'] = producto.name
                prod['price'] = producto.price
                
                
                
            numeroOrden = util.generarOrder(customer)
            newPedido = Orders(number= numeroOrden, customer = customer, send= 0, date = now)  
            newPedido.save()
            
            nombreFichero = excel.generaExcelPedido(productos, customer, newPedido)
            
            ficheroExcel = 'media/pedidos/' + str(customer.pk) + '/' + numeroOrden + "/" + nombreFichero
            
            conexionSMTP = EmailBackend(host='smtp.bernini.es', port='587', username='admin@bernini.es', 
                       password='passInfo', use_tls='True')
            
            try:
                emails = {'from_email' : 'admin@bernini.es'}
                contenidoEmail = {'titulo' : customer.name + ' ' + customer.lastname + ' - Resumen de pedido'}
                contenidoEmail['productos'] = productos
                util.enviarEmailAdjuntos(customer, 'envio-pedido.html', conexionSMTP, emails, ficheroExcel, contenidoEmail)
                
                newPedido.send = 1
                newPedido.save()
                
                response={'status':'success'}
            except Exception as e:
                print(e)
                
                response={'status':'error'}
            
        
        return HttpResponse(json.dumps(response), content_type="application/json")
    

    
