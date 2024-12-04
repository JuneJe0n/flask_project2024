window.onload = function () {
    const priceElements = document.querySelectorAll('.price'); // 모든 .price 요소 선택

    priceElements.forEach(priceElement => {
        let price = priceElement.textContent.trim();  // 텍스트 가져오기

        // "원"과 쉼표(,) 제거 후 숫자로 변환
        price = price.replace(/[^0-9]/g, '');  // 숫자가 아닌 모든 문자 제거

        // 가격을 천 단위 구분자로 포맷팅
        const formattedPrice = Number(price).toLocaleString();  // 천 단위 구분 기호 추가

        // 수정된 가격을 다시 HTML에 표시
        priceElement.textContent = formattedPrice + "원";
    });
};