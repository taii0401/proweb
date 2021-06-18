//取得Cookie
function getCookie(name) {
    var cookieValue = null;
    if(document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for(var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if(cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//跳轉頁面
function changeForm(url) {
    if(url != '') {
        location.href = url;
    }
}

//依搜尋條件產生URL
function getSearchUrl(path,is_return=false) {
    var url = path;

    i = 0;
    $('.search_input_data').each(function() {
        input_id = this.id
        input_value = $(this).val();
        if(input_id != "" && input_value != "") {
            if(i == 0) {
                url += '?';
            } else {
                url += ';';
            }
            url += input_id+'='+input_value;
            i++;
        }
    });

    //console.log(url);
    if(is_return) { //回傳URL
        return url;
    } else {
        changeForm(url);
    }
}

//全選
function checkAll() {
    if($('#check_all').prop('checked')) {
        $('.check_list').prop('checked',true);
    } else {
        $('.check_list').prop('checked',false);           
    }
	
	$('.check_list').each(function(i) {
        //console.log(this.value);
        checkId(this.value);
    });
}

//勾選
var checkboxId = new Array();
function checkId(id) {
	var check = $('#checkbox_'+id).prop('checked');
	if(check) {
		checkboxId.push(id);
	} else {
		removeArray(checkboxId, id);
	}
	
	$('#check_list').val(checkboxId);
	//console.log("checkboxId:"+checkboxId);

    if(checkboxId != '') {
        $('.check_btn').css('display','');
    } else {
        $('.check_btn').css('display','none');
    }
}

//移除陣列元素
function removeArray(arr) {
	var what, a = arguments, L = a.length, ax;
	while(L > 1 && arr.length) {
		what = a[--L];
		while((ax= arr.indexOf(what)) !== -1) {
			arr.splice(ax, 1);
		}
	}
	return arr;
}

//檢查必填欄位(class對應的欄位,是否顯示錯誤訊息區)
function checkRequiredClass(classStr,isShowMsg) {
	var class_arr = classStr.split(',');
	var required_num = 0;
	
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
		message = '您有'+required_num+'個必填欄位未選填！';
		showMsg('msg_error',message,isShowMsg);
        return false;
	}
}

//檢查格式是否正確-英文字或數字、登入密碼、確認密碼、電子郵件、手機號碼
function checkFormat(type,data,strLength,isShowMsg) {
    //去除空白
    data = data.trim();
    //回傳訊息
    var message = '';
    if(type == 'en_number') { //英文字或數字
        var regRule = /^[\d|a-zA-Z]+$/;
        if(!regRule.test(data)) {
            message = '請確認是否為英文字或數字！';
        }
    } else if(type == 'confirm_password') { //確認密碼
        var password = $('#password').val();
        if(data != password.trim()) {
            message = '請確認密碼是否一樣！';
        }
    } else if(type == 'email') { //電子郵件
        var emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
        if(data.search(emailRule) == -1) {
            message = '請檢查電子郵件格式！';
        }
    } else if(type == 'phone') { //手機號碼
        var phoneRule = /^(09)[0-9]{8}$/;
        if(!data.match(phoneRule)) {
            message = '請檢查手機號碼格式！';
        }
    }
    
    //檢查長度
    if(parseInt(strLength) > 0) {
        if(data.length > parseInt(strLength)) {
            if(message != '') {
                message += '、';
            }
            message += '請檢查長度限制！';
        }
    }
    
    
    if(message != '') {
        showMsg('msg_error',message,isShowMsg);
        return false;
    }
}

//顯示訊息
function showMsg(div_msg,message,isShowMsg) {
    if(message != '') {
        //顯示錯誤訊息
        if(isShowMsg) {
            $('#'+div_msg).css('display','');
            $('#'+div_msg).html(message);
        } else {
            $('#'+div_msg).css('display','none');
            alert(message);
        }
    }
}

//檢查帳號是否存在
function userExist(username) {
    //取得csrf_token
    var csrf_token = getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        url: '/user/ajax_user_exist/',
        dataType: 'json',
        data: {csrfmiddlewaretoken : csrf_token,username : username},
        error: function(xhr) {
            //console.log(xhr);
            alert('傳送錯誤！');
            return false;
        },
        success: function(response) {
            //console.log(response);
            if(response.error == false) {
                showMsg('msg_success',response.message,true);
                return true;
            } else if(response.error == true) {
                showMsg('msg_error',response.message,true);
                return false;
            } else {
                alert('傳送錯誤！');
                return false;
            }
        }
    });
}

//忘記密碼
function userForget() {
    //檢查必填
    if(checkRequiredClass('require',true) == false) {
		return false;
	}

    $.ajax({
        type: 'POST',
        url: '/user/ajax_user_forget/',
        dataType: 'json',
        data: $('#form_data').serialize(),
        error: function(xhr) {
            //console.log(xhr);
            alert('傳送錯誤！');
            return false;
        },
        success: function(response) {
            //console.log(response);
            if(response.error == false) {
                $('#msg_error').css('display','none');
                showMsg('msg_success',response.message,true);
                return false;
            } else if(response.error == true) {
                $('#msg_success').css('display','none');
                showMsg('msg_error',response.message,true);
                return false;
            } else {
                alert('傳送錯誤！');
                return false;
            }
        }
    });
}

//送出-使用者資料
function userSubmit(action_type) {
    $('#action_type').val(action_type);
    //檢查必填
    if(checkRequiredClass('require',true) == false) {
		return false;
	}
	if(action_type == 'add') { //新增
        //檢查登入帳號(電子郵件)
        if(checkFormat('email',$('#username').val(),128,true) == false) {
            return false;
        }
        //檢查登入帳號(電子郵件)是否存在
        if(userExist($('#username').val()) == false) {
            return false;
        }
        //檢查密碼
        if(checkFormat('en_number',$('#password').val(),0,true) == false) {
            return false;
        }
        //檢查確認密碼
        if(checkFormat('confirm_password',$('#confirm_password').val(),0,true) == false) {
            return false;
        }
	} else if(action_type == 'edit') { //編輯
	    //檢查商品頁面網址
        if($('#short_link').val() != '') {
            if(checkFormat('en_number',$('#short_link').val(),100,true) == false) {
                return false;
            }
        }
        //檢查手機號碼
        if($('#phone').val() != '') {
            if(checkFormat('phone',$('#phone').val(),0,true) == false) {
                return false;
            }
        }
    } else if(action_type == 'delete') { //刪除
        var yes = confirm("你確定要刪除嗎？");
        if(!yes) {
            return false;
        }
    }

    $('.form-control').attr('disabled',false);

    $.ajax({
        type: 'POST',
        url: '/user/ajax_user_data/',
        dataType: 'json',
        data: $('#form_data').serialize(),
        error: function(xhr) {
            //console.log(xhr);
            alert('傳送錯誤！');
            return false;
        },
        success: function(response) {
            //console.log(response);
            if(response.error == false) {
                if(action_type == 'add') { //新增
                    alert("申請成功！");
                    changeForm('/user/login');
                } else if(action_type == 'edit') { //編輯-使用者資料
                    changeForm('/user/user_data/edit');
                } else if(action_type == 'edit_password') { //編輯-密碼
                    alert("修改成功，請重新登入！");
                    changeForm('/user/logout');
                } else if(action_type == 'delete') { //刪除
                    alert("刪除成功！");
                    changeForm('/user/logout');
                }
            } else if(response.error == true) {
                showMsg('msg_error',response.message,true);
                return false;
            } else {
                alert('傳送錯誤！');
                return false;
            }
        }
    });
}

//送出-商品資料
function productSubmit(action_type) {
    $('#action_type').val(action_type);
    //檢查必填
    if(checkRequiredClass('require',true) == false) {
		return false;
	}
	if(action_type == 'add') { //新增
        
	} else if(action_type == 'edit') { //編輯
	    
    } else if(action_type == 'delete' || action_type == 'delete_list') { //刪除、刪除-列表勾選多筆
        var yes = confirm("你確定要刪除嗎？");
        if(!yes) {
            return false;
        }
    }

    $('.form-control').attr('disabled',false);
    
    $.ajax({
        type: 'POST',
        url: '/product/ajax_product_data/',
        dataType: 'json',
        data: $('#form_data').serialize(),
        error: function(xhr) {
            //console.log(xhr);
            alert('傳送錯誤！');
            return false;
        },
        success: function(response) {
            //console.log(response);
            if(response.error == false) {
                if(action_type == 'add') { //新增
                    alert("新增成功！");
                } else if(action_type == 'edit') { //編輯
                    alert("編輯成功！");
                } else if(action_type == 'delete' || action_type == 'delete_list') { //刪除、刪除-列表勾選多筆
                    alert("刪除成功！");
                }
                changeForm('/product/product_list');
            } else if(response.error == true) {
                showMsg('msg_error',response.message,true);
                return false;
            } else {
                alert('傳送錯誤！');
                return false;
            }
        }
    });
}