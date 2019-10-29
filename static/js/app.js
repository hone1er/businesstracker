function sort_it(value) {
  if (value == "cost") {
    $("#expense-out").append(
      $("#expense-out .expense").sort(function(a, b) {
        return a.getAttribute(value) - b.getAttribute(value);
      })
    );
  } 
  else if (value == "income") {
    $("#expense-out").append(
      $("#expense-out .expense").sort(function(a, b) {
        return b.getAttribute(value) - a.getAttribute(value);
      })
    );
  }
  else if (value == "date") {
    $("#expense-out").append(
      $("#expense-out .expense").sort(function(a, b) {
        // Turn your strings into dates, and then subtract them
        // to get a value that is either negative, positive, or zero.
        return (
          new Date(b.getAttribute(value)) - new Date(a.getAttribute(value))
        );
      })
    );
  } else if (value == "name" || value == "category" || "platform") {
    $("#expense-out").append(
      $("#expense-out .expense").sort(function(a, b) {
        return ("" + a.getAttribute(value)).localeCompare(
          b.getAttribute(value)
        );
      })
    );
  }
}

function reverse_list(){
  var expense = document.getElementById("expense-out");
  var i = expense.childNodes.length;
  while (i--)
    expense.appendChild(expense.childNodes[i]);
}

function success(result) {
  console.log("Item Removed!");
}

// ///// SENDS POST REQUEST TO REMOVE AN EXPENSE, NOT IN USE BECAUSE PAGE NEEDED TO BE RELOADED TO UPDATE CHARTS
// function removeExpense(value) {
//   var data = {
//     item: value
//   };

//   $.ajax({
//     type: "POST",
//     url: "/remove_expense/" + data.item,
//     data: { json: JSON.stringify(data) },
//     success: success
//   });

//   $(`[id=${value}]`).css("display", "none");
//   removeItems("itemcost", "#totalexpenses");
//   calculate();
// }

///// SENDS POST REQUEST TO REMOVE INCOME
function removeIncome(value) {
  var data = {
    item: value
  };

  $.ajax({
    type: "POST",
    url: "/remove_income/" + data.item,
    data: { json: JSON.stringify(data) },
    success: success
  });

  $(`[name=${value}]`)
    .parents("div")
    .css("display", "none");
  removeItems("incomeamount", "#totalincome");
  removeItems("feeamount", "#totalfees");
}

//// SUMS THE TOTAL OF INCOME, FEES, AND EXPENSES FOR PROFIT/LOSS
function calculate() {
  i = ["totalincome", "totalexpenses", "totalfees"];
  total = 0;
  i.forEach(element => {
    let item = document.getElementById(element);
    if (item == null) {
      item = 0;
    } else {
      total += parseFloat(item.innerText.replace(/\$/g, ""));
    }
  });

  totalid = document.getElementById("profitloss");

  if (total >= 0) {
    totalid.style.color = "green";
  } else {
    totalid.style.color = "rgba(158, 9, 9)";
  }

  totalid.innerHTML = "$" + total.toFixed(2);
}

// //// DOES CALCULATION TO CHANGE EXPENSES VALUE IN THE LAYOUT WHEN AN EXPENSE IS REMOVED
// function removeItems(classname, headerid) {
//   total = 0;

//   let item = document.getElementsByClassName(classname);

//   for (var i = 0; i < item.length; i++) {
//     if (
//       $(item[i])
//         .parents("div")
//         .css("display") == "none"
//     ) {
//     } else {
//       total += parseFloat(item[i].innerText.match(/\d+/g).map(Number));
//     }
//   }
//   if (classname == "itemcost" || classname == "feeamount") {
//     $(headerid).text("$" + total * -1);
//   } else {
//     $(headerid).text("$" + total);
//   }
// }

