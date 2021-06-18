from django.db import models
from django.shortcuts import render,redirect
#JSON
from django.http import JsonResponse
#使用者權限
from django.contrib.auth.models import User
from django.contrib import auth
#商品資料
from product.models import proweb_code,proweb_product

#from django.db.mode1s import Q

import datetime

# Create your views here.
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
def getCodeOptions(code_type=""):
    data = {}
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

######################################## 頁面 start ########################################
#商品列表
def product_list(request):
    acion = "/product/product_list"
    post_username = post_password = ""
    #登入帳號
    if "username" in request.session and request.session["username"] != "":
        username = request.session["username"]
    #登入密碼
    if "password" in request.session and request.session["password"] != "":
        password = request.session["password"]

    #搜尋條件-類別選項
    code_options = getCodeOptions("product_category")
    """
    for code_id,code_cname in code_options.items():
        if code_id == 1:
            active = "active"
        else:
            active = ""
    """

    #取得代碼名稱
    code_datas = getCode({},"cname")
    #print(code_datas)
    

    #取得目前頁數
    cur_page = 1
    search_get_url = keywords = types = ""
    if request.method == "GET":
        if "cur_page" in request.GET and request.GET["cur_page"] != "":
            cur_page = request.GET["cur_page"]
        if "keywords" in request.GET and request.GET["keywords"] != "": #關鍵字
            keywords = request.GET["keywords"].strip()
            search_get_url += ";keywords="+keywords
        if "types" in request.GET and request.GET["types"] != "": #類別
            types = request.GET["types"]
            search_get_url += ";types="+types
            
    
    try:
        auth_user = User.objects.get(username=username,password=password)
        #取得使用者資料
        if auth_user.id > 0:
            try:
                conds = {}
                conds["user_id"] = auth_user.id
                conds["is_delete"] = 0
                if keywords != "": #關鍵字
                    #contains_list = [Q(name__contains=keywords),Q(serial__icontains=keywords)]
                    #conds["name__contains"] = keywords
                    conds["serial__icontains"] = keywords
                if types != "": #類別
                    conds["types"] = types
                #取得資料
                all_datas = proweb_product.objects.filter(**conds).order_by("serial").values()
                #取得分頁
                page_data = getPage(request,cur_page,all_datas)
                if "list_data" in page_data:
                    datas = page_data["list_data"]
                    for data in datas:
                        #類別名稱
                        types_name = ""
                        if data["types"] in code_datas and code_datas[data["types"]] != "":
                            types_name = code_datas[data["types"]]
            except:
                pass
    except:
        pass
    
    return render(request,"product_list.html",locals())

######################################## 頁面 end ########################################



######################################## ajax start ########################################
#AJAX-新增、編輯、刪除商品
def ajax_product_data(request):
    error = True
    message = "請確認資料！"
    if request.method == "POST":
        import uuid
        #建立時間
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #動作類型(新增、編輯)
        action_type = request.POST["action_type"] if "action_type" in request.POST else ""
        #print(action_type)

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
        
        if post_user_id > 0:
            if action_type == "add": #新增
                pass    
            elif action_type == "edit": #編輯
                pass
            elif action_type == "delete": #刪除
                """
                if "uuid" in request.POST and request.POST["uuid"] != "":
                    #try:
                    data = proweb_product.object.get(uuid=request.POST["uuid"])
                    print(data)
                    data.is_delete = 1
                    data.save()
                    error = False
                    #except:
                        #message = "刪除錯誤！"
                else:
                    message = "無法刪除資料！"
                """
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