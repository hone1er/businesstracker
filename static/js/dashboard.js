const income = document.getElementsByClassName("income_row");
const expenses = document.getElementsByClassName("expense_row");

function create_traces(target_class, attribute) {
  var temp_dates = $(target_class).sort(function(a, b) {
    return ("" + a.getAttribute("date")).localeCompare(b.getAttribute("date"));
  });

  if (temp_dates.length <= 0) {
    return;
  }

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
  let base = [];

  for (let i = 0; i < temp_dates.length; i++) {
    // let text = [];
    const element = temp_dates[i];
    var month;
    console.log(element.getAttribute("date").slice(5, -3));
    switch (element.getAttribute("date").slice(5, -3)) {
      case "01":
        month = "Jan";
        cost[0] = cost[0] + element.getAttribute(attribute) * -1;
        break;
      case "02":
        month = "Feb";
        cost[1] = cost[1] + element.getAttribute(attribute) * -1;
        break;
      case "03":
        month = "Mar";
        cost[2] = cost[2] + element.getAttribute(attribute) * -1;
        break;
      case "04":
        month = "Apr";
        cost[3] = cost[3] + element.getAttribute(attribute) * -1;
        break;
      case "05":
        month = "May";
        cost[4] = cost[4] + element.getAttribute(attribute) * -1;
        break;
      case "06":
        month = "June";
        cost[5] = cost[5] + element.getAttribute(attribute) * -1;
        break;
      case "07":
        month = "July";
        cost[6] = cost[6] + element.getAttribute(attribute) * -1;
        break;
      case "08":
        month = "Aug";
        cost[7] = cost[7] + element.getAttribute(attribute) * -1;
        break;
      case "09":
        month = "Sep";
        cost[8] = cost[8] + element.getAttribute(attribute) * -1;
        break;
      case "10":
        month = "Oct";
        cost[9] = cost[9] + element.getAttribute(attribute) * -1;
        break;
      case "11":
        month = "Nov";
        cost[10] = cost[10] + element.getAttribute(attribute) * -1;
        break;
      case "12":
        month = "Dec";
        cost[11] = cost[11] + element.getAttribute(attribute) * -1;
    }
    var color;
    if (target_class == ".expense_row") {
      color = "rgba(204,37,41, 0.89)";
    } else {
      color = "rgba(36, 131, 36, 0.869)";
    }
    var label, name;
    if (target_class == ".expense_row") {
      label = "Expenses";
      name = "Expenses";
    } else {
      label = "Income";
      name = "Income";
    }
  }
  for (let i = 0; i < cost.length; i++) {
    const element = cost[i];
    base.push(element * -1);
  }
  var trace = {
    x: dates,
    y: cost,
    base: base,
    hovertemplate:
      `<b>${label}</b>: $%{base:.2f}` +
      "<br><b>Month</b>: %{x}<br><extra></extra>",
    marker: { color: color },
    type: "bar",
    line: {
      color: "rgb(204,37,41)"
    },
    name: name
  };
  return trace;
}

function barChart(data, div) {
  const layout = {
      barmode: 'stack',
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

  Plotly.newPlot(div, data, layout, { responsive: true });
}

function createPieTrace() {
    var trace = {}
    const expenses = document.getElementsByClassName("expense_row");
    for (let i = 0; i < expenses.length; i++) {
        const element = expenses[i];
        const category = element.getAttribute('category')
        if (category in trace) {
            trace[category] += parseInt(element.getAttribute('cost'))
        }
        else {
            trace[category] = parseInt(element.getAttribute('cost'))
        }
    }
   return trace
}

function pieChart(trace) {
    var values = []
    var labels = []
    Object.keys(trace).forEach(function(key) {
        values.push(trace[key]*-1)
        labels.push(key)
    });
    console.log(values, labels)
    var data = [{
        values: values,
        labels: labels,
        hole: .4,
        type: 'pie'
      }];
      

      
      Plotly.newPlot('pie_chart', data, {responsive: true});
}

var data = [create_traces(".income_row", "gross")];
data.push(create_traces(".expense_row", "cost"));
console.log(data);

barChart(data, "revenue_plot");
const pieTrace = createPieTrace()
pieChart(pieTrace)
