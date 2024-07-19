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

document.getElementById('inventory-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const itemName = document.getElementById('item-name').value;
    const itemQuantity = document.getElementById('item-quantity').value;
    const itemCategory = document.getElementById('item-category').value;
    const itemBrand = document.getElementById('item-brand').value;
    const itemNotes = document.getElementById('item-notes').value;

    const tableName = document.getElementById('table-name').value;
    if (!tableName) {
        tableName = 'ict';
    }

    fetch (`http://3.85.175.115:5005/inventory/add/${tableName}`, {
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
            fetchStock(tableName)
        } else {
            throw new Error('Failed to add equipment')
        }
    }).catch(error => { console.error('Error: ', error)})
    .finally(() => {
        document.getElementById('inventory-form').reset();
    });
});

async function fetchStock(tableName) {
    const response = await fetch(`http://3.85.175.115:5005/inventory/stock/${tableName}`);
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
        const td6 = document.createElement('td');

        td1.textContent = stock.itemName;
        td2.textContent = stock.itemQuantity;
        td3.textContent = stock.itemCategory;
        td4.textContent = stock.itemBrand;
        td5.textContent = stock.itemNotes;
        td6.innerHTML = `<button class="edit" data-id="${stock.item_id}" data-table="${tableName}">Edit</button><button class="delete" data-id="${stock.item_id}" data-table="${tableName}">Delete</button>`;

        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        tr.appendChild(td5);
        tr.appendChild(td6);

        tbody.appendChild(tr);
    });

    document.querySelectorAll('.edit').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.id;
            const tableName = this.dataset.table;
            editItem(tableName, itemId);
        });
    });

    document.querySelectorAll('.delete').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.id;
            const tableName = this.dataset.table;
            deleteItem(tableName, itemId);
        });
    });
}

async function editItem(tableName, itemId) {
    const itemName = prompt('Enter new item name:');
    const itemQuantity = prompt('Enter new quantity:');
    const itemCategory = prompt('Enter new category:');
    const itemBrand = prompt('Enter new brand:');
    const itemNotes = prompt('Enter new notes:');

    fetch(`http://3.85.175.115:5005/inventory/edit/${tableName}/${itemId}`, {
        method: 'PUT',
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
            console.log('Item edited successfully');
            fetchStock(tableName);
        } else {
            console.error('Failed to edit item');
        }
    }).catch(error => console.error('Error:', error));
}

async function deleteItem(tableName, itemId) {
    fetch(`http://3.85.175.115:5005/inventory/delete/${tableName}/${itemId}`, {
        method: 'DELETE'
    }).then(response => {
        if (response.ok) {
            console.log('Item deleted successfully');
            fetchStock(tableName);
        } else {
            console.error('Failed to delete item');
        }
    }).catch(error => console.error('Error:', error));
}

fetchStock('ict');

document.getElementById('logout').addEventListener('click', async function(event){
    //window.location.href='login.html';
    event.preventDefault();

    try {
        const response = await fetch('/inventory/logout', {
            method: 'POST',
            headers: {'Content-Type': 'application/json',
                      'Accept': 'application/json'
                     }
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
