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
        var RegExPattern = /^\w+(\s+\w+)*$/;
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
		var tabla, txt, filas, elemento,aComparar,rta;
		txt = texto.toUpperCase();
		tabla = document.getElementById("tablaDeposito");
		filas = tabla.getElementsByTagName('tr');
		for(i=0;i<=filas.length;i++){
                    elemento = filas[i];
                    aComparar = elemento.cells[0].textContent;
                    aComparar = aComparar.toUpperCase();
                    rta = aComparar.indexOf(txt);
                    if(rta == -1){
			elemento.style.display='none';
                    }
		}
		
	}
        
        function restaurar(){
            var tabla,filas,elemento;
                tabla = document.getElementById("tablaDeposito");
		filas = tabla.getElementsByTagName('tr');
		for(i=1;i<=filas.length;i++){
                    elemento = filas[i];
                    elemento.style.display='';
		}
            
            
        }

	function validarTexto(texto){
		var letra;
		letra = texto.charAt(texto.length-1);
		if((texto>='a' && texto <='z') || (texto>='A' && texto <='Z')){
			buscar(texto);
		}else{restaurar()}
	}