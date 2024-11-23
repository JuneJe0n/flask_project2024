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

    // 이미 선택된 옵션인지 확인 (중복 방지)
    const existingOptions = document.querySelectorAll('.newoptionDiv .optionText');
    let isDuplicate = false;

    // 선택한 옵션이 이미 추가된 옵션 목록에 있는지 확인
    existingOptions.forEach(option => {
        if (option.textContent === selectedText) {
            isDuplicate = true;
        }
    });

    if (selectedValue && !isDuplicate) {
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

//하단 이미지 클릭 시 center_img 변경
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


//footer에 iframe 생성
function loadIframe(url, element = null) {
    const iframe = document.getElementById('footer_iframe');
    iframe.src = url;
    iframe.hidden = false;

    iframe.onload = () => {
        const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
        iframe.style.height = iframeDocument.body.scrollHeight + "px";
    }; //iframe 높이 설정

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
