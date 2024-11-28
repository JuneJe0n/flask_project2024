function Delete(itemId, button) {
    // Delete the row containing the clicked button (i.e., specific item)
    var row = button.closest('td');
    row.remove();

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/remove_item', true); 
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log('Item removed from cart.');
        } else {
            console.log('Error removing item from cart.');
        }
    };
    xhr.send(JSON.stringify({ itemId: itemId }));
}
