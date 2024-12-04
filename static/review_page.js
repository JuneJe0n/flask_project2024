function sortBy(order) {
    // 버튼 상태 변경
    const buttons = document.querySelectorAll('.sort-buttons button');
    buttons.forEach(button => button.classList.remove('active'));

    if (order === 'latest') {
        buttons[0].classList.add('active');
    } else if (order === 'best') {
        buttons[1].classList.add('active');
    }

    // 서버에 AJAX 요청으로 정렬 기준 전달
    $.ajax({
        url: window.location.href, // 현재 URL 유지
        type: "GET",
        data: { sort: order }, // 정렬 기준 (latest 또는 best)
        success: function(response) {
            // 서버 응답으로 리뷰 리스트 업데이트
            $(".container").html($(response).find(".container").html());
        },
        error: function(error) {
            console.error("Error fetching sorted reviews:", error);
        }
    });
}
