function success(result) {
  console.log("Item Removed!");
}

///// SENDS POST REQUEST TO REMOVE AN EXPENSE
function removeExpense(value) {
  var data = {
    item: value,
  };

  $.ajax({
    type: "POST",
    url: "/remove_expense/" + data.item,
    data: { json: JSON.stringify(data) },
    success: success,
  });

  $(`[name=${value}]`)
    .parents("div")
    .css("display", "none");
  removeExpenses("itemcost", "#totalexpenses");
  calculate();
}

///// SENDS POST REQUEST TO REMOVE INCOME
function removeIncome(value) {
  var data = {
    item: value,
  };

  $.ajax({
    type: "POST",
    url: "/remove_income/" + data.item,
    data: { json: JSON.stringify(data) },
    success: success,
  });

  $(`[name=${value}]`)
    .parents("div")
    .css("display", "none");
  removeExpenses("incomeamount", "#totalincome");
  removeExpenses("feeamount", "#totalfees");
  calculate();
}

//// SUMS THE TOTAL OF INCOME, FEES, AND EXPENSES
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

//// DOES CALCULATION TO CHANGE EXPENSES VALUE IN THE LAYOUT WHEN AN EXPENSE IS REMOVED
function removeExpenses(classname, headerid) {
  total = 0;

  let item = document.getElementsByClassName(classname);

  for (var i = 0; i < item.length; i++) {
    if (
      $(item[i])
        .parents("div")
        .css("display") == "none"
    ) {
    } else {
      total += parseFloat(item[i].innerText.match(/\d+/g).map(Number));
    }
  }
  if (classname == "itemcost" || classname == "feeamount") {
    $(headerid).text("$" + total * -1);
  } else {
    $(headerid).text("$" + total);
  }
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
