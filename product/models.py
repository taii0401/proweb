from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
#代碼表
class proweb_code(models.Model):
    types = models.CharField(max_length=100,default="",null=True)
    code = models.CharField(max_length=30,default="",null=True)
    name = models.CharField(max_length=100,default="",null=True)
    cname = models.CharField(max_length=100,default="",null=True)
    is_delete = models.IntegerField(default=0,null=False)
    is_display = models.IntegerField(default=1,null=False)

    def __str__(self):
        return self.id
    
    class Meta:
        db_table = "proweb_code" #定義資料表名稱

#商品資料表
class proweb_product(models.Model):
    uuid = models.CharField(max_length=50,default="",null=False)
    user_id = models.IntegerField(default=0,null=False)
    types = models.IntegerField(default=0,null=False)
    serial_code = models.CharField(max_length=2,default="",null=True)
    serial_num = models.IntegerField(default=0,null=True)
    serial = models.CharField(max_length=20,default="",null=True)
    name = models.CharField(max_length=255,default="",null=True)
    author = models.CharField(max_length=255,default="",null=True)
    office = models.CharField(max_length=255,default="",null=True)
    publish = models.DateField(default="",null=True,blank=True)
    price = models.IntegerField(default=0,null=False)
    sales = models.IntegerField(default=0,null=False)
    content = RichTextUploadingField()
    category = RichTextUploadingField()
    click = models.IntegerField(default=0,null=False)
    is_delete = models.IntegerField(default=0,null=False)
    is_display = models.IntegerField(default=1,null=False)
    create_time = models.DateTimeField(default="",null=True)
    modify_time = models.DateTimeField(default="",null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "proweb_product" #定義資料表名稱
