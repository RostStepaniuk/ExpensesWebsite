//поле для ввода имени пользователя.
const usernameField = document.querySelector("#usernameField");
//область для отображения сообщения об ошибке валидации имени пользователя.
const feedBackArea = document.querySelector(".invalid_feedback");
//поле для ввода электронной почты.
const emailField = document.querySelector("#emailField");
//область для отображения сообщения об ошибке валидации электронной почты.
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
//поле для ввода пароля.
const passwordField = document.querySelector("#passwordField");
//область для отображения успеха проверки имени пользователя.
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
//кнопка для переключения видимости пароля.
const showPasswordToggle = document.querySelector(".showPasswordToggle");
//кнопка отправки формы.
const submitBtn = document.querySelector(".submit-btn");

//то функция, которая изменяет тип поля ввода пароля с password на text
const handleToggleInput = (e) => {
  if (showPasswordToggle.textContent === "SHOW") {
    showPasswordToggle.textContent = "HIDE";
    passwordField.setAttribute("type", "text");
  } else {
    showPasswordToggle.textContent = "SHOW";
    passwordField.setAttribute("type", "password");
  }
};
showPasswordToggle.addEventListener("click", handleToggleInput);


//Валидация электронной почты:
emailField.addEventListener("keyup", (e) => {
  // Эта строка добавляет обработчик события на элемент emailField. 
  // Обработчик срабатывает каждый раз, когда пользователь отпускает клавишу, 
  //находясь в поле ввода (событие "keyup").
  const emailVal = e.target.value;
  // e.target.value содержит текущее значение поля ввода. 
  emailField.classList.remove("is-invalid");
  // Удаляется класс 'is-invalid' у элемента emailField, который может использоваться для 
  //визуального отображения ошибки валидации (например, красной рамкой вокруг поля).
  emailFeedBackArea.style.display = "none";
  // Скрывается область обратной связи (emailFeedBackArea), содержащая сообщения об ошибках.

  //если поле не пустое
  if (emailVal.length > 0) {
    fetch("/authentication/validate-email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
    // Отправляется POST-запрос на сервер по адресу "/authentication/validate-email" 
    // с JSON, содержащим адрес электронной почты.
      .then((res) => res.json())
      // Когда сервер ответит, promis(обещание) разрешается, и ответ преобразуется в JSON.
      .then((data) => {
      // Полученный JSON обрабатывается в следующем блоке кода.
        console.log("data", data);
        // В консоль выводится объект data, содержащий ответ сервера.
        if (data.email_error) {
        // Если в объекте data есть ключ email_error
          submitBtn.disabled = true;
          // Кнопка отправки (submitBtn) становится неактивной.
          emailField.classList.add("is-invalid");
          // К полю ввода emailField добавляется класс 'is-invalid' для 
          // визуальной индикации ошибки.
          emailFeedBackArea.style.display = "block";
          // Область обратной связи снова делается видимой.
          emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
          // В область обратной связи помещается сообщение об ошибке, полученное от сервера.
        } else {
        // Если ключа email_error нет в объекте data, то:
          submitBtn.removeAttribute("disabled");
          // Удаляется атрибут 'disabled' у кнопки отправки, делая её активной.
      }
    });
}
});

//Валидация имени пользователя:
usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;

  usernameSuccessOutput.style.display = "block";

  usernameSuccessOutput.textContent = `Checking  ${usernameVal}`;

  usernameField.classList.remove("is-invalid");
 
  feedBackArea.style.display = "none";

  if (usernameVal.length > 0) {
    fetch("/authentication/validate-username", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        usernameSuccessOutput.style.display = "none";
        if (data.username_error) {
          usernameField.classList.add("is-invalid");
          feedBackArea.style.display = "block";
          feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
          submitBtn.disabled = true;
        } else {
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});
