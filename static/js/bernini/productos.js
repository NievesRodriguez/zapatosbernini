$(document).ready(function() {

	
	/*Formatea puntos precio articulos*/
	
	$('.price').each(function() {
		var precio = $(this).html().replace('.',',');
		$(this).html(precio);
	});
	
	
	/* CARRITO */
	
	var itemsCarrito = [];
	var total = 0;
	var carrito = $('#carrito');
	var total = $('#total');
	var items = [];
	
	
	$('.additem').on('click', function(){
		var item = $(this);
		addItemCarrito(item);
	});
	
	
	function addItemCarrito(item){
		idItem = ($(item).data('id'));
		
		itemsCarrito.push(idItem);
		
	    // actualizamos el carrito 
	    actualizaCarrito(item);
	    // Calculo el total
	    calcularTotal();
	};
	
	
	
	function calcularTotal () {
	    total = 0;
	    
	    for (item of itemsCarrito) {
	        var price = $('#' + item).find('.additem').data('price');
	        total = total + price;
	        $('#total').html(total);
	        
	    }
	    
	}
	
	function actualizaCarrito(item){
		
	    // Creamos el nodo del item del carrito
		idItem = $(item).data('id');
		
		var eleme= carrito.find("#item" + idItem);
		
		if (eleme.length == 0){
			
			nameItem = $(item).data('name');
		    priceItem = $(item).data('price');
		    
		    var nuevoItem = $('<li class="productos" data-id="' + idItem + '" data-number="1" id="item' + idItem + '"></li>');
		    nuevoItem.addClass('list-group-item mx-2');
		    
		    nuevoItem.append("<span class='cantidad'>1</span> - ");
		    nuevoItem.append("<span>" + nameItem + " - " + "</span>");
		    nuevoItem.append("<span class='precio'>" + priceItem + "</span> €");
		    
		    // Boton de borrar
		    var botonBorrar = $('<input type="button" id="boton" value="X" style="margin-left: 20px;"/>');
		    botonBorrar.addClass('btn btn-danger');
		    
		    
		    botonBorrar.on('click', borrarItemCarrito);
		    
		    nuevoItem.append(botonBorrar);
		    
		    carrito.append(nuevoItem);
		    
		    items.push(idItem);
		   
		}else{
			
			cantidad = eleme.data('number');
			eleme.data('number', cantidad + 1);
			eleme.find('.cantidad').html(cantidad + 1);
			
			precio = parseFloat(eleme.find('.precio').html());
			priceItem = parseFloat(priceItem);
			eleme.find('.precio').html(precio + priceItem);
			
		}
		
	};
	
	function borrarItemCarrito () {
	    $(this).parent().remove();
	    
	}
	
	
	/* ENVIO DEL PEDIDO UNA VEZ TERMINADO*/
	
	$('.sendOrder').on('click', function(){
		
		productos = []
		
		for (item of items) {
			console.log(item);
			console.log($('#' + item).data('number'));
			producto = {'id': item,'cantidad': $('#item' + item).data('number')};
			console.log(producto);
			productos.push(producto);
		}
		
		swal({
            title: "¿Está seguro?",
            text: "Esta acción enviará el pedido",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#dd3333",
            confirmButtonText: "Sí, Enviar",
            closeOnConfirm: false
        }, function () {
        	
        	$.ajax({
   	   		 url: '/pedidos/enviarpedido',
   	   		 type: 'POST',
   	   		 contentType: 'application/json',
   	         processData: false,
   	         dataType: 'json',
   	         data: JSON.stringify({'productos':productos}),
   	   		
   	   		 success: function(response) {
   	   			 if (response['status'] == "success"){
	   	   			swal({
			            title: "Gracias!",
			            text: "Su pedido se envió correctamente",
			            type: "success",
			            confirmButtonColor: "#dd3333",
			            confirmButtonText: "OK"
			        }, function () {
			        	
			        }); 
   	   			 }
	   	   			
   	   			 else{
	   	   			swal({
			            title: "Aviso",
			            text: "El pedido no se envió correctamente",
			            confirmButtonColor: "#dd3333",
			            confirmButtonText: "OK"
			        }, function () {
			        	
			        }); 
   	   			 }
   	   			 
   	   			
   	   		 },
   	   		 error: function(response) {
   	   			 console.log('Error');
   		    	
   	   			 
   	   		 },
   	   	  });
        	
            
        });
		
		
	});
	


});