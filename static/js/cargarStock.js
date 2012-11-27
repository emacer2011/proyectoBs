function popPropio(pk){
        var campo = document.getElementById("pkProducto");
        campo.value= pk;
        var elemento=document.getElementById("modalPropio");
        elemento.className="modal hide fade in";
        elemento.style.display="block";
        elemento.setAttribute("aria-hidden",false);
        elemento = document.createElement('div');
        elemento.setAttribute('id','nuevoPop');
        elemento.className="modal-backdrop fade in";
        document.getElementById("paraFondo").appendChild(elemento);
}
    
function volver(){
        var elemento=document.getElementById("modalPropio");
        elemento.className="modal hide fade";
        elemento.style.display="none";
        elemento.setAttribute("aria-hidden",true);
        elemento = document.getElementById("paraFondo");
        var remover = document.getElementById("nuevoPop");
        elemento.removeChild(remover);
}

function validarDisponibles(valor){ 
     valor = parseInt(valor)  
     	if (isNaN(valor)) {
     	     alert("El valor del Campo Disponibles debe ser numeros mayores a 0") 
           	 return false
     	}else{ 
           	 if (valor>0){
           	    return true
           	 }
            alert("El valor del Campo Disponibles debe ser numeros mayores a 0") 
            return false
     	} 
}


