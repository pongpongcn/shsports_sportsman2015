from rest_framework import serializers

from django.contrib.auth.models import User, Group
from .models import District, Student, Genders

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
      
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('name',)

class StudentEntry(object):
    def __init__(self, *args, **kwargs):
        self.noOfStudentStatus = kwargs.get('noOfStudentStatus')
        self.school = kwargs.get('school')
        self.schoolClass = kwargs.get('schoolClass')
        self.firstName = kwargs.get('firstName')
        self.lastName = kwargs.get('lastName')
        self.gender = kwargs.get('gender')
        self.dateOfBirth = kwargs.get('dateOfBirth')
        self.dateOfTesting = kwargs.get('dateOfTesting')
        self.creator = kwargs.get('creator')

class StudentCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    noOfStudentStatus = serializers.CharField(label='学籍号', max_length=255)
    school = serializers.CharField(label='学校', max_length=100)
    schoolClass = serializers.CharField(label='班级', max_length=100)
    firstName = serializers.CharField(label='名', max_length=255)
    lastName = serializers.CharField(label='姓', max_length=255)
    gender = serializers.ChoiceField(choices=Genders, label='性别')
    dateOfBirth = serializers.DateField(label='出生日期')
    dateOfTesting = serializers.DateField(label='测试日期', required=False)
    
    def create(self, validated_data):
        instance = StudentEntry(**validated_data)
        if instance.creator is not None:
            print('creator:' + str(instance.creator))
        return instance
        
    '''
    firstName = models.CharField('名', max_length=255)
    lastName = models.CharField('姓', max_length=255)
    universalFirstName = models.CharField('名（英文）', max_length=255, null=True, blank=True)
    universalLastName = models.CharField('姓（英文）', max_length=255, null=True, blank=True)
    gender = models.CharField('性别', max_length=255, choices=Genders, null=True, blank=True)
    dateOfBirth = models.DateField('出生日期', null=True, blank=True)
    dateOfTesting = models.DateField('测试日期', null=True, blank=True)
    number = models.IntegerField('测试编号', null=True, blank=True)
    weight = models.DecimalField('体重（公斤）', max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.PositiveSmallIntegerField('身高（厘米）', null=True, blank=True)
    e_bal30_1 = models.PositiveSmallIntegerField('测试成绩 平衡 3.0厘米 第一次（步）', null=True, blank=True)
    e_bal30_2 = models.PositiveSmallIntegerField('测试成绩 平衡 3.0厘米 第二次（步）', null=True, blank=True)
    e_bal45_1 = models.PositiveSmallIntegerField('测试成绩 平衡 4.5厘米 第一次（步）', null=True, blank=True)
    e_bal45_2 = models.PositiveSmallIntegerField('测试成绩 平衡 4.5厘米 第二次（步）', null=True, blank=True)
    e_bal60_1 = models.PositiveSmallIntegerField('测试成绩 平衡 6.0厘米 第一次（步）', null=True, blank=True)
    e_bal60_2 = models.PositiveSmallIntegerField('测试成绩 平衡 6.0厘米 第二次（步）', null=True, blank=True)
    e_shh_1f = models.PositiveSmallIntegerField('测试成绩 侧向跳 第一次跳（错误次数）', null=True, blank=True)
    e_shh_1s = models.PositiveSmallIntegerField('测试成绩 侧向跳 第一次跳（总次数）', null=True, blank=True)
    e_shh_2f = models.PositiveSmallIntegerField('测试成绩 侧向跳 第二次跳（错误次数）', null=True, blank=True)
    e_shh_2s = models.PositiveSmallIntegerField('测试成绩 侧向跳 第二次跳（总次数）', null=True, blank=True)
    e_sws_1 = models.DecimalField('测试成绩 跳远 第一次（厘米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_sws_2 = models.DecimalField('测试成绩 跳远 第二次（厘米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_20m_1 = models.DecimalField('测试成绩 20米冲刺跑 第一次（秒）', max_digits=4, decimal_places=2, null=True, blank=True)
    e_20m_2 = models.DecimalField('测试成绩 20米冲刺跑 第二次（秒）', max_digits=4, decimal_places=2, null=True, blank=True)
    e_su = models.IntegerField('测试成绩 仰卧起坐（重复次数）', null=True, blank=True)
    e_ls = models.IntegerField('测试成绩 俯卧撑（重复次数）', null=True, blank=True)
    e_rb_1 = models.DecimalField('测试成绩 直身前屈 第一次（厘米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_rb_2 = models.DecimalField('测试成绩 直身前屈 第二次（厘米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_lauf_runden = models.PositiveSmallIntegerField('测试成绩 六分跑 已完成圈数', null=True, blank=True)
    e_lauf_rest = models.PositiveSmallIntegerField('测试成绩 六分跑 最后未完成的一圈所跑距离（米）', null=True, blank=True)
    e_ball_1 = models.DecimalField('测试成绩 投掷 第一次（米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_ball_2 = models.DecimalField('测试成绩 投掷 第二次（米）', max_digits=5, decimal_places=2, null=True, blank=True)
    e_ball_3 = models.DecimalField('测试成绩 投掷 第三次（米）', max_digits=5, decimal_places=2, null=True, blank=True)    
    '''
    
class StudentSerializer(serializers.ModelSerializer):
    school = serializers.SerializerMethodField()
    schoolClass = serializers.SerializerMethodField()
    
    def get_school(self, obj):
        return obj.schoolClass.school.name
    
    def get_schoolClass(self, obj):
        return obj.schoolClass.name

    class Meta:
        model = Student
        fields = ('id', 'noOfStudentStatus', 'school', 'schoolClass', 'firstName', 'lastName', 'gender', 'dateOfBirth',
        'dateOfTesting', 'number',
        'weight', 'height',
        'e_bal30_1','e_bal30_2','e_bal45_1','e_bal45_2','e_bal60_1','e_bal60_2',
        'e_shh_1f','e_shh_1s','e_shh_2f','e_shh_2s',
        'e_sws_1','e_sws_2',
        'e_20m_1','e_20m_2',
        'e_su',
        'e_ls',
        'e_rb_1','e_rb_2',
        'e_lauf_runden','e_lauf_rest',
        'e_ball_1','e_ball_2','e_ball_3')