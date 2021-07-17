from django.db import models
from django.shortcuts import render,redirect
#JSON
from django.http import JsonResponse
#搜尋條件-OR
from django.db.models import Q
#使用者權限
from django.contrib.auth.models import User
from django.contrib import auth
#使用者資料、檔案資料
from user.models import proweb_code,proweb_file,proweb_file_data,proweb_user
#商品資料
from product.models import proweb_product

import datetime

######################################## 共用函式 start ########################################
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

#取得檔案
def getFile(conds={},return_col=""):
    data = {}
    #依搜尋條件取得檔案
    file_datas = proweb_file.objects.filter(**conds).values()
    for file_data in file_datas:
        #file_id
        file_id = 0
        if "id" in file_data and file_data["id"] > 0:
            file_id = file_data["id"]

            #回傳資料
            if return_col != "":
                if return_col in file_data:
                    data[file_id] = file_data[return_col]
            else:
                data[file_id] = file_data
    #print(data)
    return data
    
#取得檔案資料
def getFileData(conds={},is_detail=False,orderby="file_id"):
    data = {}
    #依搜尋條件取得檔案資料
    file_datas = proweb_file_data.objects.filter(**conds).order_by(orderby).values()
    for file_data in file_datas:
        #file_id
        file_id = 0
        if "file_id" in file_data and file_data["file_id"] > 0:
            file_id = file_data["file_id"]
            data[file_id] = file_data

            if is_detail: #取得檔案詳細資料
                conds_file = {}
                conds_file["id"] = file_id
                file_details = getFile(conds_file)
                for key,val in file_details[file_id].items():
                    if key != "id":
                        data[file_id][key] = val                        
    #print(data)
    return data

#更新檔案資料
def updateFileData(data):
    import os
    error = True
    message = "請確認資料！"
    #建立時間
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conds = {}
    if "data_id" in data and data["data_id"] != "":
        conds["data_id"] = data["data_id"]
    else:
        message = "請確認類別ID！"
    if "data_type" in data and data["data_type"] != "":
        conds["data_type"] = data["data_type"]
    else:
        message = "請確認型態！"
    
    #取得資料內所有file_id
    exist_file_ids = []
    delete_file_ids = []
    all_datas = proweb_file_data.objects.filter(**conds).values()
    for all_data in all_datas:
        if str(all_data["file_id"]) not in data["file_ids"]:
            delete_file_ids.append(all_data["file_id"]) #取得需要刪除的ID
        else:
            exist_file_ids.append(all_data["file_id"]) #取得需要存在的file_id
    #print(exist_file_ids)
    #print(delete_file_ids)

    #刪除資料
    for delete_id in delete_file_ids:
        delete_data = proweb_file_data.objects.get(file_id=delete_id)
        #刪除實際檔案
        get_file_data = proweb_file.objects.get(id=delete_id)
        #檔案名稱
        file_name = get_file_data.file_name
        #檔案儲存路徑
        user_file_path = get_file_data.path
        #檔案實際路徑
        file_path = os.path.join("media",user_file_path,file_name)
        try:
            os.remove(file_path)
            #刪除資料表檔案
            get_file_data.delete()
            delete_data.delete()
        except OSError as e:
            message = e
    
    #新增資料
    if data["data_id"] != "" and data["data_type"] != "" and "file_ids" in data:
        for file_id in data["file_ids"]:
            if int(file_id) not in exist_file_ids: #判斷file_id是否存在
                insert_data = proweb_file_data()
                insert_data.data_id = data["data_id"]
                insert_data.data_type = data["data_type"]
                insert_data.file_id = file_id
                insert_data.create_by = data["post_user_id"]
                insert_data.create_time = now
                insert_data.modify_by = data["post_user_id"]
                insert_data.modify_time = now
                insert_data.save()
        error = False
    else:
        message = "請確認檔案資料！"

    return_data = {"error":error,"message":message}
    #print(return_data)
    return return_data

#取得代碼
def getCode(conds={},return_col=""):
    data = {}
    #依搜尋條件取得代碼資料
    code_datas = proweb_code.objects.filter(**conds).values()
    for code_data in code_datas:
        #id
        code_id = 0
        if "id" in code_data and code_data["id"] > 0:
            code_id = code_data["id"]

            #回傳資料
            if return_col != "":
                if return_col in code_data:
                    data[code_id] = code_data[return_col]
            else:
                data[code_id] = code_data
    #print(data)
    return data

