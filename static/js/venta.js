function cargar(){
    var div = document.getElementById("mensajes");
    if(div.className != "")
    {
        $_POST = array(); 
        setTimeout("window.location.reload()",3000);
    }
}

function enviar() {
    var producto;
    var productos =document.getElementById("productos");
    productos.value ="";
    var tabla = document.getElementById("Comprometidos");
    var elArray = new Array();
    for (var i=0; i < tabla.rows.length; i++) {
        producto = tabla.rows[i];
        productos.value= productos.value+producto.cells[4].innerHTML+"="+producto.cells[2].innerHTML+","
    }
    productos.value = productos.value.substring(0, productos.value.length-1);    
}

function validarTabla(tabla){
    var numFilas = tabla.rows.length;
    if (numFilas == 0) {alert("Debe Elegir Productos Para Comprar");return false;};
    enviar();
    return true;    
    
}

function validarNombreApellido(campo) {
        var RegExPattern = /^\w+\w+\w+(\s\w+)*$/;
        var errorMessage = 'Nombre o Apellido invalido';
        if (campo.value.match(RegExPattern)){
            return true;
        } else {
            alert(errorMessage);
            campo.focus();
            return false;
        } 
    }
    
function validaVenta(){
		if(!validarNombreApellido(document.getElementById('nombrePersona'))){
			return false;
		}
		if(!validarNombreApellido(document.getElementById('apellidoPersona'))){
			return false;
		}
		return validarTabla(document.getElementById('Comprometidos'));
	}



function cargarDatosProducto(nombre, cantidad, precio, pk){
    var aux;
    aux = document.getElementById("nombreProducto");
    aux.value = nombre;
    aux = document.getElementById("descripcionProducto");
    aux.innerHTML = descrip;
    aux = document.getElementById("pkProducto");
    aux.value = pk;
}


function devolverProducto(fila) {
    var cantidad= parseInt(fila.cells[2].innerHTML);
    var celda = document.getElementById(fila.cells[4].innerHTML);
    var cantidadDevuelta = prompt('Cantidad a Devolver:',cantidad);
    cantidadDevuelta = parseInt(cantidadDevuelta);
    if((isNaN(cantidadDevuelta)) || (cantidadDevuelta < 1) || (cantidadDevuelta > cantidad)){
        alert('No se Devuelven Productos');
        return false;}
    celda.innerHTML = parseInt(cantidadDevuelta) + parseInt(celda.innerHTML);
    fila.cells[2].innerHTML = parseInt(fila.cells[2].innerHTML) - parseInt(cantidadDevuelta);
    fila.cells[5].innerHTML = parseInt(fila.cells[3].innerHTML) *parseInt(fila.cells[2].innerHTML);
    if(parseInt(fila.cells[2].innerHTML) == 0){ 
        fila.parentNode.deleteRow(fila.rowIndex);
    }
}

 

function agregarProducto(fila) {

    if(fila.cells[5].innerHTML== "Fraccionable"){
        agregarProductoFraccionable(fila);
    }else{
        agregarProductoNoFraccionable(fila);
    }
}

function buscarCompraExistente(pk,medida){
    var tabla = document.getElementById("Comprometidos");
    var elementos = tabla.getElementsByTagName('tr');
    var medidaFinal = parseInt(medida);
    for (var i = elementos.length - 1; i >= 0; i--) {
        if(elementos[i].cells[4].innerHTML == pk){
            if(parseInt(elementos[i].cells[6].innerHTML) == medidaFinal){
            return elementos[i];
            }
        }
    }
    return null;
}

