    
    function bajaDeposito(pk){
           $.get ("/bajaDeposito",{ pkDeposito: pk },function(estado){
               var div = document.getElementById("mensajes")
               var mensajes = estado.split("/") ;
               div.className = mensajes[0];
               div.innerHTML = mensajes[1];
               setTimeout("window.location.reload()",3000);
    }
  );    
 
        
        
    }
    
    function validarTelefono(campo) {
        var RegExPattern = /^[0-9]{7,13}$/;
        var errorMessage = 'Telefono Invalido 7 a 13 digitos';
        if (campo.value.match(RegExPattern)){
            return true;
        } else {
            alert(errorMessage);
            campo.focus();
            return false;
        } 
    }
    function validarDireccion(campo) {
        var RegExPattern = /^\w+(\s\w+)*$/;
        var errorMessage = 'Direccion invalida o vacia';
        if (campo.value.match(RegExPattern)){
            return true;
        } else {
            alert(errorMessage);
            campo.focus();
            return false;
        } 
    }
    
	function validaDeposito(deposito)
		{
			if(!validarDireccion(document.getElementById('direccionDeposito'))){
				return false;
			}
			return validarTelefono(document.getElementById('telefonoDeposito'));
		}


  	function buscar(texto){
		var tabla, txt, filas, elemento,aComparar, aComparar2,rta, rtaTel;
		txt = texto.toUpperCase();
		tabla = document.getElementById("tablaDeposito");
		filas = tabla.getElementsByTagName('tr');
		for(i=0;i<=filas.length;i++){
		    elemento = filas[i];
		    elemento.style.display='none';
		    aComparar = elemento.cells[0].textContent;
		    aComparar = aComparar.toUpperCase();
		    rta = aComparar.indexOf(txt);
		    if(rta != -1){
                elemento.style.display='';
            }
		    aComparar2 = elemento.cells[1].textContent;
		    aComparar2 = aComparar2.toUpperCase();
		    rtaTel= aComparar2.indexOf(txt);
		    if(rtaTel != -1){
		          elemento.style.display='';
		     }
		}
		
	}
        
        function restaurar(){
            var tabla,filas,elemento;
                tabla = document.getElementById("tablaDeposito");
		        filas = tabla.getElementsByTagName('tr');
		        for(i=0;i<=filas.length;i++){
                    elemento = filas[i];
                    elemento.style.display='';
		        }
        }

	function validarTexto(texto){
		buscar(texto);
	}
	
	function popupPropio(){    
	    $('#modalPropio').modal('show')
	    
	   }