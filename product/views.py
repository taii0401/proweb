from django.db import models
from django.shortcuts import render,redirect
#JSON
from django.http import JsonResponse
#使用者權限
from django.contrib.auth.models import User
from django.contrib import auth
#商品資料
from product.models import proweb_code,proweb_product


# Create your views here.
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

    #取得代碼名稱
    conds = {}
    conds["type"] = "product_category"
    code_data = getCode(conds,"cname")
    #print(code_data)

    #取得目前頁數
    cur_page = 1
    if request.method == "GET":
        if "cur_page" in request.GET and request.GET["cur_page"] != "":
            cur_page = request.GET["cur_page"]
    
    try:
        auth_user = User.objects.get(username=username,password=password)
        #取得使用者資料
        if auth_user.id > 0:
            try:
                pro_conds = {}
                pro_conds["user_id"] = auth_user.id
                pro_conds["name__contains"] = "Python"
                #取得資料
                all_datas = proweb_product.objects.filter(**pro_conds).order_by("serial").values()
                #取得分頁
                page_data = getPage(request,cur_page,all_datas)
                if "list_data" in page_data:
                    datas = page_data["list_data"]
                    for data in datas:
                        #類別名稱
                        type_name = ""
                        if data["type"] in code_data and code_data[data["type"]] != "":
                            type_name = code_data[data["type"]]
            except:
                pass
    except:
        pass
    
    return render(request,"product_list.html",locals())

