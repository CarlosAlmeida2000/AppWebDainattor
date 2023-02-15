show_spinner()

var f = new Date();
añoActual = f.getFullYear()
mesActual = (f.getMonth() + 1)
diaActual = f.getDate()
if (mesActual < 10) {
    mesActual = "0" + mesActual
}
if (diaActual < 10) {
    diaActual = "0" + diaActual
}
dtmFechaInicio = (añoActual + "-" + mesActual + "-" + diaActual)
if($("#dtmFechaHistorial").val().length == 0){
    document.querySelector("#dtmFechaHistorial").setAttribute("value", dtmFechaInicio);
}

function verFotoHistorial(rutaFoto, expresionFacial){
    document.querySelector("#fotoHistorial").setAttribute("src", rutaFoto);
    $('#exampleModalLabel').text('La expresión facial reconocida es: ' + expresionFacial)
    var myModal = new bootstrap.Modal(document.getElementById('verFotoHistorial'), {
        keyboard: false
      })
      myModal.toggle()
}

hide_spinner()