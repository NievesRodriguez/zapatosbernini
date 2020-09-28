# -*- encoding: utf-8 -*-
from .models import *
from pedidos.models import *
import hashlib
###############
from django.shortcuts import render

from django.http import HttpResponseRedirect,HttpResponse


"""
    Muestra la página de login

"""
def index(request):
    
    return render(request,'index.html')



#@csrf_exempt
def login(request): 
    if request.POST:
        email = request.POST['email'].lower()
        if request.POST['password'] is not None:
            hashlib.sha256("a".encode('utf-8')).hexdigest()
            password =  hashlib.sha256((request.POST['password']).encode('utf-8')).hexdigest()
            
        else: 
            password = None
        
        try:
            if email is not None and password is not None:
                try:
                    cliente = Customer.objects.get(email=email, password=password)
                    request.session.set_expiry(240000)
                    request.session['is_auth'] = 1
                    request.session['user_id'] = cliente.pk
                    
                except Customer.DoesNotExist:
                    userExists = False
                    return render(request,'index.html',{'userExists':userExists})
    
                
                if Customer is not None:
                    # Redirect to a success page.
                    return HttpResponseRedirect("/verproductos") 
                else:
                    # Show an error page
                    return HttpResponseRedirect("/")       
            else:
                return HttpResponseRedirect('/')
        except Customer.DoesNotExist: #si usuario no existe
            return render(request,'index.html')


"""
    Muestra todos los productos
"""

def verproductos(request):
    if "is_auth" not in request.session and "user_id" not in request.session:
        return render(request,'index.html',None)
    else:
        productos = Products.objects.all()
        
        return render(request,'productos/ver-productos.html',{'productos':productos})


