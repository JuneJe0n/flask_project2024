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

    if (selectedValue) {
        // 새 데이터를 추가
        const newOptionDiv = document.createElement('div');
        newOptionDiv.classList.add('newoptionDiv');

        const template = document.getElementById('optionTemplate')
        const clone = template.content.cloneNode(true);

        clone.querySelector('.optionText').textContent = selectedText;
        displayElement.appendChild(clone);
    }

    // 가격 업데이트 함수 호출
    updateTotalPrice();
}

function updateTotalPrice() {
    const totalPrice = calculateTotalPrice();
    const totalPriceElement = document.getElementById('totalPrice');

    // 천 단위로 구분하여 표시
    const formattedTotalPrice = totalPrice.toLocaleString();

    totalPriceElement.textContent = `${formattedTotalPrice}원`;
}

// 수량 입력이 변경될 때마다 가격을 업데이트
document.addEventListener('input', function(event) {
    if (event.target.classList.contains('quantity-input')) {
        updateTotalPrice();
    }
});

// select 요소의 변경 이벤트에 함수 연결
select.addEventListener('change', updateSelectedOptions);