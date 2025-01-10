const searchExpensesField = document.querySelector("#searchExpenses");
const tableOutput = document.querySelector(".table-output");
const tableList = document.querySelector(".list-table");
const pagination = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");
tableOutput.style.display = "none";

searchExpensesField.addEventListener("keyup", async (e) => {
  const searchStr = e.target.value;

  if (searchStr.trim().length > 0) {
    tbody.innerHTML = "";
    fetch("/search-expenses", {
      method: "POST",
      body: JSON.stringify({ searchText: searchStr }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        tableList.style.display = "none";
        tableOutput.style.display = "block";
        if (data.length === 0) {
          tbody.innerHTML = "No expenses found";
          pagination.style.display = "none";
        } else {
          pagination.style.display = "block";

          data.forEach((expense) => {
            tbody.innerHTML += `
                <tr>
                    <td>${expense.amount}</td>
                    <td>${expense.description}</td>
                    <td>${expense.category}</td>
                    <td>${expense.date}</td>
                    <td>
                        <a href="/expense-edit/${expense.id}" class="btn btn-primary">Edit</a>
                        <a href="/expense-delete/${expense.id}" class="btn btn-danger">Delete</a>
                    </td>
                </tr>
            `;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    tableList.style.display = "block";
    pagination.style.display = "block";
  }
});
