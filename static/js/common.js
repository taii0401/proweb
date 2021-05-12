//跳轉頁面
function changeForm(url) {
    if(url != "") {
        location.href = url;
    }
}

//檢查格式是否正確-電子郵件、手機號碼
function checkFormat(type,data) {
    //去除空白
    data = data.trim();
    //回傳訊息
    var msg = "";
    if(type == "email") {
        emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
        if(data.search(emailRule) == -1) {
            msg = "請檢查電子郵件的格式！";
        }
    } else if(type == "phone") {
        var phoneRule = /^(09)[0-9]{8}$/;
        if(!data.match(phoneRule)) {
            msg = "請檢查手機號碼的格式！";
        }
    }
    
    return msg;
}

//送出-帳號
function member_submit(action_type) {
    console.log("aaa");
    $("#form_data").validator();
    /*$('#form_data').validator().on('submit', function(e) {
        if (e.isDefaultPrevented()) { // 未驗證通過 則不處理
        return;
        } else { // 通过后，送出表单
        alert("已送出表單");
        }
        e.preventDefault(); // 防止原始 form 提交表单
    });*/
    
}