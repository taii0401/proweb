from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('member_data/<str:action_type>/', views.member_data), #新增、編輯帳號
    path('member_forget/', views.member_forget),

    path('ajax_member_data/', views.ajax_member_data), #檢查新增、編輯帳號
    path('ajax_member_account/', views.ajax_member_account), #檢查帳號是否已存在
    path('ajax_member_forget/', views.ajax_member_forget), #檢查忘記密碼資料
]
