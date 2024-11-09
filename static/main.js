let optnum = 0;

function addOption() {
    const optionInputs = document.querySelectorAll('input[name="option[]"]');
    optionInputs.forEach(input => {
        if (input.value.trim() !== "") {
            optnum += 1;
            document.getElementById("optnum").innerHTML = "(현재 옵션 수: "+optnum+")";    
            input.value = "";
        }
    });
}

function addItem() {
    const newname = document.getElementById("name").value;
    const newamount = document.getElementById("amount").value;
    const newcategory = document.getElementById("category").value;
    const newprice = document.getElementById("price").value;
    const newinfo = document.getElementById("info").value;

    if (newname && optnum >= 1 && newamount && newprice && newinfo && newcategory) {
        alert(newname+" 상품이 등록되었습니다!");
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

var fixcolorvalue = 1;
var star = 100;

function changecolor(cloverIndex) {
    if (fixcolorvalue == 1) {
        const n = cloverIndex;
        for (var i = 1; i <= n; i++) {
            const clovercolor = document.getElementById(`clover${i}`);
            clovercolor.src = "../static/images/greenclover.png";
        }
        for (var i = n+1; i <= 5 ; i++) {
            const clovercolor = document.getElementById(`clover${i}`);
            clovercolor.src = "../static/images/clover.png";
        }
    }
}

function fixcolor(cloverIndex) {
    fixcolorvalue *= -1;
    star = cloverIndex;
}

function addReview() {
    const opt = document.getElementById("option").value;
    const rev = document.getElementById("info").value;

    if (opt && rev.length >= 20 && star <= 5) {
        alert("리뷰가 등록되었습니다!");
    } else if (opt && star <= 5) {
        alert("리뷰를 20자 이상 입력해주세요!");
    } else {
        alert("필수 입력 요소를 입력해주세요!")
    }
}