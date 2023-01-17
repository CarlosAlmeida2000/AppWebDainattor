// Función para crear una llave de seguridad "crsftoken" y poder realizar una petición ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Función para validar campos de sólo letras
function soloLetras(event) {
    var regex = new RegExp("^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
    }
}

// Función para validar campos de número de teléfonos
function soloCedula(event) {
    var regex = new RegExp("^[a-zA-Z0-9-. ]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
    }
}