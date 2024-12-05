function sortBy(order) {
    const buttons = document.querySelectorAll('.sort-buttons button');

    // 버튼 'active' 클래스 관리
    buttons.forEach(button => button.classList.remove('active'));
    if (order === 'latest') {
        buttons[0].classList.add('active');
    } else if (order === 'best') {
        buttons[1].classList.add('active');
    }

    // 아이템 이름 추출 (현재 페이지 경로에서 가져옴)
    const name = window.location.pathname.split('/').slice(-2, -1)[0];

    // AJAX 요청
    $.ajax({
        url: `/reviews/sort`, // Flask 엔드포인트
        type: 'GET',
        data: { sort: order, name: name }, // 정렬 기준 및 아이템 이름 전달
        success: function (data) {
            // 서버에서 받은 데이터로 컨테이너 업데이트
            const newContainer = $(data).find('.container').html();
            $('.container').html(newContainer);
        },
        error: function (error) {
            console.error('Error fetching sorted reviews:', error);
            alert('리뷰 정렬에 문제가 발생했습니다.');
        }
    });
}
