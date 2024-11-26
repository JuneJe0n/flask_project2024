const select = document.getElementById('option');
const displayElement = document.getElementById('selectedOptions');
const finalPriceElement = document.getElementById('finalPrice');
let finalPrice = parseFloat(finalPriceElement.textContent);
finalPriceElement.textContent = finalPrice.toLocaleString() + "원";

window.onload = function() {
    const priceElement = document.getElementById('price');
    let price = priceElement.textContent.trim();
    price = price.replace(/[^0-9]/g, '');
    const formattedPrice = Number(price).toLocaleString();
    priceElement.textContent = formattedPrice + "원";
};

function calculateTotalPrice() {
    let totalPrice = 0;
    const quantityInputs = displayElement.querySelectorAll('input[type="number"]');
    quantityInputs.forEach(input => {
        const quantity = parseInt(input.value, 10);
        if (!isNaN(quantity)) {
            totalPrice += quantity * finalPrice;
        }
    });
    return totalPrice;
}

function updateSelectedOptions() {
    const selectedValue = select.value;
    const selectedText = select.options[select.selectedIndex].text;
    const existingOptions = document.querySelectorAll('.newoptionDiv .optionText');
    let isDuplicate = false;
    
    existingOptions.forEach(option => {
        if (option.textContent === selectedText) {
            isDuplicate = true;
        }
    });

    if (selectedValue && !isDuplicate) {
        const newOptionDiv = document.createElement('div');
        newOptionDiv.classList.add('newoptionDiv');
        const template = document.getElementById('optionTemplate');
        const clone = template.content.cloneNode(true);
        clone.querySelector('.optionText').textContent = selectedText;
        displayElement.appendChild(clone);
    }

    updateTotalPrice();
}

const hiddenInput = document.getElementById('hiddenOptionInput');
hiddenInput.value = selectedText;

function updateTotalPrice() {
    const totalPrice = calculateTotalPrice();
    const totalPriceElement = document.getElementById('totalPrice');
    const formattedTotalPrice = totalPrice.toLocaleString();
    totalPriceElement.textContent = `${formattedTotalPrice}원`;
}

document.addEventListener('input', function(event) {
    if (event.target.classList.contains('quantity-input')) {
        updateTotalPrice();
    }
});

select.addEventListener('change', updateSelectedOptions);

function changeCenterImage(thumbnail) {
    const centerImage = document.getElementById('center_img');
    centerImage.src = thumbnail.src;

    if (thumbnail) {
        const thumbnails = document.querySelectorAll('.thumbnail');
        thumbnails.forEach(img => img.classList.remove('active-thumbnail'));
        thumbnail.classList.add('active-thumbnail');
    }
}

window.onload = () => {
    thumbnails[0].classList.add('active-thumbnail');
};

function loadIframe(url, element = null) {
    const iframe = document.getElementById('footer_iframe');
    iframe.src = url;
    iframe.hidden = false;

    iframe.onload = () => {
        const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
        iframe.style.height = iframeDocument.body.scrollHeight + "px";
    };

    if (element) {
        const buttons = document.querySelectorAll('.footer_nav a');
        buttons.forEach(button => button.classList.remove('active'));
        element.classList.add('active');
    }
}

window.onload = () => {
    const defaultButton = document.querySelector('.footer_nav a[href="/review_page"]');
    loadIframe('/detail_info', defaultButton);
};

function submitData(action) {
    const displayElement = document.getElementById('selectedOptions');
    const selectedOptions = Array.from(
        displayElement.querySelectorAll('.newoptionDiv')
    ).map(optionDiv => ({
        option: optionDiv.querySelector('.optionText').textContent,
        quantity: optionDiv.querySelector('.quantity-input').value
    }));

    document.getElementById('selectedOptionInput').value = JSON.stringify(selectedOptions);

    const productData = {
        name: document.getElementById('productName').textContent,
        price: document.getElementById('productPrice').textContent,
        image: document.getElementById('productImage').src
    };
    document.getElementById('productDataInput').value = JSON.stringify(productData);

    const otherData = {
        userId: document.getElementById('userId').value
    };
    document.getElementById('otherDataInput').value = JSON.stringify(otherData);

    const form = document.getElementById('dataForm');

    if (action === 'cart') {
        form.action = "{{ url_for('add_to_cart') }}";
    } else if (action === 'order') {
        form.action = "{{ url_for('order_page') }}";
    } else if (action === 'wishlist') {
        form.action = "{{ url_for('view_likelist') }}";
    }

    form.submit();
}

function addToCart() {
    const newname = document.getElementById("name").value;
    const newamount = document.getElementById("image").value;
    const newprice = document.getElementById("price").value;
    const newinfo = document.getElementById("options").value;

    if (newname && optnum >= 1 && newamount && newprice && newinfo && newcategory) {
        alert(newname+" 가 장바구니에 담겼습니다!");
    } else {
        alert("필수 입력 요소를 선택해주세요!");
    }
}

function reqCustomization() {
    const name = document.querySelector('input[name="name"]').value;
    const image = document.querySelector('input[name="image"]').value;
    const totalPrice = document.querySelector('#totalPrice').value;
    const selectedOption = document.querySelector('#selectedOptionInput').value;

    window.location.href = `/customazing?name=${encodeURIComponent(name)}&image=${encodeURIComponent(image)}&totalPrice=${totalPrice}&selectedOption=${encodeURIComponent(selectedOption)}`;
}

function buyingItem() {
    const name = document.querySelector('input[name="name"]').value;
    const image = document.querySelector('input[name="image"]').value;
    const totalPrice = document.querySelector('#totalPrice').value;
    const selectedOption = document.querySelector('#selectedOptionInput').value;

    window.location.href = `/buying?name=${encodeURIComponent(name)}&image=${encodeURIComponent(image)}&totalPrice=${totalPrice}&selectedOption=${encodeURIComponent(selectedOption)}`;
}