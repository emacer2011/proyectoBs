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

function mostrarDescripcion(descripcion){
  $(descripcion).tooltip('show');
}


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


     function imprimirPDF(){
      var filtro = document.getElementById("filtro").value;
      var selector = document.getElementById("depoPk");
      selector = selector.innerHTML;
      ventana = window.open("/listarProductoPDF/?filtro="+filtro+"&deposito="+selector, this.target, 'width=600,hei ght=400,top=100px,left=100px');
      location.href=location.href;
      
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
     
        var errorMessage = 'Descripcion invalida';
        if (campo.value.length <= 20){
            return true;
        } else {
            alert(errorMessage);
            campo.focus();
            return false;
        } 
    }

    
   function valoresConComa(medida){
    var coma = ',';
    var punto = '.';
    var cadena = "";
    for (var i = 0; i < medida.length; i++) {
        
        if (medida[i] == coma){
            cadena = cadena+punto;
        }else{
            cadena= cadena+medida[i];
        }
    }
    return cadena;
}


    function validarPrecio(campo){
        var valor = campo.value;
        //var patron = /\d+(\.\d{1,2})?$/;
        var patron = /^[0-9]+(\.[0-9]+)?$/;
        valor = valoresConComa(valor);
        if (valor.match(patron) && valor != ""){
          return true;
        }   
        alert("Error en el Precio");
        return false;
    }


function validarPrecioResguardo(campo){
        var valor = campo.value;
        valor = valoresConComa(valor);
        campo.value= valor;
        var entero = parseFloat(valor);
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

      if ((document.getElementById("fraccionable").checked)){
        if (!validarDatosFraccionables()) {
          return false;
        };
      };
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


function mostrarDatosFraccionable(){
  var datos = document.getElementById("datosFraccionable");
  var check = document.getElementById("fraccionable");
  if (check.checked){
    datos.style.display = '';
  }else{
    datos.style.display = "none";
  }
}

function validarDatosFraccionables(){
  var patron = /\d+|(\d+.\d\d)/;
  var medidaMinima = valoresConComa(document.getElementById("medidaMinimaProducto").value);
  document.getElementById("medidaMinimaProducto").value = medidaMinima;
  var medida = valoresConComa(parseFloat(document.getElementById("medidaProducto").value));
  parseFloat(document.getElementById("medidaProducto").value) = medida;
  if (patron.match(medidaMinima) && patron.match(medida)){
      medidaMinima = parseFloat(medidaMinima.value);
      medida = parseFloat(medida);
      if (medidaMinima != "" && (medidaMinima>0 && medida > 0)){
          return true;
      }   
  }
  alert("Error en Medidas (no pueden ser nulas ni menores a '0')");
  return false; 
}


function ayudaAltaPDF(){
      ventana = window.open("/ayudaAltaProducto", this.target, 'width=600,hei ght=400,top=100px,left=100px');
      location.href=location.href;
}

function ayudaBajaPDF(){
      ventana = window.open("/ayudaBajaProducto", this.target, 'width=600,hei ght=400,top=100px,left=100px');
      location.href=location.href;
}

function ayudaModificarPDF(){
      ventana = window.open("/ayudaModificarProducto", this.target, 'width=600,hei ght=400,top=100px,left=100px');
      location.href=location.href;
}

function ayudaListarPDF(){
      ventana = window.open("/ayudaListarProducto", this.target, 'width=600,hei ght=400,top=100px,left=100px');
      location.href=location.href;
}



function listarConDepo(valor){
  var filtro = document.getElementById("filtro").value;
  location.href = "/listarProducto/?filtro="+filtro+"&deposito="+valor;
}

function ValorSelect(valor){
  document.getElementById("depositoMostrado").innerHTML = valor;
}

function descargarEstadisticas(){
  location.href="/estadistico";

}