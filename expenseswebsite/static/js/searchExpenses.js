const searchField = document.querySelector("#searchField");

//контейнер, который будет отображать результаты поиска.
const tableOutput = document.querySelector(".table-output");

//таблица, которая, вероятно, отображает все данные и скрывается, когда происходит поиск.
const appTable = document.querySelector(".app-table");

//контейнер для пагинации, который скрывается при отображении результатов поиска.
const paginationContainer = document.querySelector(".pagination-container");

//первоначально скрывает контейнер результатов поиска.
tableOutput.style.display = "none";

//элемент, который отображает сообщение, когда поиск не дает результатов.
const noResults = document.querySelector(".no-results");

//элемент тела таблицы, куда будут добавлены результаты поиска.
const tbody = document.querySelector(".table-body");





//Добавляется обработчик события на searchField
searchField.addEventListener("keyup", (e) => {
  //значение поля поиска
  const searchValue = e.target.value;

  //проверяем что поля ввода не пустое с помощью trim()
  if (searchValue.trim().length > 0) {
    //cкривает контейнер пагинации
    paginationContainer.style.display = "none";

    //очищает предидущие результати поиска
    tbody.innerHTML = "";

    //передаем Пост запрос на "/search-expenses" введенный поисковый запрос в формате JSON.
    fetch("/search-expenses", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {//Если данные получены:
        console.log("data", data);
        appTable.style.display = "none";//скрывается основная таблица.
        tableOutput.style.display = "block";//отображается контейнер результатов поиска.

        console.log("data.length", data.length);

        if (data.length === 0) { //Если результатов нет 
          noResults.style.display = "block"; //отображается сообщение о том, что результатов нет
          tableOutput.style.display = "none";//tableOutput скрывается.
        } else {
          noResults.style.display = "none";//Сообщение о ненайденных результатах скрывается
          data.forEach((item) => {
            //Каждый элемент в массиве данных обходится с помощью forEach
            //и в tbody добавляются строки таблицы с данными о каждой трате
            tbody.innerHTML += ` 
                <tr>
                <td>${item.amount}</td>
                <td>${item.category}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
                </tr>`;
          });
        }
      });
    //если пользователь удалил запрос
  } else {
    tableOutput.style.display = "none";//скрывается
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
    //appTable и paginationContainer вновь отображаются
  }
});
