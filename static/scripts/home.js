document.getElementById('inventory-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const itemName = document.getElementById('item-name').value;
    const itemQuantity = document.getElementById('item-quantity').value;
    const itemCategory = document.getElementById('item-category').value;
    const itemBrand = document.getElementById('item-brand').value;
    const itemNotes = document.getElementById('item-notes').value;

    fetch ('http://localhost:5000/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            itemName: itemName,
            itemQuantity: itemQuantity,
            itemCategory: itemCategory,
            itemBrand: itemBrand,
            itemNotes: itemNotes
        })
    }).then(response => {
        if (response.ok) {
            console.log('Item added successfully');
            fetchStock()
        } else {
            throw new Error('Failed to add equipment')
        }
    }).catch(error => { console.error('Error: ', error)})
    .finally(() => {
        document.getElementById('inventory-form').reset();
    });
});

async function fetchStock() {
    const response = await fetch('http://localhost:5000/stock');
    const stocks = await response.json();
    const tbody = document.querySelector('#inventory-table tbody');
    tbody.innerHTML = '';

    stocks.forEach(stock => {
        const tr = document.createElement('tr');

        const td1 = document.createElement('td');
        const td2 = document.createElement('td');
        const td3 = document.createElement('td');
        const td4 = document.createElement('td');
        const td5 = document.createElement('td');
        const td6 = document.createElement('td');

        td1.textContent = stock.itemName;
        td2.textContent = stock.itemQuantity;
        td3.textContent = stock.itemCategory;
        td4.textContent = stock.itemBrand;
        td5.textContent = stock.itemNotes;
        td6.innerHTML = '<button class="edit">Edit</button><button class="delete">Delete</button>';

        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        tr.appendChild(td5);
        tr.appendChild(td6);

        tbody.appendChild(tr);
    });
}
fetchStock();