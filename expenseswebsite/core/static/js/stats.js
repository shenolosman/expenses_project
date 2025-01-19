const renderChart = (dataObj, labels) => {
  const ctx = document.getElementById("summaryChart"); //.getContext("2d");
  //   const labels = ["Red", "Blue", "Yellow"];
  //   const dataObj = [300, 50, 100];
  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          data: dataObj,
          lineTension: 0,
          backgroundColor: "transparent",
          borderColor: "#007bff",
          borderWidth: 4,
          pointBackgroundColor: "#007bff",
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: false,
            },
          },
        ],
      },
      legend: {
        display: false,
      },
    },
  });
  //   const data = {
  //     labels: labels,
  //     datasets: [
  //       {
  //         label: "Last 6 months expenses",
  //         data: dataObj,
  //         backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255, 205, 86)"],
  //         hoverOffset: 4,
  //       },
  //     ],
  //   };

  //   const options = {
  //     responsive: true,
  //     title: {
  //         display: true,
  //         text: "Expenses Per Category",
  //       },
  //     // plugins: {
  //     //   legend: {
  //     //     position: "top",
  //     //   },

  //     // },
  //   };
  //   const config = {
  //     type: "doughnut",
  //     data: data,
  //     options: options,
  //   };

  //   new Chart(ctx, config);
};

const getChartData = () => {
  fetch("expense-category-summary")
    .then((res) => res.json())
    .then((res) => {
      console.log(res);
      //   const labels = ;
      //   const dataObj = ;
      const [labels, dataObj] = [Object.keys(res.category_data), Object.values(res.category_data)];
      renderChart(dataObj, labels);
    })
    .catch((err) => console.log(err));
};

document.onload = getChartData();
