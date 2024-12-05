const select = document.getElementById('option');
const displayElement = document.getElementById('selectedOptions');
const finalPriceElement = document.getElementById('finalPrice');
let finalPrice = parseFloat(finalPriceElement.textContent.replace(/[^0-9]/g, ''));
finalPriceElement.textContent = finalPrice.toLocaleString() + "원";


// 페이지 로드 시 가격 형식 업데이트
window.onload = function () {
    const priceElement = document.getElementById('price');
    let price = priceElement.textContent.trim();
    price = price.replace(/[^0-9]/g, '');
    const formattedPrice = Number(price).toLocaleString();
    priceElement.textContent = formattedPrice + "원";

    updateTotalPrice(); // 총 가격 초기화 및 반영
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
document.addEventListener('input', function (event) {
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

// 구매 버튼 클릭 시 실행될 함수
function buyingItem() {
    const name = document.querySelector('input[name="name"]').value;
    const image = document.querySelector('input[name="image"]').value;
    const discount = document.querySelector('input[name="discount"]').value;
    const seller = document.querySelector('input[name="seller"]').value;
    const totalPrice = calculateTotalPrice();

    // 선택된 옵션과 수량을 JSON 형식으로 변환
    const selectedOption = selectedOptions.map(option => ({
        optionName: option[0],
        quantity: option[1]
    }));

    const buyData = {
        name: name,
        image: image,
        discount: discount,
        seller: seller,
        totalPrice: totalPrice,
        option: selectedOption
    };

    fetch('/buy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(buyData)
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/buy'; // 구매 페이지로 리다이렉트
        } else {
            alert('구매 처리 중 오류가 발생했습니다.');
        }
    })
    .catch(error => console.error('Error:', error));
}


function addToCart() {
    const name = document.querySelector('input[name="name"]').value;
    const image = document.querySelector('input[name="image"]').value;
    const discount = document.querySelector('input[name="discount"]').value;
    const seller = document.querySelector('input[name="seller"]').value;
    const finalPrice = calculateTotalPrice();
    const selectedOptionData = selectedOptions.map(option => ({
        optionName: option[0],
        quantity: option[1]
    }));

    // 장바구니 데이터 생성
    const cartData = {
        name: name,
        image: image,
        price: finalPrice, // 총 금액
        discount: discount,
        option: selectedOptionData, // 옵션 데이터
        quantity: selectedOptionData.reduce((sum, option) => sum + option.quantity, 0) // 전체 수량 계산
    };

    // Flask 서버로 AJAX POST 요청
    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(cartData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 팝업 메시지 표시
                const modal = document.getElementById('cartModal');
                modal.style.display = 'flex';

                // 팝업 확인 버튼 클릭 시 buy.html로 이동
                const confirmButton = document.getElementById('confirmButton');
                confirmButton.addEventListener('click', () => {
                    modal.style.display = 'none';
                    window.location.href = '/buy';
                });
            } else {
                alert(`장바구니 추가 실패: ${data.message}`);
            }
        })
        .catch(error => {
            console.error("Error adding to cart:", error);
            alert("장바구니 추가 중 오류가 발생했습니다.");
        });
}


// 좋아요 표시 및 취소
function showHeart() {
    $.ajax({
        type: 'GET',
        url: '/show_heart/{{name}}/',
        data: {},
        success: function (response) {
            let my_heart = response['my_heart'];
            if (my_heart['interested'] == 'Y') {
                $("#heart").css("color", "red");
                $("#heart").attr("onclick", "unlike()");
            } else {
                $("#heart").css("color", "gray");
                $("#heart").attr("onclick", "like()");
            }
        }
    });
}

function like() {
    $.ajax({
        type: 'POST',
        url: '/like/{{name}}/',
        data: {
            interested: "Y",
            image: $("#center_img").attr("src")
        },
        success: function (response) {
            window.location.reload();
        }
    });
}

function unlike() {
    $.ajax({
        type: 'POST',
        url: '/unlike/{{name}}/',
        data: {
            interested: "N"
        },
        success: function (response) {
            window.location.reload();
        }
    });
}

$(document).ready(function () {
    showHeart();
});
