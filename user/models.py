from django.db import models


# Create your models here.
#使用者資料表
class proweb_user(models.Model):
    uuid = models.CharField(max_length=50,default="",null=False)
    user_id = models.IntegerField(default=0,null=False,unique=True)
    short_link = models.CharField(max_length=100,default="",null=True)
    name = models.CharField(max_length=30,default="",null=True)
    sex = models.IntegerField(default=1,null=True)
    birthday = models.DateField(default="",null=True,blank=True)
    phone = models.CharField(max_length=10,default="",null=True)
    address = models.CharField(max_length=255,default="",null=True)
    file_id = models.IntegerField(default=0,null=False)
    is_delete = models.IntegerField(default=0,null=False)
    create_time = models.DateTimeField(default="",null=True)
    modify_time = models.DateTimeField(default="",null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "proweb_user" #定義資料表名稱

#上傳檔案資料表
class proweb_file(models.Model):
    name = models.CharField(max_length=255,default="",null=True)
    file_name = models.CharField(max_length=255,default="",unique=True)
    path = models.CharField(max_length=255,default="",null=True)
    size = models.CharField(max_length=30,default="",null=True)
    types = models.CharField(max_length=30,default="",null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "proweb_file" #定義資料表名稱

#檔案資訊資料表
class proweb_file_data(models.Model):
    data_id = models.IntegerField(default=0,null=False)
    data_type = models.CharField(max_length=100,default="",null=True)
    file_id = models.IntegerField(default=0,null=False)
    create_by = models.IntegerField(default=0,null=False)
    create_time = models.DateTimeField(default="",null=True)
    modify_by = models.IntegerField(default=0,null=False)
    modify_time = models.DateTimeField(default="",null=True)
    
    def __str__(self):
        return self.data_id
    
    class Meta:
        db_table = "proweb_file_data" #定義資料表名稱