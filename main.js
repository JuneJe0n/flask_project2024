var options = [];
let optnum = 0;

function addOption() {
    const optionInputs = document.querySelectorAll('input[name="option[]"]');
    optionInputs.forEach(input => {
        if (input.value.trim() !== "") {
            options.push(input.value);
            optnum += 1;
            document.getElementById("optnum").innerHTML = "(현재 옵션 수: "+optnum+")";    
            input.value = "";
        }
    });
}


function Item (name, option, amount, category, price, discount, info) {
    this.name = name;
    this.option = option;
    this.amount = amount;
    this.category = category;
    this.price = price;
    this.discount = discount;
    this.info = info;
}

function addItem() {
    const newname = document.querySelector('input[name="name"]');
    const newamount = document.querySelector('input[name="amount"]');
    const newprice = document.querySelector('input[name="price"]');
    const newdiscount = document.querySelector('input[name="discount"]');
    const newinfo = document.querySelector('input[name="info"]');
    const newcategory = document.getElementById("category");

    var newItem = new Item( newname.value, options, newamount.value, newcategory.value, newprice.value, newdiscount.value, newinfo.value);
    alert(newname.value+"상품이 등록되었습니다!");
}

function changecolor() {

}

function fixcolor() {

}