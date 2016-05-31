from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from .functions import calculate_age, calculate_months_of_age, calculate_days_of_age, calculate_bmi

# Create your models here.

Genders = (
     ('MALE', '男'),
     ('FEMALE', '女'),
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
    e_20m = models.DecimalField('20米跑', max_digits=3, decimal_places=2)
    e_bal = models.IntegerField('后退平衡')
    e_shh = models.IntegerField('侧向跳')
    e_rb = models.DecimalField('立位体前屈', max_digits=3, decimal_places=1)
    e_ls = models.IntegerField('俯卧撑')
    e_su = models.IntegerField('仰卧起坐')
    e_sws = models.DecimalField('立定跳远', max_digits=4, decimal_places=1)
    e_ball = models.DecimalField('投掷球', max_digits=3, decimal_places=1)
    e_lauf = models.IntegerField('6分钟跑')

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
    mean_weight = models.DecimalField('体重（公斤）平均值', max_digits=5, decimal_places=2)
    standard_deviation_weight = models.DecimalField('体重（公斤）标准偏差', max_digits=10, decimal_places=4)
    mean_height = models.DecimalField('身高（厘米）平均值', max_digits=4, decimal_places=1)
    standard_deviation_height = models.DecimalField('身高（厘米）标准偏差', max_digits=10, decimal_places=4)
    mean_bmi = models.DecimalField('BMI平均值', max_digits=3, decimal_places=1)
    standard_deviation_bmi = models.DecimalField('BMI标准偏差', max_digits=10, decimal_places=4)

    def __str__(self):
        return '%s months, %s(%s)' % (self.month_age, self.gender, self.version)
    
    class Meta:
        verbose_name = "测试项目成绩分布参数"
        verbose_name_plural = "测试项目成绩分布参数"

class Sport(models.Model):
    code = models.CharField('代码', max_length=50, unique=True)
    name = models.CharField('名称', max_length=50)
    universalName = models.CharField('名称（英文）', max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "体育项目"
        verbose_name_plural = "体育项目"

class SportPotentialFactor(models.Model):
    sport = models.ForeignKey(Sport, verbose_name="体育项目")
    weight_p_bal = models.DecimalField('权重 平衡', max_digits=6, decimal_places=4)
    weight_p_shh = models.DecimalField('权重 侧向跳', max_digits=6, decimal_places=4)
    weight_p_sws = models.DecimalField('权重 跳远', max_digits=6, decimal_places=4)
    weight_p_20m = models.DecimalField('权重 20米冲刺跑', max_digits=6, decimal_places=4)
    weight_p_su = models.DecimalField('权重 仰卧起坐', max_digits=6, decimal_places=4)
    weight_p_ls = models.DecimalField('权重 俯卧撑', max_digits=6, decimal_places=4)
    weight_p_rb = models.DecimalField('权重 直身前屈', max_digits=6, decimal_places=4)
    weight_p_lauf = models.DecimalField('权重 六分跑', max_digits=6, decimal_places=4)
    weight_p_ball = models.DecimalField('权重 投掷', max_digits=6, decimal_places=4)
    weight_p_height = models.DecimalField('权重 身高', max_digits=6, decimal_places=4)
    weight_p_weight = models.DecimalField('权重 体重', max_digits=6, decimal_places=4)
    weight_p_bmi = models.DecimalField('权重 BMI', max_digits=6, decimal_places=4)
    const = models.DecimalField('常量', max_digits=6, decimal_places=4)

    def __str__(self):
        return '%s 潜质参数' % str(self.sport)
    
    class Meta:
        verbose_name = "体育项目潜质参数"
        verbose_name_plural = "体育项目潜质参数"
        
class TestPlan(models.Model):
    name = models.CharField('名称', max_length=255)
    startDate = models.DateField('开始日期', null=True, blank=True)
    endDate = models.DateField('结束日期', null=True, blank=True)
    isPublished = models.BooleanField('已发布', default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "测试批次"
        verbose_name_plural = "测试批次"
        
class Student(models.Model):
    noOfStudentStatus = models.CharField('学籍号', max_length=255, null=True, blank=True)
    testPlan = models.ForeignKey(TestPlan, verbose_name="测试批次", null=True, blank=True)
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
    creator = models.ForeignKey(User, verbose_name="创建者", null=True, blank=True)
    
    def _get_age(self):
        values = (self.dateOfBirth, self.dateOfTesting)
        if all(value != None for value in values):
            return calculate_age(self.dateOfBirth, self.dateOfTesting)
        else:
            return None
    age = property(_get_age, None, None, '年龄')
    
    def _get_months_of_age(self):
        values = (self.dateOfBirth, self.dateOfTesting)
        if all(value != None for value in values):
            return calculate_months_of_age(self.dateOfBirth, self.dateOfTesting)
        else:
            return None
    months_of_age = property(_get_months_of_age, None, None, '月龄')
    
    def _get_days_of_age(self):
        values = (self.dateOfBirth, self.dateOfTesting)
        if all(value != None for value in values):
            return calculate_days_of_age(self.dateOfBirth, self.dateOfTesting)
        else:
            return None
    days_of_age = property(_get_days_of_age, None, None, '日龄')
    
    def _get_bmi(self):
        values = (self.weight, self.height)
        if all(value != None for value in values):
            return calculate_bmi(self.weight, self.height * Decimal(0.01))
        else:
            return None
    bmi = property(_get_bmi, None, None, 'BMI')

    #Examination results

    weight = models.DecimalField('体重（公斤）', max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.PositiveSmallIntegerField('身高（厘米）', null=True, blank=True)
    
    #平衡
    e_bal30_1 = models.PositiveSmallIntegerField('测试成绩 平衡 3.0厘米 第一次（步）', null=True, blank=True)
    e_bal30_2 = models.PositiveSmallIntegerField('测试成绩 平衡 3.0厘米 第二次（步）', null=True, blank=True)
    e_bal45_1 = models.PositiveSmallIntegerField('测试成绩 平衡 4.5厘米 第一次（步）', null=True, blank=True)
    e_bal45_2 = models.PositiveSmallIntegerField('测试成绩 平衡 4.5厘米 第二次（步）', null=True, blank=True)
    e_bal60_1 = models.PositiveSmallIntegerField('测试成绩 平衡 6.0厘米 第一次（步）', null=True, blank=True)
    e_bal60_2 = models.PositiveSmallIntegerField('测试成绩 平衡 6.0厘米 第二次（步）', null=True, blank=True)
    def _get_e_bal(self):
        values = (self.e_bal60_1, self.e_bal60_2, self.e_bal45_1, self.e_bal45_2, self.e_bal30_1, self.e_bal30_2)
        if all(value != None for value in values):
            return sum(values)
        else:
            return None
    e_bal = property(_get_e_bal, None, None, '测试成绩 平衡（步）')
    
    #侧向跳
    e_shh_1f = models.PositiveSmallIntegerField('测试成绩 侧向跳 第一次跳（错误次数）', null=True, blank=True)
    e_shh_1s = models.PositiveSmallIntegerField('测试成绩 侧向跳 第一次跳（总次数）', null=True, blank=True)
    e_shh_2f = models.PositiveSmallIntegerField('测试成绩 侧向跳 第二次跳（错误次数）', null=True, blank=True)
    e_shh_2s = models.PositiveSmallIntegerField('测试成绩 侧向跳 第二次跳（总次数）', null=True, blank=True)
    def _get_e_shh(self):
        values = (self.e_shh_1f, self.e_shh_1s, self.e_shh_2f, self.e_shh_2s)
        if all(value != None for value in values):
            return round(Decimal((self.e_shh_1s - self.e_shh_1f + self.e_shh_2s - self.e_shh_2f) / 2), 2)
        else:
            return None
    e_shh = property(_get_e_shh, None, None, '测试成绩 侧向跳（次）')
    
    #跳远
    e_sws_1 = models.DecimalField('测试成绩 跳远 第一次（厘米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_sws_2 = models.DecimalField('测试成绩 跳远 第二次（厘米）', max_digits=5, decimal_places=2, null=True, blank=True)
    def _get_e_sws(self):
        values = (self.e_sws_1, self.e_sws_2)
        if all(value != None for value in values):
            return max(values)
        else:
            return None
    e_sws = property(_get_e_sws, None, None, '测试成绩 跳远（厘米）')
    
    #20米冲刺跑
    e_20m_1 = models.DecimalField('测试成绩 20米冲刺跑 第一次（秒）', max_digits=4, decimal_places=2, null=True, blank=True)
    e_20m_2 = models.DecimalField('测试成绩 20米冲刺跑 第二次（秒）', max_digits=4, decimal_places=2, null=True, blank=True)
    def _get_e_20m(self):
        values = (self.e_20m_1, self.e_20m_2)
        if all(value != None for value in values):
            return min(values)
        else:
            return None
    e_20m = property(_get_e_20m, None, None, '测试成绩 20米冲刺跑（秒）')

    #仰卧起坐
    e_su = models.IntegerField('测试成绩 仰卧起坐（重复次数）', null=True, blank=True)
    
    #俯卧撑
    e_ls = models.IntegerField('测试成绩 俯卧撑（重复次数）', null=True, blank=True)

    #直身前屈
    e_rb_1 = models.DecimalField('测试成绩 直身前屈 第一次（厘米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_rb_2 = models.DecimalField('测试成绩 直身前屈 第二次（厘米）', max_digits=5, decimal_places=2, null=True, blank=True)
    def _get_e_rb(self):
        values = (self.e_rb_1, self.e_rb_2)
        if all(value != None for value in values):
            return max(values)
        else:
            return None
    e_rb = property(_get_e_rb, None, None, '测试成绩 直身前屈（厘米）')
    
    #六分跑
    e_lauf_runden = models.PositiveSmallIntegerField('测试成绩 六分跑 已完成圈数', null=True, blank=True)
    e_lauf_rest = models.PositiveSmallIntegerField('测试成绩 六分跑 最后未完成的一圈所跑距离（米）', null=True, blank=True)
    def _get_e_lauf(self):
        values = (self.e_lauf_runden, self.e_lauf_rest)
        if all(value != None for value in values):
            return self.e_lauf_runden * 54 + self.e_lauf_rest
        else:
            return None
    e_lauf = property(_get_e_lauf, None, None, '测试成绩 六分跑')
    
    #投掷
    e_ball_1 = models.DecimalField('测试成绩 投掷 第一次（米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_ball_2 = models.DecimalField('测试成绩 投掷 第二次（米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_ball_3 = models.DecimalField('测试成绩 投掷 第三次（米）', max_digits=5, decimal_places=2, null=True, blank=True)
    def _get_e_ball(self):
        values = (self.e_ball_1, self.e_ball_2, self.e_ball_3)
        if all(value != None for value in values):
            return max(values)
        else:
            return None
    e_ball = property(_get_e_ball, None, None, '测试成绩 投掷（米）')

    e_slauf_10 = models.DecimalField('星形跑重复10次', max_digits=19, decimal_places=2, null=True, blank=True)
    last_name = models.CharField('姓', max_length=5, null=True, blank=True)
    first_name = models.CharField('名', max_length=10, null=True, blank=True)
    birth_date = models.DateField('出生日期', null=True, blank=True)
    school_name = models.CharField('学校名称', max_length=100, null=True, blank=True)
    class_name = models.CharField('班级名称', max_length=100, null=True, blank=True)
    external_id = models.CharField('外部标识', max_length=10, null=True, blank=True)
    
    x_jirou = models.CharField('肌肉', max_length=255, null=True, blank=True)
    x_shuifen = models.CharField('水分', max_length=255, null=True, blank=True)
    x_jichudaixie = models.CharField('基础代谢', max_length=255, null=True, blank=True)
    
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
    
    testPlan = models.ForeignKey(TestPlan, verbose_name="测试批次", null=True, blank=True)
    
    p_bal = models.PositiveSmallIntegerField('百分等级 平衡', null=True, blank=True)
    p_shh = models.PositiveSmallIntegerField('百分等级 侧向跳', null=True, blank=True)
    p_sws = models.PositiveSmallIntegerField('百分等级 跳远', null=True, blank=True)
    p_20m = models.PositiveSmallIntegerField('百分等级 20米冲刺跑', null=True, blank=True)
    p_su = models.PositiveSmallIntegerField('百分等级 仰卧起坐', null=True, blank=True)
    p_ls = models.PositiveSmallIntegerField('百分等级 俯卧撑', null=True, blank=True)
    p_rb = models.PositiveSmallIntegerField('百分等级 直身前屈', null=True, blank=True)
    p_lauf = models.PositiveSmallIntegerField('百分等级 六分跑', null=True, blank=True)
    p_ball = models.PositiveSmallIntegerField('百分等级 投掷', null=True, blank=True)
    p_height = models.PositiveSmallIntegerField('百分等级 身高', null=True, blank=True)
    p_weight = models.PositiveSmallIntegerField('百分等级 体重', null=True, blank=True)
    p_bmi = models.PositiveSmallIntegerField('百分等级 BMI', null=True, blank=True)
    
    potential_badminton = models.DecimalField('运动潜质 羽毛球', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_basketball = models.DecimalField('运动潜质 篮球', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_soccer = models.DecimalField('运动潜质 足球', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_gymnastics = models.DecimalField('运动潜质 体操', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_canoe = models.DecimalField('运动潜质 皮艇/划艇', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_discus = models.DecimalField('运动潜质 铁饼', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_shot_put = models.DecimalField('运动潜质 铅球', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_pole_vault = models.DecimalField('运动潜质 撑杆跳', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_high_jump = models.DecimalField('运动潜质 跳高', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_javelin = models.DecimalField('运动潜质 标枪', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_long_jump = models.DecimalField('运动潜质 跳远', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_huerdles = models.DecimalField('运动潜质 跨栏', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_sprint = models.DecimalField('运动潜质 短跑', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_rowing = models.DecimalField('运动潜质 赛艇', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_swimming = models.DecimalField('运动潜质 游泳', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_tennis = models.DecimalField('运动潜质 网球', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_table_tennis = models.DecimalField('运动潜质 乒乓球', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_volleyball = models.DecimalField('运动潜质 排球', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_athletics_running = models.DecimalField('运动潜质 耐力跑', max_digits=7, decimal_places=6, null=True, blank=True)
    potential_athletics_sprinting_jumping_throwing = models.DecimalField('运动潜质 跑跳投', max_digits=7, decimal_places=6, null=True, blank=True)
    
    is_talent = models.BooleanField('运动天赋优秀', default=False)
    is_frail = models.BooleanField('需要健康干预', default=False)
    '''排名均基于测试批次'''
    overall_score = models.PositiveSmallIntegerField('总分', null=True, blank=True)
    talent_rank_number = models.PositiveSmallIntegerField('运动天赋优秀排名', null=True, blank=True)
    frail_rank_number = models.PositiveSmallIntegerField('需要健康干预排名', null=True, blank=True)
    certificate_data = models.TextField('证书数据', null=True, blank=True)
    certificate_file = models.FileField('证书文件', upload_to='certificates/%Y/%m/%d/', null=True, blank=True)
    
    def __str__(self):
        return str(self.student) + ' 的评价'

    class Meta:
        verbose_name = "学生评价"
        verbose_name_plural = "学生评价"