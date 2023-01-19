function mostrarValor(tipo){
//    var tipo = document.getElementById("txtClave");
    if(tipo.type == "password"){
        tipo.type = "text";
    }else{
        tipo.type = "password";
    }
}

// sobrescritura del submit del formulario registrar usuario
$(document).ready(function () {
    $("#formRegistroUsuario").submit(function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        // se bloquea el botón guardar para que el usuario no envíe múltiples peticiones
        document.querySelector("#btnCrearCuenta").setAttribute("disabled", false);
        document.body.style.cursor = 'wait';
        // petición ajax
        $.ajax({
            type: 'POST',
            url: '/guardar-usuario/',
            data: parametros,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false
        }).done(function (data) {
            document.body.style.cursor = 'default';
            document.querySelector("#btnCrearCuenta").removeAttribute("disabled")
            switch (data.result) {
                case '1':
                  Swal.fire({
                    icon: 'success',
                    title: '¡Excelente!',
                    text: 'Cuenta creada exitosamente, ya puedes iniciar sesión.',
                    confirmButtonText: 'Ok'
                  }).then((result) => {
                    window.location.href = '/';
                  });
                break;
                case '3':
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'La cédula ya se encuentra registra por otro usuario'
                    });
                break;
                case '4':
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'El nombre de usuario ya se encuentra registro por otra persona'
                    });
                break;
                case '0':
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Sucedió un error en registrar tus datos, intentalo de nuevo'
                    });
                break;
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            document.body.style.cursor = 'default';
            document.querySelector("#btnCrearCuenta").removeAttribute("disabled")
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Sucedió un error en registrar tus datos, intentalo de nuevo acaa'
            });
        }).always(function (data) {
        });
    });
});


// sobrescritura del submit del formulario de inicio de sesión
$(document).ready(function () {
    $("#formLogin").submit(function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        // se bloquea el botón guardar para que el usuario no envíe múltiples peticiones
        document.querySelector("#iniciarSesion").setAttribute("disabled", false);
        document.body.style.cursor = 'wait';
        // petición ajax
        $.ajax({
            type: 'POST',
            url: '/login/',
            data: parametros,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false
        }).done(function (data) {
            document.body.style.cursor = 'default';
            document.querySelector("#iniciarSesion").removeAttribute("disabled")
            switch (data.result) {
                case '1':
                    window.location.href = '/home';
                break;
                case '2':
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Credenciales incorrectas!, intentalo de nuevo'
                    });
                break;
                case '0':
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Sucedió un error al iniciar sesión, intentalo de nuevo'
                    });
                break;
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            document.body.style.cursor = 'default';
            document.querySelector("#iniciarSesion").removeAttribute("disabled")
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Sucedió un error al iniciar sesión, intentalo de nuevo'
            });
        }).always(function (data) {
        });
    });
});

// sobrescritura del submit del formulario modificar datos de usuario
$(document).ready(function () {
    $("#formModificaroUsuario").submit(function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        // se bloquea el botón guardar para que el usuario no envíe múltiples peticiones
        document.querySelector("#btnModificarCuenta").setAttribute("disabled", false);
        document.body.style.cursor = 'wait';
        // petición ajax
        $.ajax({
            type: 'POST',
            url: '/modificar-usuario/',
            data: parametros,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false
        }).done(function (data) {
            document.body.style.cursor = 'default';
            document.querySelector("#btnModificarCuenta").removeAttribute("disabled")
            switch (data.result) {
                case '1':
                Swal.fire({
                    icon: 'success',
                    title: '¡Excelente!',
                    text: 'Datos de perfil modificados exitosamente.',
                    confirmButtonText: 'Ok'
                    }).then((result) => {
                        location.reload()
                    });
                break;
                case '3':
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'La cédula ya se encuentra registra por otro usuario'
                    });
                break;
                case '4':
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'El nombre de usuario ya se encuentra registro por otra persona'
                    });
                break;
                case '0':
                case '2':
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Sucedió un error en registrar tus datos, intentalo de nuevo'
                    });
                break;
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            document.body.style.cursor = 'default';
            document.querySelector("#btnModificarCuenta").removeAttribute("disabled")
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Sucedió un error en modificar tus datos, intentalo de nuevo'
            });
        }).always(function (data) {
        });
    });
});

// Presisualizar la foto ingresada en el input en un elemento img
function previewimagen(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#foto-usuario').attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// sobrescritura del submit del formulario modificar foto de usuario
$(document).on('submit', '#formGuardarFoto', function (e) {
    e.preventDefault();
    var data = new FormData(this);
    // se bloquea el botón guardar para que el usuario no envíe múltiples peticiones
    document.querySelector("#btnGuardarFoto").setAttribute("disabled", false);
    document.body.style.cursor = 'wait';
    $.ajax({
        type: 'POST',
        url: '/modificar-foto-usuario/',
        data: data,
        contentType: false,
        processData: false,
    }).done(function (data) {
        document.body.style.cursor = 'default';
        document.querySelector("#btnGuardarFoto").removeAttribute("disabled")
        switch (data.result) {
            case '1':
            Swal.fire({
                icon: 'success',
                title: '¡Excelente!',
                text: 'Foto de perfil modificada exitosamente.',
                confirmButtonText: 'Ok'
                }).then((result) => {
                    location.reload();
                });
            break;
            case '0':
            case '2':
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Sucedió un error en modificar la foto, intentalo de nuevo'
                });
            break;
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        document.body.style.cursor = 'default';
        document.querySelector("#btnGuardarFoto").removeAttribute("disabled")
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Sucedió un error en modificar la foto, intentalo de nuevo'
        });
    }).always(function (data) {
    });
});