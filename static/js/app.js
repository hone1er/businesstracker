const income = document.getElementById('totalincome')
const expenses = document.getElementById('totalexpenses')

let total = income.innerText.replace(/\$/g, '') - expenses.innerText.replace(/\$/g, '')

totalid = document.getElementById('profitloss')
if (totalid.innerHTML >= '0') {
    totalid.setAttribute('style', 'color:#222')
}
else {
    totalid.setAttribute('style', 'color:rgba(158, 9, 9);')
}

totalid.innerHTML = total
