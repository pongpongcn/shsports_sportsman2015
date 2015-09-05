from django.db import models

# Create your models here.

Genders = (
     ('MALE', '男'),
     ('FEMALE', '女'),
    )

MovementTypes = (
        ('20m', '20米跑'),
        ('bal', '后退平衡'),
        ('shh', '侧向跳'),
        ('rb', '躯体'),
    )

class Factor(models.Model):
    gender = models.CharField('性别', max_length=10, choices=Genders)
    month_age = models.IntegerField('月龄')
    movement_type = models.CharField('测试点', max_length=10, choices=MovementTypes)
    mean = models.FloatField('平均值')
    standard_deviation = models.FloatField('标准偏差')

    class Meta:
        verbose_name_plural = "分布因素(Factors)"
    
class Student(models.Model):
    last_name = models.CharField('姓', max_length=5)
    first_name = models.CharField('名', max_length=10)
    gender = models.CharField('性别', max_length=10, choices=Genders)
    dateOfBirth = models.DateField('出生日期')
    schoolName = models.CharField('学校名称', max_length=100)
    className = models.CharField('班级名称', max_length=100)
    height = models.FloatField('身高')
    weight = models.FloatField('体重')

    class Meta:
        verbose_name_plural = "学生信息(Students)"
