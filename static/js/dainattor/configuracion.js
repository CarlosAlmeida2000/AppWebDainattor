const switchEntrenamiento = document.getElementById("switchEntrenamiento")
const switchMonitoreo = document.getElementById("switchMonitoreo")
const video = document.getElementById('video')
var canvas = document.getElementById('canvas')
var context = canvas.getContext('2d')
var cont_imagenes = 0
var caputarar_imagenes = 70
var entrenando = false
var monitoreando = false

// iniciar cámara web
function iniciarVideo(accion) {
    navigator.mediaDevices.getUserMedia({
        video: true
    })
        .then(stream => {
            window.localStream = stream;
            video.srcObject = stream;
            if (accion == 'entrenamiento') {
                $("#seccion-entrenamiento").removeClass("d-none");
                iniciarEntrenamiento()
            } else {
                $("#seccion-monitoreo").removeClass("d-none");
                inicioCronometro()
            }
        })
        .catch((err) => {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Sucedió un error en iniciar el video, intentalo de nuevo'
            });
        });
}

// detener cámara web
function detenerVideo() {
    localStream.getVideoTracks()[0].stop()
    video.srcObject = null
}

switchEntrenamiento.addEventListener('click', function () {
    if (!entrenando) {
        entrenando = true
        document.querySelector("#switchMonitoreo").setAttribute("disabled", false);
        iniciarVideo('entrenamiento')
    } else {
        entrenando = false
        cont_imagenes = 0
        detenerVideo()
        document.querySelector("#switchMonitoreo").removeAttribute("disabled")
        $("#seccion-entrenamiento").addClass("d-none");
    }
});

switchMonitoreo.addEventListener('click', function () {
    if (!monitoreando) {
        var csrftoken = getCookie('csrftoken')
        $.ajax({
            url: '/tiene-entrenamiento/',
            type: 'POST',
            data: { csrfmiddlewaretoken: csrftoken },
            dataType: "json"
        }).done(function (data) {
            if (data.result) {
                monitoreando = true
                document.querySelector("#switchEntrenamiento").setAttribute("disabled", false);
                $("#reloj-monitoreo").css("color", "#0e0c66")
                $("#tiempo").css("color", "#0e0c66")
                iniciarVideo('monitoreo')
            } else {
                Swal.fire({
                    icon: 'warning',
                    title: 'Oops...',
                    text: 'Debe de realizar el entrenamiento facial para poder monitorear las expresiones faciales'
                });
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Sucedió un error al cargar los datos, intentalo de nuevo'
            });
        }).always(function (data) {
        });
    } else {
        monitoreando = false
        detenerVideo()
        reiniciarCronometro()
        document.querySelector("#switchEntrenamiento").removeAttribute("disabled")
        $("#icono-exprexion").html('<i class="fas fa-smile-beam"></i> <i class="fas fa-search"></i>');
        $("#estado-monitoreo").text('')
        $("#seccion-monitoreo").addClass("d-none");
    }
});

function iniciarEntrenamiento() {
    var csrftoken = getCookie('csrftoken')
    context.drawImage(video, 0, 0, 640, 480)
    const data = canvas.toDataURL()
    $.ajax({
        url: '/capturar-rostro-entrenamiento/',
        type: 'POST',
        data: { csrfmiddlewaretoken: csrftoken, 'imagen': data, 'cont_imagenes': cont_imagenes },
        dataType: "json"
    }).done(function (data) {
        switch (data.result) {
            case '1':
                if (data.tiene_rostro == '1') {
                    $("#estado-entrenamiento").text((cont_imagenes + 1) + ' de ' + caputarar_imagenes + ' fotos')
                    $("#estado-entrenamiento").css("color", "#0e0c66")
                    $("#camara-entrenamiento").css("color", "#0e0c66")
                    cont_imagenes += 1
                } else {
                    $("#estado-entrenamiento").text('No se detecta ningún rostro')
                    $("#estado-entrenamiento").css("color", "#ff0000")
                    $("#camara-entrenamiento").css("color", "#ff0000")
                }
                break;
            case '0':
                cont_imagenes = 0
                detenerVideo()
                document.querySelector("#switchMonitoreo").removeAttribute("disabled")
                $("#seccion-entrenamiento").addClass("d-none");
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Sucedió un error durante el entrenamiento facial, intentalo de nuevo'
                });
                break;
        }
        if (cont_imagenes < caputarar_imagenes & entrenando == true) {
            iniciarEntrenamiento()
        } else if (entrenando == false) {
            cont_imagenes = 0
            detenerVideo()
            $("#seccion-entrenamiento").addClass("d-none");
            return 0
        } else {
            cont_imagenes = 0
            detenerVideo()
            document.querySelector("#switchMonitoreo").removeAttribute("disabled")
            $("#seccion-entrenamiento").addClass("d-none");
            Swal.fire({
                icon: 'success',
                title: '¡Excelente!',
                text: 'Entrenamiento facial culminado exitosamente.'
            });
            return 0
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        cont_imagenes = 0
        detenerVideo()
        document.querySelector("#switchMonitoreo").removeAttribute("disabled")
        $("#seccion-entrenamiento").addClass("d-none");
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Sucedió un error durante el entrenamiento facial, intentalo de nuevo'
        });
    }).always(function (data) {
    });
}


