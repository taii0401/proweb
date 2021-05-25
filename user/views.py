from django.shortcuts import render,redirect
from django.http import JsonResponse
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
            user = proweb_user.objects.get(username=post_username)
            #print(user)
        else:
            message = "請輸入帳號和密碼！"



        """
        #try:
            user = models.proweb_user.objects.get(account=post_account)
            print(user)
            if user.password == post_password:
                request.session["account"] = post_account
                request.session["password"] = post_password
                return redirect("/user/user_data/edit")
        #except:
            #pass
        
        if login_form.is_valid():
            account = request.POST["account"]
            password = request.POST["password"]
            msg = "登入成功"
        else:
            msg = "請檢查帳號密碼！"
        """
    else:
        pass
    
    """
    try:
        if account in request.session:
            request.session["account"] = account
        if password in request.session:
            request.session["password"] = password    
    except:
        pass
    """

    return render(request,"login.html",locals())

#登出
#def logout(request):
    #request.session["account"] = None
    #return redirect("/")

#新增、編輯帳號
def user_data(request,action_type="add"):
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