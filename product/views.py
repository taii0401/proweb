from django.db import models
from django.shortcuts import render,redirect
#JSON
from django.http import JsonResponse
#搜尋條件-OR
from django.db.models import Q
#使用者權限
from django.contrib.auth.models import User
from django.contrib import auth
#商品資料
from product.models import proweb_product
#取得共用函式
from user.views import *

import datetime


######################################## 頁面 start ########################################
#商品列表
def product_list(request):
    acion = "/product/product_list"
    username = password = "";
    #登入帳號
    if "username" in request.session and request.session["username"] != "":
        username = request.session["username"]
    #登入密碼
    if "password" in request.session and request.session["password"] != "":
        password = request.session["password"]

    if username != "" and password != "":
        #搜尋條件-類別選項
        code_options = getCodeOptions("product_category",True)

        #取得代碼名稱
        code_datas = getCode({},"cname")
        #print(code_datas)

        #是否顯示
        is_display_datas = {}
        is_display_datas[""] = "全部"
        is_display_datas[1] = "是"
        is_display_datas[0] = "否"

        #排序
        orderby_datas = {}
        orderby_datas["serial"] = "編號 遞增"
        orderby_datas["-serial"] = "編號 遞減"
        orderby_datas["price"] = "價錢 遞增"
        orderby_datas["-price"] = "價錢 遞減"

        #取得目前頁數
        cur_page = 1
        search_get_url = keywords = types = is_display = ""
        orderby = "serial"
        if request.method == "GET":
            if "cur_page" in request.GET and request.GET["cur_page"] != "":
                cur_page = request.GET["cur_page"]
            if "keywords" in request.GET and request.GET["keywords"] != "": #關鍵字
                keywords = request.GET["keywords"].strip()
                search_get_url += ";keywords="+keywords
            if "types" in request.GET and request.GET["types"] != "": #類別
                types = int(request.GET["types"])
                search_get_url += ";types="+str(types)
            if "is_display" in request.GET and request.GET["is_display"] != "": #是否顯示
                is_display = int(request.GET["is_display"])
                search_get_url += ";is_display="+str(is_display)
            if "orderby" in request.GET and request.GET["orderby"] != "": #排序
                orderby = request.GET["orderby"]
                search_get_url += ";orderby="+orderby
        
        try:
            auth_user = User.objects.get(username=username,password=password)
            #取得使用者資料
            if auth_user.id > 0:
                try:
                    user_data = proweb_user.objects.get(user_id=auth_user.id)
                except:
                    pass

                try:
                    conds = Q()
                    conds_and = Q()
                    conds_and.connector = "AND"
                    conds_and.children.append(("user_id",auth_user.id))
                    conds_and.children.append(("is_delete",0))
                    if types != "": #類別
                        conds_and.children.append(("types",types))
                    if is_display != "": #是否顯示
                        conds_and.children.append(("is_display",is_display))
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
                            #轉換名稱-類別
                            types_name = ""
                            if data["types"] in code_datas and code_datas[data["types"]] != "":
                                types_name = code_datas[data["types"]]
                            data["types_name"] = types_name
                            #轉換名稱-是否顯示
                            is_display_name = "否"
                            if data["is_display"] == 1:
                                is_display_name = "是"
                            data["is_display_name"] = is_display_name
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
    
        return render(request,"product_list.html",locals())
    else:
        #跳至頁面-登入
        return redirect("/user/login")

#新增、編輯商品
def product_data(request,action_type="add"):
    username = password = ""
    #登入帳號
    if "username" in request.session and request.session["username"] != "":
        username = request.session["username"]
    #登入密碼
    if "password" in request.session and request.session["password"] != "":
        password = request.session["password"]
    if username != "" and password != "":
        try:
            auth_user = User.objects.get(username=username,password=password)
            #取得使用者資料
            if auth_user.id > 0:
                #類別選項
                code_options = getCodeOptions("product_category")
                #目前先預設-書籍
                select_types = 1

                if action_type == "add": #新增
                    title_txt = "新增商品"
                    #隱藏按鈕-刪除商品
                    btn_none = "none"
                    #是否顯示
                    is_display_checked = "checked"
                elif action_type == "edit": #編輯
                    title_txt = "編輯商品"
                    uuid = is_display_checked = ""
                    #取得UUID
                    if request.method == "GET":
                        if "uuid" in request.GET and request.GET["uuid"] != "":
                            uuid = request.GET["uuid"]
                    
                    #依UUID取得資料
                    if uuid != "":
                        try:
                            data = proweb_product.objects.get(uuid=uuid)
                            if data.is_display == 1:
                                is_display_checked = "checked"
                            
                            #取得檔案
                            conds = {}
                            conds["data_id"] = data.id
                            conds["data_type"] = "product"
                            file_datas = getFileData(conds,True)
                        except:
                            pass

        except:
            pass
        return render(request,"product_data.html",locals())
    else:
        #跳至頁面-登入
        return redirect("/user/login")

#檢視商品
def product_data_view(request):
    title_txt = "商品明細"
    uuid = ""
    #取得UUID
    if request.method == "GET":
        if "uuid" in request.GET and request.GET["uuid"] != "":
            uuid = request.GET["uuid"]
        if "short_link" in request.GET and request.GET["short_link"] != "":
            short_link = request.GET["short_link"]

    #依UUID取得資料
    if uuid != "":
        try:
            data = proweb_product.objects.get(uuid=uuid)
            
            #取得檔案
            conds = {}
            conds["data_id"] = data.id
            conds["data_type"] = "product"
            file_datas = getFileData(conds,True)
        except:
            pass

    return render(request,"product_data_view.html",locals())