function plotExpenses(type) {
  var temp_dates = $(type).sort(function(a, b) {
    return ("" + a.getAttribute("date")).localeCompare(b.getAttribute("date"));
  });

  if (temp_dates.length <= 0) {
    return;
  }
  var data = [];
  let dates = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
  ];
  let cost = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
  let base = []

  for (let i = 0; i < temp_dates.length; i++) {
    // let text = [];
    const element = temp_dates[i];
    var month;

    switch (element.getAttribute("date").slice(5, -3)) {
      case "01":
        month = "Jan";
        cost[0] = cost[0] + element.getAttribute("cost") * -1;
        break;
      case "02":
        month = "Feb";
        cost[1] = cost[1] + element.getAttribute("cost") * -1;
        break;
      case "03":
        month = "Mar";
        cost[2] = cost[2] + element.getAttribute("cost") * -1;
        break;
      case "04":
        month = "Apr";
        cost[3] = cost[3] + element.getAttribute("cost") * -1;
        break;
      case "05":
        month = "May";
        cost[4] = cost[4] + element.getAttribute("cost") * -1;
        break;
      case "06":
        month = "June";
        cost[5] = cost[5] + element.getAttribute("cost") * -1;
        break;
      case "07":
        month = "July";
        cost[6] = cost[6] + element.getAttribute("cost") * -1;
        break;
      case "08":
        month = "Aug";
        cost[7] = cost[7] + element.getAttribute("cost") * -1;
        break;
      case "09":
        month = "Sep";
        cost[8] = cost[8] + element.getAttribute("cost") * -1;
        break;
      case "10":
        month = "Oct";
        cost[9] = cost[9] + element.getAttribute("cost") * -1;
        break;
      case "11":
        month = "Nov";
        cost[10] = cost[10] + element.getAttribute("cost") * -1;
        break;
      case "12":
        month = "Dec";
        cost[11] = cost[11] + element.getAttribute("cost") * -1;
    }
    var color
    if (type == '.expense') {
      color = "rgba(204,37,41, 0.89)"
    }
    else {
      color = "rgba(36, 131, 36, 0.869)"
    }
  }
  for (let i = 0; i < cost.length; i++) {
    const element = cost[i];
    base.push(element*-1)
  }
  var trace = {
    x: dates,
    y: cost,
    base: base,
    hovertemplate: '<b>Expenses</b>: $%{base:.2f}' +
    '<br><b>Month</b>: %{x}<br><extra></extra>',
    marker: { color: color },
    type: "bar",
    line: {
      color: "rgb(204,37,41)"
    }
  };
  data.push(trace);
  const layout = {
    barmode: "stack",
    xaxis: {
      tickfont: {
        size: 14,
        color: "rgb(107, 107, 107)"
      }
    },
    yaxis: {
      title: "USD ($)",
      tickformat: "$",
      titlefont: {
        size: 16,
        color: "rgb(107, 107, 107)"
      },
      tickfont: {
        size: 14,
        color: "rgb(107, 107, 107)"
      }
    },
    legend: {
      x: 0,
      y: 1.5,
      bgcolor: "rgba(255, 255, 255, 0)",
      bordercolor: "rgba(255, 255, 255, 0)"
    }
  };

  Plotly.newPlot("plot", data, layout, { responsive: true });
}

//// IF FILE UPLOAD IS SUCCESSFUL, SET THE CLASS OF THE BANNER TO ALERT-PRIMARY TO SHOW BLUE BANNER
if ($("#message").text() != "No selected file") {
  $(".alert").removeClass("alert-danger");
  $(".alert").addClass("alert-primary");
}

/// THIS IS NEEDED TO REMOVE THE BANNER THAT APPEARS WHEN SENDING FILES
$(".close").click(function() {
  $(".alert").css("display", "none");
});

///// ENABLES CLOSING OF THE BANNER ON MOBILE /// TESTED ON IOS
$(".close").on("click touchend", function(event) {
  if (event.type == "click") detectTap = true; //detects click events
  if (detectTap) {
    $(".alert.alert-dismissable").css("display", "none");
  }
});

calculate();

let item = document.getElementsByClassName("itemcost");
for (let i = 0; i < item.length; i++) {
  const element = item[i];
  element.innerText = element.innerText.replace("$-", "$");
}

if (window.location.pathname == "/get_expenses") {
  plotExpenses('.expense');
}

if (window.location.pathname == "/income") {
  plotExpenses('.project');
}