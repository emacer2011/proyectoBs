
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
 
 
function actualizarEntregados(){
    debugger;
    var pk = document.getElementById("pkRemito").value;
    $.get ("/actualizarEntregados",{ pkRemito: pk },function(data){
        window.location.reload();
    }
  );    
    
}   

function cerrar(){
    var check,filaActual;
    var tabla = document.getElementById("tablaDetalles");
    var filas = tabla.rows;
            debugger;
    for(i=1; i < filas.length; i++){
        filaActual = filas[i];
        check = filaActual.cells[3].children[0];
        if((check.checked) && !(check.hasAttribute("disabled"))){
            cargarEntregados(filaActual.cells[0].innerHTML);
        }
    }
        
    
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
        cerrar();
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