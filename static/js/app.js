function success(result) {
  alert("Item Removed!");
}

///// SENDS POST REQUEST TO REMOVE AN EXPENSE
function sendPost(value) {
  var data = {
    item: value,
  };
  
  $.ajax({
    type: "POST",
    url: "/remove_expense/" + data.item,
    data: { json: JSON.stringify(data) },
    success: success,
  });

    $(`[name=${value}]`).parents("div").css("display", "none");
    removeExpenses()
    calculate()
}

//// SUMS THE TOTAL OF INCOME, FEES, AND EXPENSES
function calculate() {
  i = ["totalincome", "totalexpenses" ,"totalfees"]
  total = 0
  i.forEach(element => {
      let item =  document.getElementById(element) 
      if (item == null) {
        item = 0
      }
      else {
        total += parseFloat(item.innerText.replace(/\$/g, ""));
      }
  });

  totalid = document.getElementById("profitloss");
  if (totalid.innerHTML >= "0") {
    totalid.setAttribute("style", "color:#222");
  } else {
    totalid.setAttribute("style", "color:rgba(158, 9, 9);");
  }

  totalid.innerHTML = total.toFixed(2);
}

//// DOES CALCULATION TO CHANGE EXPENSES VALUE WHEN AN EXPENSE IS REMOVED
function removeExpenses() {
 
  total = 0

      let item =  document.getElementsByClassName('itemcost') 
      console.log(item)
      for (var i=0; i<item.length; i++) {
        
        if ($(item[i]).parents("div").css("display") == 'none') {
          item[i] -= parseFloat(item[i].innerText.replace(/\$/g, ""));
        }
        else {
          total += parseFloat(item[i].innerText.replace(/\$/g, ""));
        }
      };
  console.log(total)
  $('#totalexpenses').text(total)
}

//// IF FILE UPLOAD IS SUCCESSFUL, SET THE CLASS OF THE BANNER TO ALERT-PRIMARY TO SHOW BLUE BANNER
if ($("#message").text() != "No selected file") {
  $(".alert").removeClass("alert-danger");
  $(".alert").addClass("alert-primary");
}


/// THIS IS NEEDED TO REMOVE THE BANNER THAT APPEARS WHEN SENDING FILES
$(".close").click(function() {
  $(".alert").css("display", "none");
  console.log($("#message").text());
});

///// ENABLES CLOSING OF THE BANNER ON MOBILE /// TESTED ON IOS
$(".close").on("click touchend", function(event) {
  if (event.type == "click") detectTap = true; //detects click events
  if (detectTap) {
    $(".alert.alert-dismissable").css("display", "none");
    console.log($("#message").text());
  }
});

calculate()

