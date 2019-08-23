const income = document.getElementById("totalincome");
const expenses = document.getElementById("totalexpenses");
const fees = document.getElementById("totalfees");

const total =
  parseFloat(income.innerText.replace(/\$/g, "")) +
  parseFloat(expenses.innerText.replace(/\$/g, "")) +
  parseFloat(fees.innerText.replace(/\$/g, ""));

totalid = document.getElementById("profitloss");
if (totalid.innerHTML >= "0") {
  totalid.setAttribute("style", "color:#222");
} else {
  totalid.setAttribute("style", "color:rgba(158, 9, 9);");
}

totalid.innerHTML = total;

if ($("#message").text() != 'No selected file') {
  $(".alert").removeClass("alert-danger");
  $(".alert").addClass("alert-primary");

}
$(".close").click(function(){
  $(".alert").css("display", "none");
  console.log($("#message").text())
});

