const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tbody.innerHTML = ""; //очищаем предидущие результати поиска

    //отправляем пост запрос на сервер с данними в строке поиска
    fetch("/income/search-income", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())//преобразуем тело ответа из джсон в обьект JS
      .then((data) => { //дальше работает с єтим обьектом JS
        console.log("data", data);
        appTable.style.display = "none";//скривается основная таблица
        tableOutput.style.display = "block";//отображается таблица результата поиска

        if (data.length === 0) { //если нету результата
          noResults.style.display = "block";//сообщение об отсутс. результатов
          tableOutput.style.display = "none";
        } else {
          noResults.style.display = "none";
          data.forEach((item) => {
            tbody.innerHTML += `
                <tr>
                <td>${item.amount}</td>
                <td>${item.source}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
                </tr>`;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});
