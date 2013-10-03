var Deposito;
var Producto;

function verificarCarga(){
  var mensaje = document.getElementById("mensaje").innerHTML;
  if(mensaje != ""){
    setTimeout("location.href=location.href",2000);
  }
}

function popPropio(pk){
        var depositos = document.getElementById("deposito").options;
        if (depositos.length == 0) {alert("No hay depositos cargados");return false;};
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
        var campo = document.getElementById("pkProductoDescuento");
        campo.value= pk;
        var elemento=document.getElementById("modalPropio2");
        elemento.className="modalDescuento hide fade in";
        elemento.style.display="block";
        elemento.setAttribute("aria-hidden",false);
        elemento = document.createElement('div');
        elemento.setAttribute('id','nuevoPop');
        elemento.className="modal-backdrop fade in";
        document.getElementById("paraFondo").appendChild(elemento);
        cargarTabla(pk);
}


function validarNumeros(pk,e){
  cantidad = document.getElementById('d'+String(pk)).value;
  var filtro = /([A-z])+/;
  if(filtro.test(cantidad)){
    alert("Error al cargar datos: verifique que el valor sea correcto");
    cantidad.focus();
  }
}


function verificarDescuento(pk,e){
  cantidad = document.getElementById('d'+String(pk)).value;
  elemento = document.getElementById('s'+String(pk));
    validarNumeros(pk,e);
    if(parseInt(cantidad) > 0 && parseInt(elemento.cells[2].innerHTML) >= parseInt(cantidad)){
      return alert("Descontando Stock!!!!");
    }
}


function cargarTabla(pk){
  $.get ("/cargarDepositos",{ pkProducto: pk },function(data){
        tabla = document.getElementById("tablaDetalles");
        tabla.innerHTML = data;
    }
      );
}


function mostrarDetalles(fila){
  Deposito = fila.cells[0].innerHTML;
  Producto = fila.id;
  limpiarCamposDescuento()
  document.getElementById("depositoSeleccionado").innerHTML= "Deposito seleccionado: "+fila.cells[1].innerHTML;
  div = document.getElementById("divDescripcionDescuento");
  if(div.style.display == "none"){
    div.style.display="block";
    deposito = document.getElementById("pkDeposito");
    deposito.value = Deposito;
  }else{
    div.style.display = "none";
  }
  ocultarBeneficiario()
}

function limpiarCamposDescuento(){
  cantidad = document.getElementById("cantidadDescuento").value = "";
  beneficiario = document.getElementById("beneficiarioDescuento").value= "";
  document.getElementById("descripcionDescuento").value= "";
  document.getElementById("pkDeposito").value = "";
  document.getElementById("depositoSeleccionado").innerHTML= "";
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
        var div = document.getElementById("divDescripcionDescuento");
        div.style.display ="none";
        limpiarCamposDescuento()

        var elemento=document.getElementById("modalPropio2");
        elemento.className="modal hide fade";
        elemento.style.display="none";
        elemento.setAttribute("aria-hidden",true);
        elemento = document.getElementById("paraFondo");
        var remover = document.getElementById("nuevoPop");
        elemento.removeChild(remover);
}

function validarDisponibles(valor){ 
    var patron = /^[0-9]+$/;
    	if (!valor.match(patron)) {
     	     alert("El valor del Campo Disponibles debe ser numeros mayores a 0") 
           	 return false
     	}else{ 
            valor = parseInt(valor)
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


function validarCantidadDescuento(){
  var patron = /^[0-9]+$/;
  cantidad = document.getElementById("cantidadDescuento").value;
  pkDeposito = document.getElementById("pkDeposito").value;
  cantidadTotal = document.getElementById("d"+pkDeposito);
  cantidad = valores
  if (cantidad.match(patron) && cantidadTotal.match(patron)){
    cantidadTotal = parseInt(cantidadTotal.innerHTML);
    cantidad = parseInt(cantidad);
    if(cantidad > 0 & cantidad <= cantidadTotal){
      document.getElementById("cantidadDescuento").value = cantidad
      return true;
    }
  }
  alert("Cantidad a descontar incorrecta");
  return false;

}

function ocultarBeneficiario(){
  motivoObj=document.getElementById("motivoDescuento");
  motivo = motivoObj.value;
  beneficiario = document.getElementById("beneficiarioDescuento");
  if (motivo == "Donacion") {
    beneficiario.disabled = false;
  }  
  else{
    beneficiario.disabled = true;
  }
}

function validarBeneficiario(){

  motivo = document.getElementById("motivoDescuento").value;
  if (motivo == "Donacion") {
    beneficiario = document.getElementById("beneficiarioDescuento").value;
    if (beneficiario=="") {
        alert("Si el motivo es 'Donacion' el beneficiario no puede ser vacio");
        return false;
    }
  }
  return true;

}

function verificarEnvio(){
  div = document.getElementById("divDescripcionDescuento");
  if(div.style.display == "none"){
    volver2();
    return false;
  }
  if (!validarCantidadDescuento()) {
      return false;

  };
  if (!validarBeneficiario()) {
      return false;
  };
  return true;

}

function ayudaPDF(){
      ventana = window.open("/ayudaManejoStock", this.target, 'width=600,hei ght=400,top=100px,left=100px');
      location.href=location.href;
}