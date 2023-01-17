const labels = ['Enfadado', 'Disgustado', 'Temeroso', 'Feliz', 'Neutral', 'Triste', 'Sorprendido']
 
const graph = document.querySelector("#grafica-expresiones")

var csrftoken = getCookie('csrftoken')
$.ajax({
    url: '/grafico/',
    type: 'POST',
    data: {csrfmiddlewaretoken: csrftoken},
    dataType: "json"
}).done(function (data) {
    if(data.result == '1'){
        if(data.grafico.length > 0){
            graficar([data.grafico[0].enfadado, data.grafico[0].disgustado, data.grafico[0].temeroso, data.grafico[0].feliz, data.grafico[0].neutral, data.grafico[0].triste, data.grafico[0].sorprendido])
            $("#prediccion").text(data.grafico[0].prediccion_trastorno)
            for(let i = 0; i < data.grafico[0].actividades.length; i++){
                $("#lista_actividades").prepend("<li> "+ data.grafico[0].actividades[i] +" </li>")
            }
        }else{
            graficar([0, 0, 0, 0, 0, 0, 0])
            $("#prediccion").text("Sin predicción, porque no existe un historial")
            $("#lista_actividades").prepend("<li> Sin actividades, porque no existe un historial </li>")
        }
    }else{
        graficar([0, 0, 0, 0, 0, 0, 0])
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Sucedió un error al cargar los datos, intentalo de nuevo'
        });
    }
}).fail(function (jqXHR, textStatus, errorThrown) {
    graficar([0, 0, 0, 0, 0, 0, 0])
    Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Sucedió un error al cargar los datos, intentalo de nuevo'
    });
    switchEntrenamiento.disabled = false
}).always(function (data) {
});

function graficar(data){
    const data_grafico = {
        labels: labels,
        datasets: [{
            label:"Frecuencia de las expresiones faciales",
            data: data,
            backgroundColor: [
                "#003785",
                "#688391",
                "#ffbba8",
                "#f8de7e",
                "#81c9fa",
                "#b87400",
                "#4ed2ad",
            ]
        }]
    };
    const config = {
        type: 'bar',
        data: data_grafico,
    };
    new Chart(graph, config);
}