from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.

Genders = (
     ('MALE', '男'),
     ('FEMALE', '女'),
    )

MovementTypes = (
        ('20m', '20米冲刺跑'),
        ('bal', '平衡'),
        ('shh', '侧向跳'),
        ('rb', '直身前驱'),
        ('ball', '投掷'),
        ('ls', '俯卧撑'),
        ('su', '仰卧起坐'),
        ('sws', '跳远'),
        ('lauf', '六分跑'),
        ('slauf', '星形跑'),
    )

class SequenceNumber(models.Model):
    code = models.CharField('代码', max_length=100, unique=True)
    value = models.BigIntegerField('值（当前）')
    prefix = models.CharField('前缀', max_length=100, null=True, blank=True)
    suffix = models.CharField('后缀', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "序列编号"
        verbose_name_plural = "序列编号"

def GetNextSequenceNumber(code):
    sequenceNumberQuery = SequenceNumber.objects.filter(code=code)
    if sequenceNumberQuery.exists():
        sequenceNumber = sequenceNumberQuery[0]
        sequenceNumber.value += 1
    else:
        startValue = 1
        sequenceNumber = SequenceNumber(code=code, value=startValue)
    sequenceNumber.save()
    return sequenceNumber

def GetNextSequenceNumberValue(code):
    sequenceNumber = GetNextSequenceNumber(code)
    return sequenceNumber.value

class District(models.Model):
    name = models.CharField('名称', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "区县"
        verbose_name_plural = "区县"

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    district = models.ForeignKey(District, verbose_name="所属区县", null=True, blank=True)

    def __str__(self):
        return str(self.user) + '的用户资料'

    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

class School(models.Model):
    name = models.CharField('名称', max_length=100)
    universalName = models.CharField('名称（英文）', max_length=100)
    district = models.ForeignKey(District, verbose_name="所属区县", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "学校"
        verbose_name_plural = "学校"

class SchoolClass(models.Model):
    school = models.ForeignKey(School, verbose_name="学校")
    name = models.CharField('名称', max_length=100)
    universalName = models.CharField('名称（英文）', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = "班级"

class StandardParameter(models.Model):
    version = models.CharField('版本', max_length=100)
    gender = models.CharField('性别', max_length=10, choices=Genders)
    age = models.IntegerField('年龄')
    percentile = models.DecimalField('百分位', max_digits=3, decimal_places=1)
    original_score_20m = models.DecimalField('20米跑', max_digits=3, decimal_places=2)
    original_score_bal = models.IntegerField('后退平衡')
    original_score_shh = models.IntegerField('侧向跳')
    original_score_rb = models.DecimalField('立位体前屈', max_digits=3, decimal_places=1)
    original_score_ls = models.IntegerField('俯卧撑')
    original_score_su = models.IntegerField('仰卧起坐')
    original_score_sws = models.DecimalField('立定跳远', max_digits=4, decimal_places=1)
    original_score_ball = models.DecimalField('投掷球', max_digits=3, decimal_places=1)
    original_score_lauf = models.IntegerField('6分钟跑')

    class Meta:
        verbose_name = "标准值表"
        verbose_name_plural = "标准值表"

class Factor(models.Model):
    version = models.CharField('版本', max_length=100)
    month_age = models.IntegerField('月龄')
    gender = models.CharField('性别', max_length=10, choices=Genders)
    mean_20m = models.DecimalField('20米跑平均值', max_digits=10, decimal_places=2)
    standard_deviation_20m = models.DecimalField('20米跑标准偏差', max_digits=10, decimal_places=4)
    mean_bal = models.DecimalField('后退平衡平均值', max_digits=10, decimal_places=2)
    standard_deviation_bal = models.DecimalField('后退平衡标准偏差', max_digits=10, decimal_places=4)
    mean_shh = models.DecimalField('侧向跳平均值', max_digits=10, decimal_places=2)
    standard_deviation_shh = models.DecimalField('侧向跳标准偏差', max_digits=10, decimal_places=4)
    mean_rb = models.DecimalField('立位体前屈平均值', max_digits=10, decimal_places=2)
    standard_deviation_rb = models.DecimalField('立位体前屈标准偏差', max_digits=10, decimal_places=4)
    mean_ls = models.DecimalField('俯卧撑平均值', max_digits=10, decimal_places=2)
    standard_deviation_ls = models.DecimalField('俯卧撑标准偏差', max_digits=10, decimal_places=4)
    mean_su = models.DecimalField('仰卧起坐平均值', max_digits=10, decimal_places=2)
    standard_deviation_su = models.DecimalField('仰卧起坐标准偏差', max_digits=10, decimal_places=4)
    mean_sws = models.DecimalField('立定跳远平均值', max_digits=10, decimal_places=2)
    standard_deviation_sws = models.DecimalField('立定跳远标准偏差', max_digits=10, decimal_places=4)
    mean_ball = models.DecimalField('投掷球平均值', max_digits=10, decimal_places=2)
    standard_deviation_ball = models.DecimalField('投掷球标准偏差', max_digits=10, decimal_places=4)
    mean_lauf = models.DecimalField('6分钟跑平均值', max_digits=10, decimal_places=2)
    standard_deviation_lauf = models.DecimalField('6分钟跑标准偏差', max_digits=10, decimal_places=4)
    
    class Meta:
        verbose_name = "分布因素"
        verbose_name_plural = "分布因素"
    
class Student(models.Model):
    noOfStudentStatus = models.CharField('学籍号', max_length=255, null=True, blank=True)
    schoolClass = models.ForeignKey(SchoolClass, verbose_name="班级")
    firstName = models.CharField('名', max_length=255)
    lastName = models.CharField('姓', max_length=255)
    universalFirstName = models.CharField('名（英文）', max_length=255, null=True, blank=True)
    universalLastName = models.CharField('姓（英文）', max_length=255, null=True, blank=True)
    gender = models.CharField('性别', max_length=255, choices=Genders, null=True, blank=True)
    dateOfBirth = models.DateField('出生日期', null=True, blank=True)
    dateOfTesting = models.DateField('测试日期', null=True, blank=True)
    number = models.IntegerField('测试编号', null=True, blank=True)
    questionary = models.IntegerField('问卷编号', null=True, blank=True)
    street = models.CharField('路（地址）', max_length=255, null=True, blank=True)
    housenumber = models.CharField('弄（地址）', max_length=255, null=True, blank=True)
    addition = models.CharField('号（地址）', max_length=255, null=True, blank=True)
    zip = models.CharField('邮政编码（地址）', max_length=255, null=True, blank=True)
    city = models.CharField('城市（地址）', max_length=255, null=True, blank=True)
    addressClearance = models.BooleanField('地址Clearance', default=False)
    
    #Examination results

    weight = models.DecimalField('体重（公斤）', max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.PositiveSmallIntegerField('身高（厘米）', null=True, blank=True)
    
    #20米跑
    e_20m_1 = models.DecimalField('测试成绩 20米跑 第一次（秒）', max_digits=4, decimal_places=2, null=True, blank=True)
    e_20m_2 = models.DecimalField('测试成绩 20米跑 第二次（秒）', max_digits=4, decimal_places=2, null=True, blank=True)
    def _get_e_20m(self):
        values = (self.e_20m_1, self.e_20m_2)
        if all(value != None for value in values):
            return min(values)
        else:
            return None
    e_20m = property(_get_e_20m, None, None, '测试成绩 20米跑（秒）')
    
    #后退平衡
    e_bal30_1 = models.PositiveSmallIntegerField('测试成绩 后退平衡 3.0厘米 第一次（次数）', null=True, blank=True)
    e_bal30_2 = models.PositiveSmallIntegerField('测试成绩 后退平衡 3.0厘米 第二次（次数）', null=True, blank=True)
    e_bal45_1 = models.PositiveSmallIntegerField('测试成绩 后退平衡 4.5厘米 第一次（次数）', null=True, blank=True)
    e_bal45_2 = models.PositiveSmallIntegerField('测试成绩 后退平衡 4.5厘米 第二次（次数）', null=True, blank=True)
    e_bal60_1 = models.PositiveSmallIntegerField('测试成绩 后退平衡 6.0厘米 第一次（次数）', null=True, blank=True)
    e_bal60_2 = models.PositiveSmallIntegerField('测试成绩 后退平衡 6.0厘米 第二次（次数）', null=True, blank=True)
    def _get_e_bal(self):
        values = (self.e_bal60_1, self.e_bal60_2, self.e_bal45_1, self.e_bal45_2, self.e_bal30_1, self.e_bal30_2)
        if all(value != None for value in values):
            return sum(values)
        else:
            return None
    e_bal = property(_get_e_bal, None, None, '测试成绩 后退平衡（次数）')
    
    #投掷球
    e_ball_1 = models.DecimalField('测试成绩 投掷球 第一次（米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_ball_2 = models.DecimalField('测试成绩 投掷球 第二次（米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_ball_3 = models.DecimalField('测试成绩 投掷球 第三次（米）', max_digits=5, decimal_places=2, null=True, blank=True)
    def _get_e_ball(self):
        values = (self.e_ball_1, self.e_ball_2, self.e_ball_3)
        if all(value != None for value in values):
            return max(values)
        else:
            return None
    e_ball = property(_get_e_ball, None, None, '测试成绩 投掷球（米）')
    
    #6分钟跑
    e_lauf_runden = models.PositiveSmallIntegerField('测试成绩 6分钟跑 圈数', null=True, blank=True)
    e_lauf_rest = models.PositiveSmallIntegerField('测试成绩 6分钟跑 最后未完成的一圈所跑距离（米）', null=True, blank=True)
    def _get_e_lauf(self):
        values = (self.e_lauf_runden, self.e_lauf_rest)
        if all(value != None for value in values):
            return self.e_lauf_runden * 54 + self.e_lauf_rest
        else:
            return None
    e_lauf = property(_get_e_lauf, None, None, '测试成绩 6分钟跑（米）')
    
    e_ls = models.IntegerField('俯卧撑 次数（40秒内）', null=True, blank=True)
    
    e_rb_1 = models.DecimalField('立位体前屈 第一次（厘米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_rb_2 = models.DecimalField('立位体前屈 第二次（厘米）', max_digits=5, decimal_places=2, null=True, blank=True)
    def _get_e_rb(self):
        values = (self.e_rb_1, self.e_rb_2)
        if all(value != None for value in values):
            return max(values)
        else:
            return None
    e_rb = property(_get_e_rb, None, None, '立位体前屈（厘米）')
    
    e_shh_1f = models.PositiveSmallIntegerField('侧向跳 第一次跳（错误次数）', null=True, blank=True)
    e_shh_1s = models.PositiveSmallIntegerField('侧向跳 第一次跳（总次数）', null=True, blank=True)
    e_shh_2f = models.PositiveSmallIntegerField('侧向跳 第二次跳（错误次数）', null=True, blank=True)
    e_shh_2s = models.PositiveSmallIntegerField('侧向跳 第二次跳（总次数）', null=True, blank=True)
    def _get_e_shh(self):
        values = (self.e_shh_1f, self.e_shh_1s, self.e_shh_2f, self.e_shh_2s)
        if all(value != None for value in values):
            return round(Decimal((self.e_shh_1s - self.e_shh_1f + self.e_shh_2s - self.e_shh_2f) / 2), 2)
        else:
            return None
    e_shh = property(_get_e_shh, None, None, '侧向跳（次数）')
    
    e_su = models.IntegerField('仰卧起坐 次数（40秒内）', null=True, blank=True)
    
    e_sws_1 = models.DecimalField('立定跳远 第一次（厘米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_sws_2 = models.DecimalField('立定跳远 第二次（厘米）', max_digits=5, decimal_places=2, null=True, blank=True)
    def _get_e_sws(self):
        values = (self.e_sws_1, self.e_sws_2)
        if all(value != None for value in values):
            return max(values)
        else:
            return None
    e_sws = property(_get_e_sws, None, None, '立定跳远（厘米）')
    
    e_slauf_10 = models.DecimalField('星形跑重复10次', max_digits=19, decimal_places=2, null=True, blank=True)

    last_name = models.CharField('姓', max_length=5, null=True, blank=True)
    first_name = models.CharField('名', max_length=10, null=True, blank=True)
    birth_date = models.DateField('出生日期', null=True, blank=True)
    school_name = models.CharField('学校名称', max_length=100, null=True, blank=True)
    class_name = models.CharField('班级名称', max_length=100, null=True, blank=True)
    external_id = models.CharField('外部标识', max_length=10, null=True, blank=True)
    def __str__(self):
        return self.lastName + ' ' + self.firstName

    def save(self, *args, **kw):
        dateOfTestingChanged = False
        if self.pk is not None:
            orig = Student.objects.get(pk=self.pk)
            if orig.dateOfTesting != self.dateOfTesting:
                dateOfTestingChanged = True
        else:
            if self.dateOfTesting is not None:
                dateOfTestingChanged = True

        if dateOfTestingChanged == True:
            if self.dateOfTesting is not None:
                sequenceNumberCodeOfNumber = 'NUMBER_DATE_OF_TESTING_' + str(self.dateOfTesting)
                self.number = GetNextSequenceNumberValue(sequenceNumberCodeOfNumber)
            else:
                self.number = None

        super(Student, self).save(*args, **kw)
    
    class Meta:
        verbose_name = "学生"
        verbose_name_plural = "学生"
        permissions = (
            ("import_student", "可以导入学生"),
            ("export_student", "可以导出学生"),
            ("evaluate_student", "可以评价学生"),
        )

class StudentEvaluation(models.Model):
    student = models.OneToOneField(Student)
    age = models.IntegerField('年龄')
    month_age = models.IntegerField('月龄')
    day_age = models.IntegerField('日龄')
    bmi = models.DecimalField('BMI', max_digits=3, decimal_places=1)
    original_score_bal = models.IntegerField('后退平衡 原始成绩')
    percentage_bal = models.DecimalField('后退平衡 评价', max_digits=5, decimal_places=2) 
    original_score_shh = models.DecimalField('侧向跳 原始成绩', max_digits=19, decimal_places=2)
    percentage_shh = models.DecimalField('侧向跳 评价', max_digits=5, decimal_places=2) 
    original_score_sws = models.DecimalField('立定跳远 原始成绩', max_digits=19, decimal_places=2)
    percentage_sws = models.DecimalField('立定跳远 评价', max_digits=5, decimal_places=2) 
    original_score_20m = models.DecimalField('20米跑 原始成绩', max_digits=19, decimal_places=2)
    percentage_20m = models.DecimalField('20米跑 评价', max_digits=5, decimal_places=2) 
    original_score_su = models.IntegerField('仰卧起坐 原始成绩')
    percentage_su = models.DecimalField('仰卧起坐 评价', max_digits=5, decimal_places=2) 
    original_score_ls = models.IntegerField('俯卧撑 原始成绩')
    percentage_ls = models.DecimalField('俯卧撑 评价', max_digits=5, decimal_places=2) 
    original_score_rb = models.DecimalField('立位体前屈 原始成绩', max_digits=19, decimal_places=2)
    percentage_rb = models.DecimalField('立位体前屈 评价', max_digits=5, decimal_places=2) 
    original_score_lauf = models.IntegerField('6分钟跑 原始成绩')
    percentage_lauf = models.DecimalField('6分钟跑 评价', max_digits=5, decimal_places=2) 
    original_score_ball = models.DecimalField('投掷球 原始成绩', max_digits=19, decimal_places=2)
    percentage_ball = models.DecimalField('投掷球 评价', max_digits=5, decimal_places=2)
    score_sum = models.DecimalField('评价总分', max_digits=19, decimal_places=2)

    def __str__(self):
        return str(self.student) + ' 的评价'

    class Meta:
        verbose_name = "学生评价"
        verbose_name_plural = "学生评价"

class TestRefData(models.Model):
    testing_date = models.DateField('测试日期')
    testing_number = models.IntegerField('测试编号')
    student = models.ForeignKey(Student, verbose_name="测试学生")
    height = models.FloatField('身高')
    weight = models.FloatField('体重')
    def __str__(self):
        return str(self.testing_date) + '#' + str(self.testing_number)
    
    class Meta:
        verbose_name_plural = "测试原始记录(TestRefDatas)"

class TestRefDataItem(models.Model):
    test_ref_data = models.ForeignKey(TestRefData, verbose_name="测试原始记录")
    movement_type = models.CharField('测试点', max_length=10, choices=MovementTypes)
    key = models.CharField('数据项(第一次, 第二次, ...)', max_length=10)
    value = models.FloatField('数据值')
    def __str__(self):
        return str(self.key)
    
    class Meta:
        verbose_name_plural = "测试原始记录单项数据(TestRefDataItem)"

class TestSummaryData(models.Model):
    student = models.ForeignKey(Student)
    testing_date = models.DateField('测试日期')
    height = models.FloatField('身高')
    weight = models.FloatField('体重')
    month_age = models.IntegerField('月龄')
    day_age = models.IntegerField('日龄')
    test_ref_data = models.ForeignKey(TestRefData)
    
    class Meta:
        verbose_name_plural = "测试总结(TestSummaryData)"

class TestSummaryDataItem(models.Model):
    test_summary_data = models.ForeignKey(TestSummaryData)
    movement_type = models.CharField('测试点', max_length=10, choices=MovementTypes)
    value = models.FloatField('数据值')
    evaluate_date = models.DateTimeField('评估时间')
    evaluate_value = models.FloatField('评估分值')
    
    class Meta:
        verbose_name_plural = "测试总结单项数据(TestSummaryDataItem)"

    
    
