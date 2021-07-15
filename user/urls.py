from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),                                #登入
    path('logout/', views.logout),                              #登出
    path('user_forget/', views.user_forget),                    #忘記密碼
    path('user_data/<str:action_type>/', views.user_data),      #新增、編輯使用者
    path('my_page/<str:short_link>', views.my_page),            #我的頁面
    

    path('ajax_upload/', views.ajax_upload),                    #上傳檔案
    path('ajax_upload_delete/', views.ajax_upload_delete),      #上傳檔案-刪除實際檔案
    path('ajax_user_data/', views.ajax_user_data),              #檢查新增、編輯、刪除使用者
    path('ajax_user_exist/', views.ajax_user_exist),            #檢查使用者帳號是否已存在
    path('ajax_user_link_exist/', views.ajax_user_link_exist),  #檢查商品頁面網址是否已存在
    path('ajax_user_forget/', views.ajax_user_forget),          #檢查忘記密碼資料
]
