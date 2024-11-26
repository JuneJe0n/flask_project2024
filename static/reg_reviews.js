function addReview(event) {
    event.preventDefault();

    const opt = document.getElementById('options').value;
    const rev = document.getElementById('info').value;

    if (opt && rev.length >= 20 && fixcolorvalue == -1) {
        alert('리뷰가 등록되었습니다!');
        document.getElementById('regreview').submit();
    } else if (opt && fixcolorvalue == -1) {
        alert('리뷰를 20자 이상 입력해주세요!');
    } else {
        alert('필수 입력 요소를 입력해주세요!');
    }
}

var fixcolorvalue = 1;
var star = 100;

function changecolor(cloverIndex) {
    if (fixcolorvalue == 1) {
        const n = cloverIndex;
        for (var i = 1; i <= n; i++) {
            const clovercolor = document.getElementById(`clover${i}`);
            clovercolor.src = "/static/images/greenclover.png";
        }
        for (var i = n+1; i <= 5 ; i++) {
            const clovercolor = document.getElementById(`clover${i}`);
            clovercolor.src = "/static/images/clover.png";
        }
    }
}

function fixcolor(cloverIndex) {
    fixcolorvalue *= -1;
    star = cloverIndex;
    if (fixcolorvalue == -1) {
        var clovers = document.getElementById('clovers');
        clovers.value = star;
        clovers.innerHTML = star;
    }
}