# -*- encoding: utf-8 -*-

from django.core.mail import EmailMultiAlternatives
from datetime import datetime,date
from django.template import Context
from django.template.loader import render_to_string


class Utils(object):
    """
            Genera numero de orden 
            Parametros:
                customer: objeto tipo Customer de BD
            Return: String
        """
    def generarOrder(self,customer):
        clave = customer.pk
        fecha = datetime.now()
        mes = fecha.month
        if int(mes) < 10:
            mes = '0' + str(mes)
                
        anio = str(fecha.year)
        tamano = len(anio)
        cifra = anio[tamano-2] + anio[tamano-1] 
            
        fecha = str(mes) + cifra
        cadena = str(clave) + fecha
            
        return cadena
    
    
    """
        Envia emails que usan plantillas html con ficheros adjuntos
        
    """   
    def enviarEmailAdjuntos(self, customer, template, conexionSMTP, emails, fichero, contenidoEmail):
        
        titulo = contenidoEmail['titulo']
        
        contenido = render_to_string('mail/' + template,{'cliente':customer,'productos':contenidoEmail['productos']})
        
            
        correo = EmailMultiAlternatives(titulo, contenido, emails['from_email'], ['pedidos@bernini.es'], 
                    connection = conexionSMTP)
        
        try:
            correo.attach_alternative(contenido, "text/html")
            correo.attach_file(fichero)
                
               
            correo.send()
        except:
            print("error en envio")
            