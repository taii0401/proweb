from django.db import models
from django.shortcuts import render,redirect
#JSON
from django.http import JsonResponse
#使用者權限
from django.contrib.auth.models import User
from django.contrib import auth
#使用者資料
from user.models import proweb_user

import datetime

# Create your views here.
#測試連線
def dblink(request,db_name):
    import pymysql
    dbhost = "localhost"
    dbuser = "root"
    dbpass = "root"
    dbname = db_name
    dbport = 3306
    try:
    	conn = pymysql.connect(host=dbhost,port=dbport,user=dbuser,password=dbpass,database=dbname)
    	result = "連接資料庫成功"
    except pymysql.Error as e:
    	result = "連接資料庫失敗："+str(e)
    return render(request,"dblink.html",locals())

#取得數字和字母隨機位數
def getRandom(num):
    import random
    ran_str = ""
    for i in range(0,num): 
        #定義一個隨機範圍，去猜i的值。
        current = random.randint(0,num) 
        if current == i:                                
            #生成一個隨機的數字
            current_code = random.randint(0,9)
        else:                                           
            #生成一個隨機的字母，這裡一定要主義chr（）轉換一下
            current_code = chr(random.randint(65,90))
        ran_str += str(current_code)
    
    return ran_str

######################################## 頁面 start ########################################
#首頁
def index(request):
    username = password = ""
    #登入帳號
    if "username" in request.session and request.session["username"] != "":
        username = request.session["username"]
    #登入密碼
    if "password" in request.session and request.session["password"] != "":
        password = request.session["password"]
    if username != "" and password != "":
        #跳至頁面-使用者資料
        return redirect("/user/user_data/edit")
    else:
        #跳至頁面-登入
        return redirect("/user/login")

#登入
def login(request):
    if request.method == "POST":
        post_username = post_password = ""
        if "username" in request.POST and request.POST["username"].strip() != "":
            post_username = request.POST["username"].strip()
        else:
            message = "請輸入帳號！"
            pass
        if "password" in request.POST and request.POST["password"].strip() != "":
            post_password = request.POST["password"].strip()
        else:
            message = "請輸入密碼！"
            pass
        
        if post_username != "" and post_password != "":
            try:
                auth_user = auth.authenticate(username=post_username,password=post_password)
                if auth_user is not None and auth_user.is_active:
                    #更新登入時間(last_login)
                    auth_user.last_login = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    auth_user.save()
                    #將登入資訊存入session
                    request.session["username"] = auth_user.username
                    request.session["password"] = auth_user.password
                    #跳至頁面-編輯使用者
                    return redirect("/user/user_data/edit")
                else:
                    message = "請確認帳號或密碼！"
            except:
                message = "請確認帳號或密碼！"
        else:
            message = "請輸入帳號和密碼！"
    else:
        pass

    return render(request,"login.html",locals())

#登出
def logout(request):
    #刪除session
    del request.session["username"]
    del request.session["password"]
    #跳至頁面-登入
    return redirect("/user/login")

#新增、編輯使用者
def user_data(request,action_type="add"):
    username = password = ""
    #登入帳號
    if "username" in request.session and request.session["username"] != "":
        username = request.session["username"]
    #登入密碼
    if "password" in request.session and request.session["password"] != "":
        password = request.session["password"]
    #若有登入帳號及密碼，並點選註冊，則改為編輯帳號頁面
    if action_type == "add" and username != "" and password != "":
        action_type = "edit"

    if action_type == "add": #新增
        title_txt = "申請帳號"
        #隱藏按鈕-刪除帳號
        btn_none = "none"
        #性別-預設男
        checked_sex_1 = "checked"
    elif action_type == "edit": #編輯
        title_txt = "會員資料"
        #隱藏欄位
        edit_none = edit_pass_none = "none"
        #隱藏按鈕-刪除帳號
        btn_none = "none"
        #取得使用者
        try:
            auth_user = User.objects.get(username=username,password=password)
            #取得使用者資料
            if auth_user.id > 0:
                try:
                    data = proweb_user.objects.get(user_id=auth_user.id)
                    #性別
                    if data.sex == 2:
                        checked_sex_2 = "checked"
                    else:
                        checked_sex_1 = "checked"
                except:
                    pass
        except:
            pass
    elif action_type == "edit_password": #修改密碼
        title_txt = "修改密碼"
        #隱藏欄位
        edit_none = edit_data_none = "none"
        #取得使用者
        try:
            auth_user = User.objects.get(username=username,password=password)
        except:
            pass   
    return render(request,"user_data.html",locals())

#忘記密碼
def user_forget(request):
    title_txt = "忘記密碼"
    return render(request,"user_forget.html",locals())

######################################## 頁面 end ########################################



######################################## ajax start ########################################
#AJAX-檢查使用者帳號是否已存在
def ajax_user_exist(request):
    error = True
    message = "請確認資料！"
    if request.method == "POST":
        post_username = post_email = ""
        if "username" in request.POST and request.POST["username"].strip() != "":
            post_username = request.POST["username"].strip()
        else:
            message = "請輸入帳號！"
            pass
        
        if post_username != "":
            try:
                User.objects.get(username=post_username,is_active=1)
                message = "帳號已存在！"
            except:
                error = False
                message = "帳號可新增！"

    return_data = {"error":error,"message":message}
    #print(return_data)
    return JsonResponse(return_data)

