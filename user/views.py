from django.db import models
from django.shortcuts import render,redirect
#JSON
from django.http import JsonResponse
#使用者權限
from django.contrib.auth.models import User
from django.contrib import auth
#使用者資料
from user.models import proweb_user

# Create your views here.
#測試連線
def dblink(request):
    import pymysql
    dbhost = "localhost"
    dbuser = "root"
    dbpass = "root"
    dbname = "proweb"
    dbport = 3306
    try:
    	conn = pymysql.connect(host=dbhost,port=dbport,user=dbuser,password=dbpass,database=dbname)
    	result = "連接資料庫成功"
    except pymysql.Error as e:
    	result = "連接資料庫失敗："+str(e)
    return render(request,"dblink.html",locals())

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
                user = User.objects.get(username=post_username)
                if user.password == post_password:
                    request.session["username"] = user.username
                    request.session["password"] = user.password
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
    del request.session["username"]
    del request.session["password"]
    return redirect("/user/login")

#新增、編輯帳號
def user_data(request,action_type="add"):
    username = password = ""
    #登入帳號
    if "username" in request.session and request.session["username"] != "":
        username = request.session["username"]
    #登入密碼
    if "password" in request.session and request.session["password"] != "":
        password = request.session["password"]
    #若有登入帳號及密碼，並點選註冊，則改為編輯帳號頁面
    if username != "" and password != "":
        action_type = "edit"

    if action_type == "add": #新增
        title_txt = "申請帳號"
        #隱藏按鈕-刪除帳號
        btn_none = "none"
        #性別-預設男
        checked_1 = "checked"
    elif action_type == "edit": #編輯
        title_txt = "修改帳號"
        #不可編輯欄位-帳號
        disabled = "disabled"
    
    return render(request,"user_data.html",locals())

#忘記密碼
def user_forget(request):
    title_txt = "忘記密碼"
    return render(request,"user_forget.html",locals())



######################################## ajax start ########################################
#AJAX-檢查帳號是否已存在
def ajax_user_account(request):
    if request.method == "POST":
        #account = request.POST["account"]
        error = False
        msg = "right"
    else:
        error = True
        msg = "error"
    return_data = {"error":error,"msg":msg}
    #print(return_data)
    return JsonResponse(return_data)

#AJAX-檢查忘記密碼資料
def ajax_user_forget(request):
    if request.method == "POST":
        #account = request.POST["account"]
        error = False
        msg = "right"
    else:
        error = True
        msg = "error"
    return_data = {"error":error,"msg":msg}
    #print(return_data)
    return JsonResponse(return_data)

#AJAX-新增、編輯帳號
def ajax_user_data(request):
    if request.method == "POST":
        #account = request.POST["account"]
        error = False
        msg = "right"
    else:
        error = True
        msg = "error"
    return_data = {"error":error,"msg":msg}
    #print(return_data)
    return JsonResponse(return_data)

######################################## ajax end ########################################