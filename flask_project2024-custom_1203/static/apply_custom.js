function applyCustom() {
    const newname = document.getElementById("name").value;
    const newamount = document.getElementById("amount").value;
    const newsize = document.getElementById("size").value;
    const newcolor = document.getElementById("color").value;

    if (newname && newamount && newsize && newcolor) {
        alert(newname+" 상품의 커스터마이징 요청이 전송되었습니다!");
    } else {
        alert("필수 입력 요소를 입력해주세요!");
    }
}

function openFileDialog(event, boxIndex) {
    // 클릭된 박스가 활성화된 경우에만 파일 선택 창 열기
    if (event.currentTarget.style.pointerEvents !== "none") {
        document.getElementById(`fileInput${boxIndex}`).click();
    }
}

var changed = Array(9).fill(1);

function changeIMG(boxIndex) {
    const fileInput = document.getElementById(`fileInput${boxIndex}`);
    const preview = document.getElementById(`preview${boxIndex}`);
    const plus = document.getElementById(`plus${boxIndex}`);

    if (fileInput.files && fileInput.files[0]) {
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            plus.style.display = 'none';
        };

        reader.readAsDataURL(file);

        const nextBox = document.getElementById(`box${boxIndex + 1}`);
        const nextplus = document.getElementById(`plus${boxIndex + 1}`);
        if (nextBox && changed[boxIndex] == 1) {
            nextBox.style.opacity = "1";
            nextBox.style.pointerEvents = "auto";
            nextplus.style.display = 'block';
            changed[boxIndex] = 0;
        }
    }
}