const select = document.getElementById('option');
const displayElement = document.getElementById('selectedOptions');
const finalPriceElement = document.getElementById('finalPrice');
let finalPrice = parseFloat(finalPriceElement.textContent.replace(/[^0-9]/g, ''));
finalPriceElement.textContent = finalPrice.toLocaleString() + "원";

// 페이지 로드 시 가격 형식 업데이트
window.onload = function() {
    const priceElement = document.getElementById('price');
    let price = priceElement.textContent.trim();
    price = price.replace(/[^0-9]/g, '');
    const formattedPrice = Number(price).toLocaleString();
    priceElement.textContent = formattedPrice + "원";

    updateTotalPrice(); // totalPrice 초기화 및 반영
};

// 총 가격 계산 함수
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

// 총 가격 업데이트 함수
function updateTotalPrice() {
    const totalPrice = calculateTotalPrice();
    const totalPriceElement = document.getElementById('totalPrice');
    if (totalPriceElement) {
        totalPriceElement.textContent = totalPrice.toLocaleString() + "원";
    }
}

// 선택된 옵션과 수량을 저장할 배열
let selectedOptions = [];

// 옵션 업데이트 함수
function updateSelectedOptions() {
    const selectedValue = select.value;
    const selectedText = select.options[select.selectedIndex].text;

    // 이미 선택된 옵션인지 확인 (중복 방지)
    const existingOptions = document.querySelectorAll('.newoptionDiv .optionText');
    let isDuplicate = false;

    existingOptions.forEach(option => {
        if (option.textContent === selectedText) {
            isDuplicate = true;
        }
    });

    if (selectedValue && !isDuplicate) {
        // 새 데이터를 추가
        const newOptionDiv = document.createElement('div');
        newOptionDiv.classList.add('newoptionDiv');

        const template = document.getElementById('optionTemplate');
        const clone = template.content.cloneNode(true);

        clone.querySelector('.optionText').textContent = selectedText;
        displayElement.appendChild(clone);

        // 수량 기본값 1로 초기화
        const quantity = 1;

        // 선택된 옵션과 수량을 이차원 배열 형태로 저장
        selectedOptions.push([selectedText, quantity]);
    }

    updateTotalPrice();
}

// 수량 변경 시 호출
document.addEventListener('input', function(event) {
    if (event.target.classList.contains('quantity-input')) {
        const optionText = event.target.closest('.newoptionDiv').querySelector('.optionText').textContent;
        const quantity = parseInt(event.target.value, 10);

        // 선택된 옵션의 수량 업데이트
        selectedOptions = selectedOptions.map(option =>
            option[0] === optionText ? [option[0], quantity] : option
        );

        updateTotalPrice();
    }
});

// select 요소의 변경 이벤트에 함수 연결
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

// 구매 버튼 클릭 시 실행될 함수
function buyingItem() {
    const name = document.querySelector('input[name="name"]').value;
    const image = document.querySelector('input[name="image"]').value;
    const discount = document.querySelector('input[name="discount"]').value;
    const totalPrice = calculateTotalPrice();

    // 선택된 옵션과 수량을 JSON 형식으로 변환
    const selectedOptionQuery = encodeURIComponent(JSON.stringify(selectedOptions));

    window.location.href = `/buying?name=${encodeURIComponent(name)}&image=${encodeURIComponent(image)}&discount=${encodeURIComponent(discount)}&totalPrice=${totalPrice}&selectedOption=${selectedOptionQuery}`;
}

// 커스터마이징 요청 버튼 클릭 시 실행될 함수
function reqCustomization() {
    const name = document.querySelector('input[name="name"]').value;
    const image = document.querySelector('input[name="image"]').value;
    const price = document.querySelector('input[name="price"]').value;

    window.location.href = `/customizing?name=${encodeURIComponent(name)}&image=${encodeURIComponent(image)}&price=${price}`;
}