document.addEventListener('DOMContentLoaded', function() {
  
  
  const perPage = 4;  // This should match the backend

  function loadIncomes(page) {
    const url = `/income/get_incomes?page=${page}`;
    console.log('Fetching URL:', url);
    fetch(url)
      .then(response => response.json())
      .then(data => {
        console.log("log from income_list.js:",data);
        const incomeList = document.getElementById('income-list');
        incomeList.innerHTML = '';  // Clear the current content
        data.data.forEach(income => {
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
        document.getElementById('prev-button').disabled = data.current_page <= 1;
        document.getElementById('next-button').disabled = data.current_page >= data.num_pages;
      })
      .catch(error => console.error('Error:', error));
    }

    let currentPage = 1;  // Initialize current page

    // Function to change the current page
    function changePage(offset) {
      const newPage = currentPage + offset;
      currentPage = newPage; // Update the current page
      loadIncomes(newPage); // Load the incomes for the new page
    }
  
    // Load the initial page of incomes
    loadIncomes(currentPage);
  
    // Event listeners for the pagination buttons
    document.getElementById('prev-button').addEventListener('click', function() {
      if (currentPage > 1) {
        changePage(-1); // Go to the previous page
      }
    });
  
    document.getElementById('next-button').addEventListener('click', function() {
      changePage(1); // Go to the next page
    });

});




