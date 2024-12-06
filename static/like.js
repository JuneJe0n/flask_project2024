window.onload = function () {
    const priceElements = document.querySelectorAll('.price');

    priceElements.forEach(priceElement => {
        let price = priceElement.textContent.trim();
        price = price.replace(/[^0-9]/g, ''); // 숫자가 아닌 모든 문자 제거
        if (price) {
            const formattedPrice = Number(price).toLocaleString(); // 천 단위 구분 기호 추가
            priceElement.textContent = formattedPrice + "원"; // 포맷팅된 가격 표시
        }
    });
};
