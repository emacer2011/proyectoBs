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

function popPropio2(pk){
        var campo = document.getElementById("pkProducto");
        campo.value= pk;
        var elemento=document.getElementById("modalPropio2");
        elemento.className="modal hide fade in";
        elemento.style.display="block";
        elemento.setAttribute("aria-hidden",false);
        elemento = document.createElement('div');
        elemento.setAttribute('id','nuevoPop');
        elemento.className="modal-backdrop fade in";
        document.getElementById("paraFondo").appendChild(elemento);
        cargarTabla(pk);
}

function cargarTabla(pk){
  $.get ("/cargarDepositos",{ pkProducto: pk },function(data){
        tabla = document.getElementById("tablaDetalles");
        tabla.innerHTML = data;
    }
      );
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

function volver2(){
        var elemento=document.getElementById("modalPropio2");
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


function buscar(texto,idTabla){
    var tabla, txt, filas, elemento,aComparar, aComparar2,rta, rtaTel;
    txt = texto.toUpperCase();
    tabla = document.getElementById(idTabla);
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
          aComparar2 = (elemento.cells[1].textContent).toUpperCase();
          rtaTel= aComparar2.indexOf(txt);
          if(rtaTel != -1){
            elemento.style.display='';
       }
    }

}
    
    function restaurar(idTabla){
        var tabla,filas,elemento;
            tabla = document.getElementById(idTabla);
      filas = tabla.getElementsByTagName('tr');
      for(i=0;i<=filas.length;i++){
                elemento = filas[i];
                elemento.style.display='';
      }
}