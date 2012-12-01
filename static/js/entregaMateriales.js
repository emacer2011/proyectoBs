
function cargarTabla(pk){
  $.get ("/cargarDetalles",{ pkRemito: pk },function(data){
        tabla = document.getElementById("tablaDetalles");
        tabla.innerHTML = data;
    }
      );
}


function cargarEntregados(pk){
    
    $.get ("/cargarEntregados",{ pkDetalle: pk },function(data){
    }
  );    
    
}
    

function popPropio(pk){
        var nroRemito = document.getElementById("pkRemito");
        nroRemito.value= pk;
        var elemento=document.getElementById("modalPropio");
        elemento.className="modal hide fade in";
        elemento.style.display="block";
        elemento.setAttribute("aria-hidden",false);
        elemento = document.createElement('div');
        elemento.setAttribute('id','nuevoPop');
        elemento.className="modal-backdrop fade in";
        document.getElementById("paraFondo").appendChild(elemento);
        cargarTabla(pk);
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