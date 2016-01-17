from django.db import models

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

class School(models.Model):
    name = models.CharField('名称', max_length=100)
    universalName = models.CharField('名称（英文）', max_length=100)

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
    gender = models.CharField('性别', max_length=10, choices=Genders)
    month_age = models.IntegerField('月龄')
    movement_type = models.CharField('测试点', max_length=10, choices=MovementTypes)
    mean = models.FloatField('平均值')
    standard_deviation = models.FloatField('标准偏差')
    
    class Meta:
        verbose_name_plural = "分布因素(Factors)"
    
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
    e_20m_1 = models.DecimalField('20米跑 第一次跑（秒）', max_digits=19, decimal_places=2, null=True, blank=True)
    e_20m_2 = models.DecimalField('20米跑 第二次跑（秒）', max_digits=19, decimal_places=2, null=True, blank=True)
    e_bal30_1 = models.IntegerField('后退平衡 3.0厘米 第一次', null=True, blank=True)
    e_bal30_2 = models.IntegerField('后退平衡 3.0厘米 第二次', null=True, blank=True)
    e_bal45_1 = models.IntegerField('后退平衡 4.5厘米 第一次', null=True, blank=True)
    e_bal45_2 = models.IntegerField('后退平衡 4.5厘米 第二次', null=True, blank=True)
    e_bal60_1 = models.IntegerField('后退平衡 6.0厘米 第一次', null=True, blank=True)
    e_bal60_2 = models.IntegerField('后退平衡 6.0厘米 第二次', null=True, blank=True)
    e_ball_1 = models.DecimalField('投掷球 第一次', max_digits=19, decimal_places=2, null=True, blank=True)
    e_ball_2 = models.DecimalField('投掷球 第二次', max_digits=19, decimal_places=2, null=True, blank=True)
    e_ball_3 = models.DecimalField('投掷球 第三次', max_digits=19, decimal_places=2, null=True, blank=True)
    e_lauf_rest = models.IntegerField('6分钟跑 最后未完成的一圈所跑距离（米）', null=True, blank=True)
    e_lauf_runden = models.IntegerField('6分钟跑 圈数', null=True, blank=True)
    e_ls = models.IntegerField('俯卧撑 次数（40秒内）', null=True, blank=True)
    e_rb_1 = models.DecimalField('立位体前屈 第一次（厘米）', max_digits=19, decimal_places=2, null=True, blank=True)
    e_rb_2 = models.DecimalField('立位体前屈 第二次（厘米）', max_digits=19, decimal_places=2, null=True, blank=True)
    e_shh_1f = models.IntegerField('侧向跳 第一次跳（错误次数）', null=True, blank=True)
    e_shh_1s = models.IntegerField('侧向跳 第一次跳（总次数）', null=True, blank=True)
    e_shh_2f = models.IntegerField('侧向跳 第二次跳（错误次数）', null=True, blank=True)
    e_shh_2s = models.IntegerField('侧向跳 第二次跳（总次数）', null=True, blank=True)
    e_slauf_10 = models.DecimalField('星形跑重复10次', max_digits=19, decimal_places=2, null=True, blank=True)
    e_su = models.IntegerField('仰卧起坐 次数（40秒内）', null=True, blank=True)
    e_sws_1 = models.DecimalField('立定跳远 第一次（厘米）', max_digits=19, decimal_places=2, null=True, blank=True)
    e_sws_2 = models.DecimalField('立定跳远 第二次（厘米）', max_digits=19, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField('体重（公斤）', max_digits=19, decimal_places=2, null=True, blank=True)
    height = models.IntegerField('身高（厘米）', null=True, blank=True)

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

    
    
