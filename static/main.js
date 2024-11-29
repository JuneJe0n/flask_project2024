let optnum = 0;

function addOption(OptionText) {
    if (OptionText.trim() == "") {
        return;  // 빈 값은 무시하고 함수 종료
    }

    const option = document.getElementById("options");

    const optionBox = document.createElement("div");
    optionBox.className = "option-box";
    optionBox.textContent = OptionText;

    const deleteBtn = document.createElement("span");
    deleteBtn.className = "delete-btn";
    deleteBtn.textContent = "×";
    deleteBtn.onclick = function() {
        option.removeChild(optionBox);
        optnum -= 1;
        document.getElementById(`hidden-option${optnum}`).remove();
    };

    const hiddenInput = document.createElement("input");
    hiddenInput.type = "hidden";
    hiddenInput.name = "option[]";  // 서버에서 리스트로 받을 수 있도록 설정
    hiddenInput.value = OptionText;
    hiddenInput.id = `hidden-option${optnum}`;

    // 옵션 div에 삭제 버튼 추가하고 폼에 숨겨진 input 추가
    optionBox.appendChild(deleteBtn);
    option.appendChild(optionBox);
    document.getElementById("option-container").appendChild(hiddenInput);

    optnum += 1;
}

document.getElementById("option-receive").addEventListener("keydown", function(event) {
    if (event.key === "Enter" && this.value.trim() !== "") {
        event.preventDefault();
        addOption(this.value.trim());
        this.value = "";
    }

    if (!optnum) {
        const a = document.getElementById("option-notice");
        a.style.display = 'none';
    }
});


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
