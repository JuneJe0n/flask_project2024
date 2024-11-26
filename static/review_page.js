$(document).ready(function () {
    // 페이지 로딩 시 초기화 필요 없음 (showHeart 함수 제거)
});

function sortBy(order) {
    const buttons = document.querySelectorAll('.sort-buttons button');
    buttons.forEach(button => button.classList.remove('active'));

    if (order === 'latest') {
        buttons[0].classList.add('active');
    } else if (order === 'best') {
        buttons[1].classList.add('active');
    }
}

function likeReview(reviewId) {
    console.log('Like button clicked for review ID:', reviewId);  // 콘솔에 로그를 추가해 클릭 확인

    $.ajax({
        url: '/like_review',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ review_id: reviewId }),
        success: function(response) {
            if (response.success) {
                // 좋아요 수 업데이트
                const likeCountElement = $('#like-count-' + reviewId);
                likeCountElement.text(response.new_likes);

                // 하트 아이콘 업데이트
                const heartIcon = $('#heart-icon-' + reviewId);
                if (heartIcon.hasClass('fa-heart-o')) {
                    heartIcon.removeClass('fa-heart-o').addClass('fa-heart liked');
                } else {
                    heartIcon.removeClass('fa-heart').addClass('fa-heart-o');
                }
            } else {
                console.error('Failed to update like:', response.message);
            }
        },
        error: function(error) {
            console.error('Error liking review:', error);
        }
    });
}
