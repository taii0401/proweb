from django.urls import path
from . import views

urlpatterns = [
    path('product_list/', views.product_list),                          #商品列表
    #path('product_data/<str:action_type>/', views.product_data),        #新增、編輯商品

    path('ajax_product_data/', views.ajax_product_data),                #檢查新增、編輯、刪除商品
]