######################################## 頁面 end ########################################



######################################## ajax start ########################################
#AJAX-新增、編輯、刪除商品
def ajax_product_data(request):
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

    if request.method == "POST":
        import uuid
        #建立時間
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #動作類型(新增、編輯)
        action_type = request.POST["action_type"] if "action_type" in request.POST else ""
        #print(action_type)
        
        if post_user_id > 0:
            if action_type == "add": #新增
                #取得代碼名稱
                code_datas = getCode({},"code")
                #print(code_datas)

                #取得資料表
                data = proweb_product()
                
                #類型
                types = int(request.POST["types"]) if "types" in request.POST and request.POST["types"] != "" else 1
                data.types = types

                #取得最後一筆編號
                conds = {}
                conds["types"] = types
                serial_num = int(getSerial(conds))
                serial_num = serial_num+1
                data.serial_num = serial_num
                #print(data.serial_num)
                #編號
                data.serial = str(code_datas[types])+str(serial_num).zfill(4)
                #print(data.serial)

                #商品資料
                data.uuid = uuid.uuid4()
                data.user_id = post_user_id
                data.name = request.POST["name"] if "name" in request.POST and request.POST["name"] != "" else ""
                data.author = request.POST["author"] if "author" in request.POST and request.POST["author"] != "" else ""
                data.office = request.POST["office"] if "office" in request.POST and request.POST["office"] != "" else ""
                data.publish = request.POST["publish"] if "publish" in request.POST and request.POST["publish"] != "" else datetime.datetime.now().strftime("%Y-%m-%d")
                data.price = request.POST["price"] if "price" in request.POST and request.POST["price"] != "" else 0
                data.sales = request.POST["sales"] if "sales" in request.POST and request.POST["sales"] != "" else data.price
                data.content = request.POST["content"] if "content" in request.POST and request.POST["content"] != "" else ""
                data.category = request.POST["category"] if "category" in request.POST and request.POST["category"] != "" else ""
                data.is_delete = 0
                data.create_time = now
                data.modify_time = now
                #是否顯示
                if request.POST.get("is_display","false") == "on":
                    data.is_display = 1
                else:
                    data.is_display = 0
                #儲存
                data.save()
                data_id = data.id

                #檔案
                file_data = {}
                file_data["data_id"] = data_id
                file_data["data_type"] = "product"
                file_data["file_ids"] = request.POST.getlist("file_id[]")
                file_data["post_user_id"] = post_user_id
                result = updateFileData(file_data)
                if result["error"] == False:
                    error = False   
                    message = data.uuid #回傳uuid
                else:
                    message = result["message"]
                    
            elif action_type == "edit": #編輯
                uuid = request.POST["uuid"] if "uuid" in request.POST else ""
                #取得商品資料
                data = proweb_product.objects.get(uuid=uuid)
                if post_user_id == data.user_id:
                    #商品資料
                    data.name = request.POST["name"] if "name" in request.POST and request.POST["name"] != "" else ""
                    data.types = request.POST["types"] if "types" in request.POST and request.POST["types"] != "" else ""
                    data.author = request.POST["author"] if "author" in request.POST and request.POST["author"] != "" else ""
                    data.office = request.POST["office"] if "office" in request.POST and request.POST["office"] != "" else ""
                    data.publish = request.POST["publish"] if "publish" in request.POST and request.POST["publish"] != "" else datetime.datetime.now().strftime("%Y-%m-%d")
                    data.price = request.POST["price"] if "price" in request.POST and request.POST["price"] != "" else 0
                    data.sales = request.POST["sales"] if "sales" in request.POST and request.POST["sales"] != "" else data.price
                    data.content = request.POST["content"] if "content" in request.POST and request.POST["content"] != "" else ""
                    data.category = request.POST["category"] if "category" in request.POST and request.POST["category"] != "" else ""
                    data.modify_time = now
                    #是否顯示
                    if request.POST.get("is_display","false") == "on":
                        data.is_display = 1
                    else:
                        data.is_display = 0
                    #儲存
                    data.save()
                    data_id = data.id

                    #檔案
                    file_data = {}
                    file_data["data_id"] = data_id
                    file_data["data_type"] = "product"
                    file_data["file_ids"] = request.POST.getlist("file_id[]")
                    file_data["post_user_id"] = post_user_id
                    result = updateFileData(file_data)
                    if result["error"] == False:
                        error = False
                    else:
                        message = result["message"]
                else:
                    message = "沒有編輯權限！"
            elif action_type == "delete": #刪除
                uuid = request.POST["uuid"] if "uuid" in request.POST else ""
                #取得商品資料
                data = proweb_product.objects.get(uuid=uuid)
                if post_user_id == data.user_id:
                    data.is_delete = 1
                    data.save()
                    error = False
                else:
                    message = "沒有刪除權限！"
            elif action_type == "delete_list": #刪除-列表勾選多筆
                if "check_list" in request.POST and request.POST["check_list"] != "":
                    check_list = request.POST["check_list"].split(",")
                    try:
                        proweb_product.objects.filter(uuid__in=check_list).update(is_delete=1,modify_time=now)
                        error = False
                    except:
                        message = "刪除錯誤！"

    else:
        message = "請確認商品資料！"
    
    return_data = {"error":error,"message":message}
    #print(return_data)
    return JsonResponse(return_data)

######################################## ajax end ########################################