function agregarProductoFraccionable(fila){
    var cantidad = 1;
    var medida = fila.cells[6].innerHTML;
    var medidaMinima = fila.cells[7].innerHTML;
    var cantidadComprada = prompt('Medida:'+medida+'\t Medida Minima:'+ medidaMinima+'\nMedida Deseada:',cantidad);
    if(verificarMedida(medidaMinima, medida, cantidadComprada)){
        var cantidad = parseInt(fila.cells[2].innerHTML);
        var pk = fila.cells[4].innerHTML;
        var tabla = document.getElementById("Comprometidos");
        var unidades = prompt('Cantidad:',cantidad);
        cantidadComprada = parseInt(cantidadComprada);
        if((isNaN(cantidadComprada)) || (cantidadComprada > cantidad) || (cantidadComprada<1)){return false;}
        var existente = buscarCompraExistente(pk, cantidadComprada);
        if(existente == null){
            var indice = tabla.rows.length;
            var nuevaFila = tabla.insertRow(indice);
            var celda = nuevaFila.insertCell(0);
            celda.innerHTML = fila.cells[0].innerHTML;
            celda = nuevaFila.insertCell(1);
            celda.innerHTML = fila.cells[1].innerHTML;
            celda = nuevaFila.insertCell(2);
            celda.innerHTML = unidades;
            fila.cells[2].innerHTML = cantidad-unidades;
            celda = nuevaFila.insertCell(3);
            celda.innerHTML = fila.cells[3].innerHTML;
            celda = nuevaFila.insertCell(4);
            celda.innerHTML = pk;
            celda.style.display="none";
            celda = nuevaFila.insertCell(5);
            celda.innerHTML = (cantidadComprada * parseInt(fila.cells[3].innerHTML))*unidades;
            nuevaFila.id=-parseInt(pk);
            nuevaFila.onclick = function(){devolverProducto(nuevaFila)};
            celda = nuevaFila.insertCell(6);
            celda.innerHTML = cantidadComprada;
        }else{
            existente.cells[2].innerHTML = parseInt(existente.cells[2].innerHTML) + parseInt(unidades);
            existente.cells[5].innerHTML = (parseInt(existente.cells[2].innerHTML) * parseInt(existente.cells[3].innerHTML) * parseInt(existente.cells[6].innerHTML));
            fila.cells[2].innerHTML = cantidad-parseInt(unidades);
         }

    }

}

function verificarMedida(medidaMinima, medidaMaxima, medidaSolicitada){
    var resto = medidaMaxima - medidaSolicitada;
    if(medidaSolicitada < medidaMinima || resto < medidaMinima || medidaSolicitada > medidaMaxima){
        return true;
    }
    alert('Imposible Vender la cantidad Solicitada (Violacion de Medidas Minimas/Maximas)');
    return false;
}

 function agregarProductoNoFraccionable(fila) {
    var cantidad = parseInt(fila.cells[2].innerHTML);
    var pk =fila.cells[4].innerHTML;
    var tabla = document.getElementById("Comprometidos");
    var cantidadComprada = prompt('Cantidad:',cantidad);
    cantidadComprada = parseInt(cantidadComprada);
    if((isNaN(cantidadComprada)) || (cantidadComprada > cantidad) || (cantidadComprada<1)){return false;}
    var existente = document.getElementById(-parseInt(pk));
    if(existente == null){
        var indice = tabla.rows.length;
        var nuevaFila = tabla.insertRow(indice);
        var celda = nuevaFila.insertCell(0);
        celda.innerHTML = fila.cells[0].innerHTML;
        celda = nuevaFila.insertCell(1);
        celda.innerHTML = fila.cells[1].innerHTML;
        celda = nuevaFila.insertCell(2);
        celda.innerHTML = cantidadComprada;
        fila.cells[2].innerHTML = cantidad-cantidadComprada;
        celda = nuevaFila.insertCell(3);
        celda.innerHTML = fila.cells[3].innerHTML;
        celda = nuevaFila.insertCell(4);
        celda.innerHTML = pk;
        celda.style.display="none";
        celda = nuevaFila.insertCell(5);
        celda.innerHTML = (cantidadComprada * parseInt(fila.cells[3].innerHTML));
        nuevaFila.id=-parseInt(pk);
        nuevaFila.onclick = function(){devolverProducto(nuevaFila)};
    }else{
        existente.cells[2].innerHTML = parseInt(existente.cells[2].innerHTML) + cantidadComprada;
        existente.cells[5].innerHTML = (parseInt(existente.cells[2].innerHTML) * parseInt(existente.cells[3].innerHTML));
        fila.cells[2].innerHTML = cantidad-cantidadComprada;
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