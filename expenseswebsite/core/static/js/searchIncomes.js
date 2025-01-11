const searchIncomesField = document.querySelector("#searchIncomes");
const tableOutput = document.querySelector(".table-output");
const tableList = document.querySelector(".list-table");
const pagination = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");
tableOutput.style.display = "none";

searchIncomesField.addEventListener("keyup", async (e) => {
  const searchStr = e.target.value;

  if (searchStr.trim().length > 0) {
    tbody.innerHTML = "";
    fetch("/search-incomes", {
      method: "POST",
      body: JSON.stringify({ searchText: searchStr }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        tableList.style.display = "none";
        tableOutput.style.display = "block";
        if (data.length === 0) {
          tbody.innerHTML = "No incomes found";
          pagination.style.display = "none";
        } else {
          pagination.style.display = "block";

          data.forEach((income) => {
            tbody.innerHTML += `
                <tr>
                    <td>${income.amount}</td>
                    <td>${income.description}</td>
                    <td>${income.source}</td>
                    <td>${income.date}</td>
                    <td>
                        <a href="/income-edit/${income.id}" class="btn btn-primary">Edit</a>
                        <a href="/income-delete/${income.id}" class="btn btn-danger">Delete</a>
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
