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

class Factor(models.Model):
    gender = models.CharField('性别', max_length=10, choices=Genders)
    month_age = models.IntegerField('月龄')
    movement_type = models.CharField('测试点', max_length=10, choices=MovementTypes)
    mean = models.FloatField('平均值')
    standard_deviation = models.FloatField('标准偏差')
    
    class Meta:
        verbose_name_plural = "分布因素(Factors)"
    
class Student(models.Model):
    schoolClass = models.ForeignKey(SchoolClass, verbose_name="班级")
    firstName = models.CharField('名', max_length=255)
    lastName = models.CharField('姓', max_length=255)
    universalFirstName = models.CharField('名（英文）', max_length=255, null=True, blank=True)
    universalLastName = models.CharField('姓（英文）', max_length=255, null=True, blank=True)
    gender = models.CharField('性别', max_length=255, choices=Genders, null=True, blank=True)
    dateOfBirth = models.DateField('出生日期', null=True, blank=True)
    dateOfTesting = models.DateField('考试日期', null=True, blank=True)
    number = models.IntegerField('测试号码', null=True, blank=True)
    questionary = models.IntegerField('问卷编号', null=True, blank=True)
    street = models.CharField('路（地址）', max_length=255, null=True, blank=True)
    housenumber = models.CharField('弄（地址）', max_length=255, null=True, blank=True)
    addition = models.CharField('号（地址）', max_length=255, null=True, blank=True)
    zip = models.CharField('邮政编码（地址）', max_length=255, null=True, blank=True)
    city = models.CharField('城市（地址）', max_length=255, null=True, blank=True)
    addressClearance = models.BooleanField('地址Clearance', default=False)
    e_20m_1 = models.DecimalField('20米冲刺跑1', max_digits=19, decimal_places=2, null=True, blank=True)
    e_20m_2 = models.DecimalField('20米冲刺跑2', max_digits=19, decimal_places=2, null=True, blank=True)
    e_bal30_1 = models.IntegerField('3厘米平衡木1', null=True, blank=True)
    e_bal30_2 = models.IntegerField('3厘米平衡木2', null=True, blank=True)
    e_bal45_1 = models.IntegerField('4.5厘米平衡木1', null=True, blank=True)
    e_bal45_2 = models.IntegerField('4.5厘米平衡木2', null=True, blank=True)
    e_bal60_1 = models.IntegerField('6厘米平衡木1', null=True, blank=True)
    e_bal60_2 = models.IntegerField('6厘米平衡木2', null=True, blank=True)
    e_ball_1 = models.DecimalField('投掷1', max_digits=19, decimal_places=2, null=True, blank=True)
    e_ball_2 = models.DecimalField('投掷2', max_digits=19, decimal_places=2, null=True, blank=True)
    e_ball_3 = models.DecimalField('投掷3', max_digits=19, decimal_places=2, null=True, blank=True)
    e_lauf_rest = models.IntegerField('六分跑剩余距离', null=True, blank=True)
    e_lauf_runden = models.IntegerField('六分跑圈数', null=True, blank=True)
    e_ls = models.IntegerField('俯卧撑', null=True, blank=True)
    e_rb_1 = models.DecimalField('直身前屈1', max_digits=19, decimal_places=2, null=True, blank=True)
    e_rb_2 = models.DecimalField('直身前屈2', max_digits=19, decimal_places=2, null=True, blank=True)
    e_shh_1f = models.IntegerField('侧向跳1 错误', null=True, blank=True)
    e_shh_1s = models.IntegerField('侧向跳1 次', null=True, blank=True)
    e_shh_2f = models.IntegerField('侧向跳2 错误', null=True, blank=True)
    e_shh_2s = models.IntegerField('侧向跳2 次', null=True, blank=True)
    e_slauf_10 = models.DecimalField('星形跑重复10次', max_digits=19, decimal_places=2, null=True, blank=True)
    e_su = models.IntegerField('仰卧起坐', null=True, blank=True)
    e_sws_1 = models.DecimalField('跳远1', max_digits=19, decimal_places=2, null=True, blank=True)
    e_sws_2 = models.DecimalField('跳远2', max_digits=19, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField('体重（千克）', max_digits=19, decimal_places=2, null=True, blank=True)
    height = models.DecimalField('身高（厘米）', max_digits=19, decimal_places=2, null=True, blank=True)

    last_name = models.CharField('姓', max_length=5)
    first_name = models.CharField('名', max_length=10)
    birth_date = models.DateField('出生日期')
    school_name = models.CharField('学校名称', max_length=100)
    class_name = models.CharField('班级名称', max_length=100)
    external_id = models.CharField('外部标识', max_length=10, null=True, blank=True)
    def __str__(self):
        return self.last_name + ' ' + self.first_name
    
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

    
    