#AJAX-檢查忘記密碼資料
def ajax_user_forget(request):
    error = True
    message = "請確認資料！"
    if request.method == "POST":
        post_username = ""
        if "username" in request.POST and request.POST["username"].strip() != "":
            post_username = request.POST["username"].strip()
        else:
            message = "請輸入帳號！"
            pass
        
        if post_username != "":
            try:
                auth_user = User.objects.get(username=post_username,email=post_username)
                #隨機產生6位數
                ran_str = getRandom(6)
                try:
                    #設定密碼
                    auth_user.set_password(ran_str)
                    #儲存
                    auth_user.save()
                    error = False
                    message = "密碼："+ran_str+"  請重新登入後，至修改密碼更新！"
                except:
                    pass
            except:
                message = "請確認帳號！"

    return_data = {"error":error,"message":message}
    #print(return_data)
    return JsonResponse(return_data)

#AJAX-新增、編輯、刪除使用者
def ajax_user_data(request):
    error = True
    message = "請確認資料！"
    if request.method == "POST":
        import uuid
        #建立時間
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #動作類型(新增、編輯)
        action_type = request.POST["action_type"] if "action_type" in request.POST else ""
        #print(action_type)

        #檢查必填欄位
        post_username = post_password = ""
        if action_type == "add":
            if "username" in request.POST and request.POST["username"].strip() != "":
                post_username = request.POST["username"].strip()
            else:
                message = "請輸入帳號！"
                pass
            if "password" in request.POST and request.POST["password"].strip() != "":
                post_password = request.POST["password"].strip()
            else:
                message = "請輸入密碼！"
                pass
        else:
            #登入帳號
            if "username" in request.session and request.session["username"] != "":
                post_username = request.session["username"]
            #登入密碼
            if "password" in request.session and request.session["password"] != "":
                post_password = request.session["password"]
        #print(post_username)
        #print(post_password)
        
        if post_username != "" and post_password != "":
            if action_type == "add": #新增
                try:
                    auth_user = User.objects.create_user(username=post_username,password=post_password,email=post_username)
                    #print(auth_user.id)
                    if auth_user.id > 0:
                        try:
                            #取得資料表
                            data = proweb_user()
                            #使用者資料
                            data.uuid = uuid.uuid4()
                            data.user_id = auth_user.id
                            data.short_link = request.POST["short_link"] if "short_link" in request.POST and request.POST["short_link"] != "" else ""
                            data.name = request.POST["name"] if "name" in request.POST and request.POST["name"] != "" else ""
                            data.sex = request.POST["sex"] if "sex" in request.POST and request.POST["sex"] != "" else "1"
                            data.birthday = request.POST["birthday"] if "birthday" in request.POST and request.POST["birthday"] != "" else "1980-01-01"
                            data.phone = request.POST["phone"] if "phone" in request.POST and request.POST["phone"] != "" else ""
                            data.address = request.POST["address"] if "address" in request.POST and request.POST["address"] != "" else ""
                            data.is_delete = 0
                            data.create_time = now
                            data.modify_time = now
                            #儲存
                            data.save()
                            error = False
                        except:
                            auth_user.delete()
                            message = "新增錯誤！"
                except:
                    pass
            elif action_type == "edit": #編輯-使用者資料
                try:
                    auth_user = User.objects.get(username=post_username,password=post_password)
                    if auth_user is not None and auth_user.is_active:
                        try:
                            #取得使用者資料
                            post_user_id = request.POST["user_id"] if "user_id" in request.POST else ""
                            data = proweb_user.objects.get(user_id=post_user_id)
                            #使用者資料
                            data.short_link = request.POST["short_link"] if "short_link" in request.POST and request.POST["short_link"] != "" else ""
                            data.name = request.POST["name"] if "name" in request.POST and request.POST["name"] != "" else ""
                            data.sex = request.POST["sex"] if "sex" in request.POST and request.POST["sex"] != "" else "1"
                            data.birthday = request.POST["birthday"] if "birthday" in request.POST and request.POST["birthday"] != "" else "1980-01-01"
                            data.phone = request.POST["phone"] if "phone" in request.POST and request.POST["phone"] != "" else ""
                            data.address = request.POST["address"] if "address" in request.POST and request.POST["address"] != "" else ""
                            data.modify_time = now
                            #儲存
                            data.save()
                            error = False
                        except:
                            message = "更新錯誤！"
                except:
                    pass
            elif action_type == "edit_password": #編輯-密碼
                try:
                    auth_user = User.objects.get(username=post_username,password=post_password)
                    if auth_user is not None and auth_user.is_active:
                        if "password" in request.POST and auth_user.password != request.POST["password"]:
                            try:
                                #設定密碼
                                auth_user.set_password(request.POST["password"])
                                #儲存
                                auth_user.save()
                                error = False
                            except:
                                message = "更新密碼錯誤！"
                        else:
                            message = "密碼尚未修改！"
                except:
                    pass
            elif action_type == "delete": #刪除
                try:
                    auth_user = User.objects.get(username=post_username,password=post_password)
                    if auth_user is not None and auth_user.is_active:
                        auth_user.is_active = 0
                        auth_user.save()
                        try:
                            #取得使用者資料
                            post_user_id = request.POST["user_id"] if "user_id" in request.POST else ""
                            data = proweb_user.objects.get(user_id=post_user_id)
                            #使用者資料
                            data.is_delete = 1
                            #儲存
                            data.save()
                            error = False
                        except:
                            message = "刪除錯誤！"
                except:
                    pass
    else:
        message = "請確認帳號、密碼和電子郵件！"

    return_data = {"error":error,"message":message}
    #print(return_data)
    return JsonResponse(return_data)

######################################## ajax end ########################################
