function sortBy(order) {
    const buttons = document.querySelectorAll('.sort-buttons button');

    // 버튼 'active' 클래스 관리
    buttons.forEach(button => button.classList.remove('active'));
    if (order === 'latest') {
        buttons[0].classList.add('active');
    } else if (order === 'best') {
        buttons[1].classList.add('active');
    }

    // 리뷰 컨테이너와 리뷰 요소들 선택
    const reviewContainer = document.querySelector('.review-item-container');
    const reviews = Array.from(reviewContainer.children);

    // 정렬 로직
    reviews.sort((a, b) => {
        if (order === 'latest') {
            const dateA = new Date(a.querySelector('.date').textContent.trim());
            const dateB = new Date(b.querySelector('.date').textContent.trim());
            return dateB - dateA; // 최신순 정렬
        } else if (order === 'best') {
            const starA = a.querySelectorAll('.stars img').length;
            const starB = b.querySelectorAll('.stars img').length;
            return starB - starA; // 별점순 정렬
        }
    });

    // 기존 컨테이너를 비우지 않고, 정렬된 요소만 다시 추가
    reviews.forEach(review => reviewContainer.appendChild(review));
}
