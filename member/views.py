from django.shortcuts import render
from member.models import proweb_member

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

def login(request):
    return render(request,"login.html",locals())

def member_add(request):
    title_txt = "申請帳號"
    action_type = "add"
    #隱藏按鈕-刪除帳號
    btn_none = "none"
    #性別-預設男
    checked_1 = "checked"
    return render(request,"member.html",locals())

def member_edit(request):
    title_txt = "修改帳號"
    action_type = "edit"
    return render(request,"member.html",locals())