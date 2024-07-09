async function fetchStock() {
    try {
        const response = await fetch('http://localhost:5000/stock');
        if (!response.ok) {
            throw new Error('Failed to fetch stock data');
        }
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
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

fetchStock();

document.getElementById('logout').addEventListener('click', async function(event){
    //window.location.href='login.html';
    event.preventDefault();

    try {
        const response = await fetch('/logout', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        if (response.ok) {
            window.location.href = '/login'
        } else {
            console.error('Logout Failed');
        }
    }
    catch (error){
        console.error('Network Error', error)
    }

});