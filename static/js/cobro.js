function popPropio(pk, precio){
        var nroNota = document.getElementById("nroNota");
        var precioNota = document.getElementById("precioNota");
        nroNota.value= pk;
        precioNota.value = precio;
        var elemento=document.getElementById("modalPropio");
        elemento.className="modal hide fade in";
        elemento.style.display="block";
        elemento.setAttribute("aria-hidden",false);
        elemento = document.createElement('div');
        elemento.setAttribute('id','nuevoPop');
        elemento.className="modal-backdrop fade in";
        document.getElementById("paraFondo").appendChild(elemento);
}


function generarFactura(){
    var precio = document.getElementById("precioNota").value;
    var nroNota = document.getElementById("nroNota").value;
    var formaPago = document.getElementById("formaPago").value;

    $.get ("/cobro",{ precioNota: precio, nroNota: nroNota, formaPago: formaPago },function(estado){
         ventana = window.open("/generarFactura/?nroNota="+nroNota, this.target, 'width=600,hei ght=400,top=100px,left=100px');
         window.location.reload();
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

function ayudaPDF(){
      ventana = window.open("/ayudaCobro", this.target, 'width=600,hei ght=400,top=100px,left=100px');
      location.href=location.href;
}