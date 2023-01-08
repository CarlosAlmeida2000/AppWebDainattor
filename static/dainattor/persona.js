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
            url: '/guardar-usuario/',
            type: 'POST',
            data: parametros,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false
        }).done(function (data) {
            document.body.style.cursor = 'default';
            document.querySelector("#btnCrearCuenta").removeAttribute("disabled")
            if (data.result === '1') {
                Swal.fire({
                    icon: 'success',
                    text: 'Cuenta creada exitosamente, ya puedes iniciar sesión'
                })
            }else if (data.result === '3') {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'La cédula ya se encuentra registra por otro usuario'
                });
            }else if (data.result === '4') {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'El nombre de usuario ya se encuentra registro por otra persona'
                });
            }else if (data.result === '0') {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Sucedió un error en registrar tus datos, intentalo de nuevo'
                });
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
            url: '/login/',
            type: 'POST',
            data: parametros,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false
        }).done(function (data) {
            document.body.style.cursor = 'default';
            document.querySelector("#iniciarSesion").removeAttribute("disabled")
            if (data.result === '1') {
                location.href = "/home";
            }else if (data.result === '2') {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Credenciales incorrectas!, intentalo de nuevo'
                });
            }else if (data.result === '0') {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Sucedió un error al iniciar sesión, intentalo de nuevo'
                });
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            document.body.style.cursor = 'default';
            document.querySelector("#iniciarSesion").removeAttribute("disabled")
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Sucedió un error al iniciar sesión, intentalo de nuevo acaa'
            });
        }).always(function (data) {
        });
    });
});