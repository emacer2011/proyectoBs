    function bajaProducto(pk){
           $.get ("/bajaProducto",{ pkProducto: pk },function(estado){
               var div = document.getElementById("mensajes")
               var mensajes = estado.split("/") ;
               div.className = mensajes[0];
               div.innerHTML = mensajes[1];
               setTimeout("window.location.reload()",3000);
    }
  );    
 }


    function validarNombre(campo) {
        var RegExPattern = /^\w{3,30}$/;
        var errorMessage = 'Nombre de producto invalido';
        if (campo.value.match(RegExPattern)){
            return true;
        }
        else {
            alert(errorMessage);
            campo.focus();
            return false;
        } 
    }
    
    function validarDescripcion(campo) {
        var RegExPattern = /^\w*$/;
        var errorMessage = 'Descripcion invalida';
        if (campo.value.match(RegExPattern)){
            return true;
        } else {
            alert(errorMessage);
            campo.focus();
            return false;
        } 
    }

    function validarPrecio(campo){
        var valor = campo.value;
        var entero = parseInt(valor)
        if (entero != "" && !isNaN(entero)){
                if (entero>0){
                    return true;
            }
        }   
        alert("Error en el Precio");
        return false; 
    }

    function validaProducto(producto)
		{
			if(!validarNombre(document.getElementById('nombreProducto'))){
				return false;
			}	
               
               if(!validarPrecio(document.getElementById('precioProducto'))){
				return false;
			}	
                 
			return validarDescripcion(document.getElementById('descripcionProducto'));
		}
    
    

function popPropio(pk,nombre,descripcion,tipo,precio){
        var pkProd, nombreProd,descripcionProd,tipoProd,precioProd;
        pkProd = document.getElementById("pkProducto");
        pkProd.value = pk;
        nombreProd = document.getElementById("nombreProducto");
        nombreProd.value = nombre;
        descripcionProd = document.getElementById("descripcionProducto");
        descripcionProd.value = descripcion;
        precioProd = document.getElementById("precioProducto");
        precioProd.value = precio;
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