#依類型取得代碼選項
def getCodeOptions(code_type="",is_all=False):
    data = {}
    if is_all:
        data[""] = "全部"

    conds = {}
    conds["types"] = code_type
    conds["is_delete"] = 0
    code_datas = getCode(conds,"cname")
    for key,val in code_datas.items():
        data[key] = val
    
    #print(data)
    return data

#分頁
def getPage(request,cur_page="",datas={}):
    #分頁
    from django.core.paginator import Paginator
    #設定檔
    from django.conf import settings

    page_data = {}
    
    #預設第一頁
    if cur_page == "":
        cur_page = 1

    p = Paginator(datas,settings.GLOBAL_PAGE_NUM)
    #資料總數
    page_data["count"] = p.count
    #總頁數
    page_data["num_pages"] = p.num_pages
    #頁碼的列表
    page_data["page_range"] = p.page_range
    #目前頁數
    page_data["cur_page"] = cur_page
    this_page = p.page(cur_page)
    #是否有前一頁
    if this_page.has_previous():
        #前一頁的頁碼
        page_data["previous_page_number"] = this_page.previous_page_number()
    else:
        page_data["previous_page_number"] = cur_page
    #是否有後一頁
    if this_page.has_next():
        #後一頁的頁碼
        page_data["next_page_number"] = this_page.next_page_number()
    else:
        page_data["next_page_number"] = cur_page
    #目前頁面資料
    page_data["list_data"] = this_page.object_list

    return page_data

#取得最後編號
def getSerial(conds={}):
    serial_num = 0
    try:
        datas = proweb_product.objects.filter(**conds).order_by("-serial_num")[:1]
        for data in datas:
            serial_num = data.serial_num
    except:
        pass

    #print(serial_num)
    return serial_num

######################################## 共用函式 end ########################################



######################################## 頁面 start ########################################
#我的頁面
def my_page(request,short_link=""):
    #排序
    orderby_datas = {}
    orderby_datas["serial"] = "編號 遞增"
    orderby_datas["-serial"] = "編號 遞減"
    orderby_datas["sales"] = "售價 遞增"
    orderby_datas["-sales"] = "售價 遞減"

    #取得目前頁數
    cur_page = 1
    search_get_url = keywords = ""
    orderby = "serial"
    if request.method == "GET":
        if "cur_page" in request.GET and request.GET["cur_page"] != "":
            cur_page = request.GET["cur_page"]
        if "keywords" in request.GET and request.GET["keywords"] != "": #關鍵字
            keywords = request.GET["keywords"].strip()
            search_get_url += ";keywords="+keywords
        if "orderby" in request.GET and request.GET["orderby"] != "": #排序
            orderby = request.GET["orderby"]
            search_get_url += ";orderby="+orderby
    
    if short_link != "":
        try:
            user_data = proweb_user.objects.get(short_link=short_link)
            #取得使用者資料
            if user_data.user_id > 0:
                try:
                    conds = Q()
                    conds_and = Q()
                    conds_and.connector = "AND"
                    conds_and.children.append(("user_id",user_data.user_id))
                    conds_and.children.append(("is_delete",0))
                    conds_and.children.append(("is_display",1))
                    if keywords != "": #關鍵字
                        conds_or = Q()
                        conds_or.connector = "OR"
                        conds_or.children.append(("name__icontains",keywords))
                        conds_or.children.append(("serial__icontains",keywords))
                        conds.add(conds_or,"AND")
                    conds.add(conds_and,"AND")
                    #print(conds)
                    #取得資料
                    all_datas = proweb_product.objects.filter(conds).order_by(orderby).values()
                    #取得分頁
                    page_data = getPage(request,cur_page,all_datas)
                    if "list_data" in page_data:
                        datas = page_data["list_data"]
                        for data in datas:
                            #圖片路徑
                            file_path = ""
                            #取得檔案
                            conds = {}
                            conds["data_id"] = data["id"]
                            conds["data_type"] = "product"
                            file_datas = getFileData(conds,True)
                            for key,val in file_datas.items():
                                if file_path == "":
                                    file_path = "/media/"+val["path"]+"/"+val["file_name"]
                            data["file_path"] = file_path
                        
                except:
                    pass
        except:
            pass
        return render(request,"my_page.html",locals())

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
        if username != "" and password != "":
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
        else:
            #跳至頁面-登入
            return redirect("/user/login")
    elif action_type == "edit_password": #修改密碼
        if username != "" and password != "":
            title_txt = "修改密碼"
            #隱藏欄位
            edit_none = edit_data_none = "none"
            #取得使用者
            try:
                auth_user = User.objects.get(username=username,password=password)
            except:
                pass   
        else:
            #跳至頁面-登入
            return redirect("/user/login")
    return render(request,"user_data.html",locals())

