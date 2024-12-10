// 이미지 데이터를 가져오기
const dataElement = document.getElementById('image-data');
const images = JSON.parse(dataElement.dataset.images); // data-images 속성 읽기
let currentIndex = 0;
let maxIndex = images.length;

// DOM 요소 가져오기
const imgElement = document.getElementById('prev-img');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');

// 이전 버튼 클릭 이벤트
prevBtn.addEventListener('click', () => {
    if (currentIndex == 1) {
        prevBtn.style.display = "none";
    } else if (currentIndex == maxIndex - 1) {
        nextBtn.style.display = "block";
    }

    if (currentIndex > 0) {
        currentIndex = currentIndex - 1;
        imgElement.src = `${images[currentIndex]}`;
    }
});

// 다음 버튼 클릭 이벤트
nextBtn.addEventListener('click', () => {
    if (currentIndex == 0) {
        prevBtn.style.display = "block";
    } else if (currentIndex == maxIndex - 2) {
        nextBtn.style.display = "none";
    }

    if (currentIndex < maxIndex - 1) {
        currentIndex = currentIndex + 1;
        imgElement.src = `${images[currentIndex]}`;
    }
});