const labels = ['Enfadado', 'Disgustado', 'Disgustado', 'Feliz', 'Neutral', 'Triste', 'Sorprendido']
 
const graph = document.querySelector("#grafica-expresiones");
 
const data = {
    labels: labels,
    datasets: [{
        label:"Frecuencia de las expresiones faciales",
        data: [1, 2, 3, 4, 5, 6, 7],
        backgroundColor: [
            "rgba(106, 219, 213, 0.497)",
            "rgba(235, 188, 114, 0.8497)",
            "rgba(235, 188, 104, 0.797)",
            "rgba(235, 188, 134, 0.89)",
            "rgba(235, 188, 134, 0.89)",
            "rgba(235, 188, 134, 0.89)",
            "rgba(235, 188, 134, 0.89)",
        ]
    }]
};
 
const config = {
    type: 'bar',
    data: data,
};
 
new Chart(graph, config);