from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),                                #登入
    path('logout/', views.logout),                              #登出
    path('user_forget/', views.user_forget),                    #忘記密碼
    path('user_data/<str:action_type>/', views.user_data),      #新增、編輯帳號
    

    path('ajax_user_data/', views.ajax_user_data),              #檢查新增、編輯帳號
    path('ajax_user_exist/', views.ajax_user_exist),            #檢查帳號是否已存在
    path('ajax_user_forget/', views.ajax_user_forget),          #檢查忘記密碼資料
]
