// Получаем контекст 2d HTML элемента <canvas> с идентификатором "myChart" 
//для отрисовки графика
var ctx = document.getElementById("myChart").getContext("2d");

//getRandomType случайным образом выбирает тип графика из предопределённого списка.
const getRandomType = () => {
  const types = [
    "bar",
    "horizontalBar",
    "pie",
    "line",
    "radar",
    "doughnut",
    "polarArea",
  ];
  return types[Math.floor(Math.random() * types.length)];
};

//displayChart принимает два аргумента: data и labels. data - это массив данных, 
//которые будут отображаться на графике, а labels - это метки категорий по оси X.
const displayChart = (data, labels) => {
  const type = getRandomType();//getRandomType() возвращает случайно выбранный тип диаграммы из предоставленного списка.
  var myChart = new Chart(ctx, {
    //type определяет тип графика 
    type: type, // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data: { //data содержит метки и набор данных с цветами для отображения.
      labels: labels, 
      datasets: [
        {
          label: `Amount (Last 6 months) (${type} View)`,
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 99, 132,0.7)",
            "rgba(75, 192, 192, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 99, 132,0.7)",
            "rgba(75, 192, 192, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: { //содержит настройки для отображения, включая заголовок графика и легенду.
      title: {
        display: true,
        text: "Expense  Distribution Per Category",
        fontSize: 25,
      },
      legend: {
        display: true,
        position: "right",
        labels: {
          fontColor: "#000",
        },
      },
    },
  });
};

//отправляет запрос на серверный URL "last_3months_stats", получает ответ в формате JSON, который содержит 
//данные за последние три месяца преобразуются в два массива: метки (labels) и 
//соответствующие данные (data), которые передаются в displayChart для отображения графика
const getCategoryData = () => {
  fetch("last_3months_stats")
    .then((res) => res.json())
    .then((res1) => {
      console.log(res1); // Здесь будет показан ответ сервера
      const results = res1.expenses_category_data;
      const [labels, data] = [Object.keys(results), Object.values(results)];
      displayChart(data, labels);
    });


};

//Этот код связан с загрузкой страницы и вызовом функции
window.onload = getCategoryData;
