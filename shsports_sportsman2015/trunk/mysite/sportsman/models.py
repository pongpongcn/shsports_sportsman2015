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
    def __str__(self):
        return self.last_name + ' ' + self.first_name
    
    class Meta:
        verbose_name_plural = "学生信息(Students)"

class TestRefData(models.Model):
    testing_date = models.DateField('测试日期')
    testing_number = models.IntegerField('测试编号')
    student = models.ForeignKey(Student, verbose_name="测试学生")
    def __str__(self):
        return str(self.testing_date) + '#' + str(self.testing_number)
    
    class Meta:
        verbose_name_plural = "测试原始记录(TestRefDatas)"

class TestRefDataItem(models.Model):
    test_ref_data = models.ForeignKey(TestRefData, verbose_name="测试原始记录")
    movement_type = models.CharField('测试点', max_length=10, choices=MovementTypes)
    key = models.CharField('数据项(第一次, 第二次, ...)', max_length=10)
    value = models.FloatField('数据值')
    
    class Meta:
        verbose_name_plural = "测试原始记录单项数据(TestRefDataItem)"

class TestSummaryData(models.Model):
    student = models.ForeignKey(Student)
    testing_date = models.DateField('测试日期')
    month_age = models.IntegerField('月龄')
    day_age = models.IntegerField('日龄')
    test_ref_data = models.ForeignKey(TestRefData)
    
    class Meta:
        verbose_name_plural = "测试总结(TestSummaryData)"

class TestSummaryDataItem(models.Model):
    test_summary_data = models.ForeignKey(TestSummaryData)
    movement_type = models.CharField('测试点', max_length=10, choices=MovementTypes)
    value = models.FloatField('数据值')
    factor = models.ForeignKey(Factor)
    probability = models.FloatField('概率')
    
    class Meta:
        verbose_name_plural = "测试总结单项数据(TestSummaryDataItem)"

    
    
