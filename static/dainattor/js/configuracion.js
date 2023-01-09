const switchEntrenamiento = document.getElementById("switchEntrenamiento")
const switchMonitoreo = document.getElementById("switchMonitoreo")
const video = document.getElementById('video')
var canvas = document.getElementById('canvas')
var context = canvas.getContext('2d')
var cont_imagenes = 0
var caputarar_imagenes = 100

// iniciar cámara web
function iniciarVideo(accion) {
    navigator.mediaDevices.getUserMedia({
        video: true
        })
        .then(stream => {
        window.localStream = stream;
        video.srcObject = stream;
        if (accion == 'entrenamiento'){
            iniciarEntrenamiento()
        }else{
            inicioCronometro()
        }
        })
        .catch((err) => {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Sucedió un error en obtener iniciar el video, intentalo de nuevo'
        });
        });
}

// detener cámara web
function detenerVideo(){
    localStream.getVideoTracks()[0].stop()
    video.srcObject = null
}

switchEntrenamiento.addEventListener('change', function(){
    if(switchEntrenamiento.checked){
        switchEntrenamiento.disabled = true
        iniciarVideo('entrenamiento')
    }else{
        detenerVideo()
    }
});

switchMonitoreo.addEventListener('change', function(){
    if(switchMonitoreo.checked){
        iniciarVideo('monitoreo')
    }else{
        detenerVideo()
        reiniciarCronometro()
    }
});

function iniciarEntrenamiento(){
    var csrftoken = getCookie('csrftoken')
    context.drawImage(video, 0, 0, 640, 480)
    const data = canvas.toDataURL()
    $.ajax({
        url: '/capturar-rostro-entrenamiento/',
        type: 'POST',
        data: {csrfmiddlewaretoken: csrftoken, 'imagen': data, 'cont_imagenes': cont_imagenes},
        dataType: "json"
    }).done(function (data) {
        switch (data.result) {
            case '1':
                if(data.tiene_rostro == '1'){
                    $("#estado-entrenamiento").text('Fotos capturadas: ' + (cont_imagenes + 1))
                    $("#estado-entrenamiento").css("color", "#000000")
                    cont_imagenes += 1
                }else{
                    $("#estado-entrenamiento").text('Fotos capturadas: No existe un rostro en la imagen')
                    $("#estado-entrenamiento").css("color", "#ff0000")
                }
            break;
            case '0':
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Sucedió un error durante el entrenamiento facial, intentalo de nuevo'
                });
            break;
        }
        if(cont_imagenes < caputarar_imagenes){
            iniciarEntrenamiento()
        }else{
            switchEntrenamiento.checked = false
            cont_imagenes = 0
            detenerVideo()
            switchEntrenamiento.disabled = false
            Swal.fire({
                icon: 'success',
                title: '¡Excelente!',
                text: 'Entrenamiento facial culminado exitosamente.'
                });
            return 0
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Sucedió un error durante el entrenamiento facial, intentalo de nuevo'
        });
        switchEntrenamiento.disabled = false
    }).always(function (data) {
    });
}


// Cronómetro para analizar expresiones faciales
var centesimas = 0
var segundos = 0
var minutos = 0

function inicioCronometro () {
	control = setInterval(cronometro, 10);
}

function reiniciarCronometro () {
	clearInterval(control)
	centesimas = 0
	segundos = 0
	minutos = 0
	tiempo.innerHTML = "Reloj: "+ minutos +":"+ segundos +":"+ centesimas +""
}

function cronometro () {
	if (centesimas < 99) {
		centesimas++;
		if (centesimas < 10) { centesimas = "0"+centesimas }
        tiempo.innerHTML = "Reloj: "+ minutos +":"+ segundos +":"+ centesimas +""
	}
	if (centesimas == 99) {
		centesimas = -1;
	}
	if (centesimas == 0) {
		segundos ++
		if (segundos < 10) { segundos = "0"+segundos }
		tiempo.innerHTML = "Reloj: "+ minutos +":"+ segundos +":"+ centesimas +""
	}
    if(segundos == $("#tiempo-monitoreo option:selected").val()){
        reiniciarCronometro()
        monitorearExpre()
    }
	if (segundos == 59) {
		segundos = -1
	}
	if ( (centesimas == 0)&&(segundos == 0) ) {
		minutos++
		if (minutos < 10) { minutos = "0"+minutos }
		tiempo.innerHTML = "Reloj: "+ minutos +":"+ segundos +":"+ centesimas +""
	}
	if (minutos == 59) {
		minutos = -1
	}
    
}

function monitorearExpre(){
    var csrftoken = getCookie('csrftoken')
    context.drawImage(video, 0, 0, 640, 480)
    const data = canvas.toDataURL()
    $.ajax({
        url: '/monitorear-expesiones/',
        type: 'POST',
        data: {csrfmiddlewaretoken: csrftoken, 'imagen': data},
        dataType: "json"
    }).done(function (data) {
        reiniciarCronometro()
        inicioCronometro()
        switch (data.result) {
            case '1':
                if(data.tiene_rostro == '1'){
                    $("#estado-monitoreo").text('Estado del monitoreo: Rostro detectado con expresión facial de ' + data.expresion_facial)
                    $("#estado-monitoreo").css("color", "#000000")
                    cont_imagenes += 1
                }else{
                    $("#estado-monitoreo").text('Estado del monitoreo: No existe un rostro en la imagen')
                    $("#estado-monitoreo").css("color", "#ff0000")
                }
            break;
            case '0':
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Sucedió un error durante el monitoreo facial, intentalo de nuevo'
                });
            break;
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        reiniciarCronometro()
        inicioCronometro()
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Sucedió un error durante el monitoreo facial, intentalo de nuevo'
        });
        switchEntrenamiento.disabled = false
    }).always(function (data) {
    });
}
/*
Swal.fire({
    icon: 'warning',
    title: 'Oops...',
    text: 'Debe realizar el entrenamiento facial para ponder activar el monitoreo'
});*/