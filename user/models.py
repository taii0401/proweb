from django.db import models

# Create your models here.
class proweb_user(models.Model):
    uuid = models.CharField(max_length=255,default="",null=False)
    username = models.CharField(max_length=150,default="",null=False)
    name = models.CharField(max_length=30,default="",null=False)
    sex = models.IntegerField(default="",null=True)
    birthday = models.DateField(default="",null=True)
    email = models.EmailField(max_length=255,default="",null=True)
    phone = models.CharField(max_length=10,default="",null=True)
    address = models.CharField(max_length=255,default="",null=True)
    is_delete = models.IntegerField(default=0,null=False)
    create_time = models.DateTimeField(default="",null=True)
    modify_time = models.DateTimeField(default="",null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "proweb_user" #定義資料表名稱
    