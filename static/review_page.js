function sortBy(order) {
    const buttons = document.querySelectorAll('.sort-buttons button');
    buttons.forEach(button => button.classList.remove('active'));

    if (order === 'latest') {
        buttons[0].classList.add('active');
    } else if (order === 'best') {
        buttons[1].classList.add('active');
    }
}
