//跳轉頁面
function changeForm(url) {
    if(url != '') {
        location.href = url;
    }
}

//檢查必填欄位(class對應的欄位,是否不顯示提醒視窗,是否顯示錯誤訊息區)
function checkRequiredClass(classStr,isShowMsg) {
	var class_arr = classStr.split(',');
	var required_num = 0;
	var placeholder = [];
	
	for(var i = 0;i < class_arr.length;i++) {
		var class_name = class_arr[i];
		
		$('.'+class_name).each(function() {
			var data = $(this).val();
			
			if(!data) {
				$(this).css('background-color','#FFCCCC');
				required_num++;
			} else {
				$(this).css('background-color','');
			}
		});
	}
	
	if(required_num > 0) {
		msg = '您有'+required_num+'個必填欄位未選填！';
		if(isShowMsg) {
    		$('#error_msg_div').css('display','');
            $('#error_msg').html(msg);
		} else {
    		$('#error_msg_div').css('display','none');
    		alert(msg);
		}
		return false;
	}
}

//檢查格式是否正確-英文字或數字、登入密碼、確認密碼、電子郵件、手機號碼
function checkFormat(type,data,strLength,isShowMsg) {
    //去除空白
    data = data.trim();
    //回傳訊息
    var msg = '';
    if(type == 'en_number') { //英文字或數字
        var regRule = /^[\d|a-zA-Z]+$/;
        if(!regRule.test(data)) {
            msg = '請確認是否為英文字或數字！';
        }
    } else if(type == 'confirm_password') { //確認密碼
        var password = $('#password').val();
        if(data != password.trim()) {
            msg = '請確認密碼是否一樣！';
        }
    } else if(type == 'email') { //電子郵件
        var emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
        if(data.search(emailRule) == -1) {
            msg = '請檢查電子郵件格式！';
        }
    } else if(type == 'phone') { //手機號碼
        var phoneRule = /^(09)[0-9]{8}$/;
        if(!data.match(phoneRule)) {
            msg = '請檢查手機號碼格式！';
        }
    }
    
    //檢查長度
    if(parseInt(strLength) > 0) {
        if(data.length > parseInt(strLength)) {
            if(msg != '') {
                msg += '、';
            }
            msg += '請檢查長度限制！';
        }
    }
    
    
    if(msg != '') {
        //顯示錯誤訊息
        if(isShowMsg) {
            $('#error_msg_div').css('display','');
            $('#error_msg').html(msg);
            return false;
        } else {
            $('#error_msg_div').css('display','none');
            return msg;
        }
    }
}


//送出-帳號
function member_submit(action_type) {
    //檢查必填
    if(checkRequiredClass('require',true) == false) {
		return false;
	}
	if(action_type == 'add') { //申請
    	//檢查帳號
    	checkFormat('en_number',$('#account').val(),30,true);
	}
	//檢查密碼
	checkFormat('en_number',$('#password').val(),30,true);
	//檢查確認密碼
	checkFormat('confirm_password',$('#confirm_password').val(),0,true);
	//檢查電子郵件
	if($('#email').val() != '') {
    	checkFormat('email',$('#email').val(),0,true);
	}
    //檢查手機號碼
    if($('#phone').val() != '') {
    	checkFormat('phone',$('#phone').val(),0,true);
    }
	
	return false;
}