#忘記密碼
def user_forget(request):
    title_txt = "忘記密碼"
    return render(request,"user_forget.html",locals())

######################################## 頁面 end ########################################



######################################## ajax start ########################################
#AJAX-上傳檔案
def ajax_upload(request):
    import os,uuid
    error = True
    message = "請確認資料！"

    #登入帳號
    if "username" in request.session and request.session["username"] != "":
        post_username = request.session["username"]

    #取得使用者ID
    post_user_id = 0
    try:
        auth_user = User.objects.get(username=post_username)
        if auth_user is not None and auth_user.is_active:
            post_user_id = auth_user.id
    except:
        message = "無法取得使用者！"
    #print(post_user_id)

    file_id = 0 #檔案ID
    file_name = "" #檔案名稱
    if post_user_id > 0:
        try:
            #取得檔案
            file = request.FILES["file"]
            #檔案大小
            size = file.size
            #原檔案名稱
            name = file.name
            #print(name)
            #檔案型態
            types = name.split(".")[-1]
            #新檔案名稱
            new_name = uuid.uuid4().hex[:10]+"_"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = "{}.{}".format(new_name,types)
            #print(file_name)

            #檔案儲存路徑
            user_file_path = "files/"+str(post_user_id)
            #file_path = os.path.join(user_file_path,file_name)
            #print(file_path)
            absolute_file_path = os.path.join("media",user_file_path,file_name)
            #取得資料夾名稱
            directory = os.path.dirname(absolute_file_path)
            if not os.path.exists(directory): #檢查資料夾是否存在
                #建立資料夾
                os.makedirs(directory)
            #存入檔案
            with open(absolute_file_path,"wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            #新增檔案資料
            try:
                #取得資料表
                data = proweb_file()
                #檔案資料
                data.name = name
                data.file_name = file_name
                data.path = user_file_path
                data.size = size
                data.types = types
                #儲存
                data.save()
                file_id = data.id
                error = False
            except:
                message = "新增檔案錯誤！"
        except:
            message = "上傳檔案錯誤！"
    

    return_data = {"error":error,"message":message,"file_name":name,"file_id":file_id}
    #print(return_data)
    return JsonResponse(return_data)

#AJAX-刪除上傳檔案
def ajax_upload_delete(request):
    import os
    error = True
    message = "請確認資料！"
    if request.method == "POST":
        if "file_id" in request.POST and int(request.POST["file_id"]) > 0:
            file_id = int(request.POST["file_id"])
            try:
                data = proweb_file.objects.get(id=file_id)
                #檔案名稱
                file_name = data.file_name
                #檔案儲存路徑
                user_file_path = data.path
                #檔案實際路徑
                file_path = os.path.join("media",user_file_path,file_name)
                try:
                    os.remove(file_path)
                    #刪除資料表檔案
                    data.delete()
                    error = False
                except OSError as e:
                    message = e
            except:
                message = "檔案不存在！"

    return_data = {"error":error,"message":message}
    #print(return_data)
    return JsonResponse(return_data)

#AJAX-檢查使用者帳號是否已存在
def ajax_user_exist(request):
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
                User.objects.get(username=post_username,is_active=1)
                message = "帳號已存在！"
            except:
                error = False
                message = "帳號可新增！"

    return_data = {"error":error,"message":message}
    #print(return_data)
    return JsonResponse(return_data)

#AJAX-檢查商品頁面網址是否已存在
def ajax_user_link_exist(request):
    error = True
    message = "請確認資料！"
    if request.method == "POST":
        post_user_id = 0
        #登入帳號
        if "username" in request.session and request.session["username"] != "":
            post_username = request.session["username"]
            
            try:
                auth_user = User.objects.get(username=post_username)
                if auth_user is not None and auth_user.is_active:
                    post_user_id = auth_user.id
            except:
                pass
        
        #商品頁面網址
        post_link = ""
        if "short_link" in request.POST and request.POST["short_link"].strip() != "":
            post_link = request.POST["short_link"].strip()
        else:
            message = "請輸入商品頁面網址！"
            pass
        
        if post_link != "":
            count = 0
            isCount = False
            if post_user_id > 0: #編輯
                try:
                    count = proweb_user.objects.filter(short_link=post_link,is_delete=0).exclude(user_id=post_user_id).count()
                    isCount = True
                except:
                    pass
            else:
                try:
                    count = proweb_user.objects.filter(short_link=post_link,is_delete=0).count()
                    isCount = True
                except:
                    pass 

            if not isCount or count > 0:
                message = "商品頁面網址已存在！"
            else:
                error = False
                message = "商品頁面網址可新增！"

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
