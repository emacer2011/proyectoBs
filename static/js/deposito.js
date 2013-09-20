    
    function verificarCarga(){
        var div = document.getElementById("mensaje")
        var mensaje=div.innerHTML;
        if(mensaje != ""){
          setTimeout("location.href=location.href",2000);
  }
}

  function limpiarCampo(){
        var filtro = document.getElementById("filtro").innerHTML = "";
  }

    function bajaDeposito(pk){
           $.get ("/bajaDeposito",{ pkDeposito: pk },function(estado){
               var div = document.getElementById("mensajes")
               var mensajes = estado.split("/") ;
               div.className = mensajes[0];
               div.innerHTML = mensajes[1];
               setTimeout("window.location.reload()",1500);
    }
  );    
    }

    
    function imprimirPDF(){
      var filtro = document.getElementById("filtro").value;
      ventana = window.open("/listarDepositoPDF/?filtro="+filtro, this.target, 'width=600,hei ght=400,top=100px,left=100px');
      location.href=location.href;
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
	
	function popPropio(pk,direccion,rubro,telefono){
        var pkDeposito = document.getElementById("pkDeposito");
        pkDeposito.value = pk;
        var direccionDeposito = document.getElementById("direccionDeposito");
        direccionDeposito.value= direccion;
        var telDeposito = document.getElementById("telefonoDeposito");
        telDeposito.value= telefono;
        var rubroDeposito = document.getElementById("rubroDeposito");
        rubroDeposito.value= rubro;
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
          aComparar2 = (elemento.cells[2].textContent).toUpperCase();
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


function ayudaAltaPDF(){
      ventana = window.open("/ayudaAltaDeposito", this.target, 'width=600,hei ght=400,top=100px,left=100px');
      location.href=location.href;
}

function ayudaBajaPDF(){
      ventana = window.open("/ayudaBajaDeposito", this.target, 'width=600,hei ght=400,top=100px,left=100px');
      location.href=location.href;
}

function ayudaModificarPDF(){
      ventana = window.open("/ayudaModificarDeposito", this.target, 'width=600,hei ght=400,top=100px,left=100px');
      location.href=location.href;
}

function ayudaListarPDF(){
      ventana = window.open("/ayudaListarDepositos", this.target, 'width=600,hei ght=400,top=100px,left=100px');
      location.href=location.href;
}