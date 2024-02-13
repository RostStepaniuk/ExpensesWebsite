document.addEventListener('DOMContentLoaded', function() {
    fetch('/income/get_incomes')
      .then(response => response.json())
      .then(data => {
        const incomeList = document.getElementById('income-list');
        data.forEach(income => {
          const incomeDiv = document.createElement('div');
          incomeDiv.classList.add('income-box');
          incomeDiv.innerHTML = `
            <p><strong>Source:</strong> ${income.source}</p>
            <p><strong>Description:</strong> ${income.description}</p>
            <p><strong>Sum:</strong> ${income.amount}</p>
            <p><strong>Date:</strong> ${new Date(income.date).toLocaleDateString()}</p>
          `;
          incomeList.appendChild(incomeDiv);
        });
      })
      .catch(error => console.error('Error:', error));
  });


  