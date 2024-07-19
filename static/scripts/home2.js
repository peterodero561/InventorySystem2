
document.querySelectorAll('.buttons button').forEach(button => {
    button.addEventListener('click', function() {
        // Remove active class from all buttons
        document.querySelectorAll('.buttons button').forEach(btn => btn.classList.remove('active'));

        // Add active class to the clicked button
        this.classList.add('active');

        const tableName = this.value;
        document.getElementById('table-name').value = tableName;
        fetchStock(tableName);
    });
});
async function fetchStock(tableName) {
    const response = await fetch(`http://localhost:5005/inventory/stock/${tableName}`);
    const stocks = await response.json();
    const tbody = document.querySelector('#inventory-table tbody');
    tbody.innerHTML = '';

    stocks.forEach((stock, index) => {
    
        const tr = document.createElement('tr');

        // Create and populate numbering cell
        const tdNumber = document.createElement('td');
        tdNumber.textContent = index + 1; // Start numbering from 1
        tr.appendChild(tdNumber);

        const td1 = document.createElement('td');
        const td2 = document.createElement('td');
        const td3 = document.createElement('td');
        const td4 = document.createElement('td');
        const td5 = document.createElement('td');
        

        td1.textContent = stock.itemName;
        td2.textContent = stock.itemQuantity;
        td3.textContent = stock.itemCategory;
        td4.textContent = stock.itemBrand;
        td5.textContent = stock.itemNotes;

        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        tr.appendChild(td5);
        

        tbody.appendChild(tr);
    });
}

fetchStock('ict')

document.getElementById('logout').addEventListener('click', async function(event){
    //window.location.href='login.html';
    event.preventDefault();

    try {
        const response = await fetch('/inventory/logout', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        if (response.ok) {
            window.location.href = '/inventory/login'
        } else {
            console.error('Logout Failed');
        }
    }
    catch (error){
        console.error('Network Error', error)
    }

});