// Cronómetro para analizar expresiones faciales
var centesimas = 0
var segundos = 0
var minutos = 0

function inicioCronometro() {
    control = setInterval(cronometro, 10);
}

function reiniciarCronometro() {
    clearInterval(control)
    centesimas = 0
    segundos = 0
    minutos = 0
    tiempo.innerHTML = minutos + ":" + segundos + ":" + centesimas + ""
}

function cronometro() {
    if (centesimas < 99) {
        centesimas++;
        if (centesimas < 10) { centesimas = "0" + centesimas }
        tiempo.innerHTML = minutos + ":" + segundos + ":" + centesimas + ""
    }
    if (centesimas == 99) {
        centesimas = -1;
    }
    if (centesimas == 0) {
        segundos++
        if (segundos < 10) { segundos = "0" + segundos }
        tiempo.innerHTML = minutos + ":" + segundos + ":" + centesimas + ""
    }
    if (segundos == $("#tiempo-monitoreo option:selected").val()) {
        monitorearExpre()
        reiniciarCronometro()
    }
    if (segundos == 59) {
        segundos = -1
    }
    if ((centesimas == 0) && (segundos == 0)) {
        minutos++
        if (minutos < 10) { minutos = "0" + minutos }
        tiempo.innerHTML = minutos + ":" + segundos + ":" + centesimas + ""
    }
    if (minutos == 59) {
        minutos = -1
    }

}

function monitorearExpre() {
    var csrftoken = getCookie('csrftoken')
    context.drawImage(video, 0, 0, 640, 480)
    const data = canvas.toDataURL()
    $.ajax({
        url: '/monitorear-expesiones/',
        type: 'POST',
        data: { csrfmiddlewaretoken: csrftoken, 'imagen': data },
        dataType: "json"
    }).done(function (data) {
        reiniciarCronometro()
        inicioCronometro()
        switch (data.result) {
            case '1':
                if (data.tiene_rostro == '1') {
                    $("#estado-monitoreo").text('Última expresión facial reconocida: ' + data.expresion_facial)
                    $("#estado-monitoreo").css("color", "#0e0c66")
                    switch (data.expresion_facial) {
                        case 'Enfadado':
                            $("#icono-exprexion").html('<i class="fas fa-angry"></i>');
                            break;
                        case 'Disgustado':
                            $("#icono-exprexion").html('<i class="fas fa-frown"></i>');
                            break;
                        case 'Temeroso':
                            $("#icono-exprexion").html('<i class="fas fa-grimace"></i>');
                            break;
                        case 'Feliz':
                            $("#icono-exprexion").html('<i class="fas fa-laugh-beam"></i>');
                            break;
                        case 'Neutral':
                            $("#icono-exprexion").html('<i class="fas fa-smile"></i>');
                            break;
                        case 'Triste':
                            $("#icono-exprexion").html('<i class="fas fa-sad-cry"></i>');
                            break;
                        case 'Sorprendido':
                            $("#icono-exprexion").html('<i class="fas fa-surprise"></i>');
                            break;
                    }
                } else {
                    $("#estado-monitoreo").text('En la última toma no se reconoció un rostro')
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
    }).always(function (data) {
    });

}