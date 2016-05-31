from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Student, Genders, School, SchoolClass, StudentEvaluation

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
        self.number = kwargs.get('number')
        self.weight = kwargs.get('weight')
        self.height = kwargs.get('height')
        self.e_bal30_1 = kwargs.get('e_bal30_1')
        self.e_bal30_2 = kwargs.get('e_bal30_2')
        self.e_bal45_1 = kwargs.get('e_bal45_1')
        self.e_bal45_2 = kwargs.get('e_bal45_2')
        self.e_bal60_1 = kwargs.get('e_bal60_1')
        self.e_bal60_2 = kwargs.get('e_bal60_2')
        self.e_shh_1f = kwargs.get('e_shh_1f')
        self.e_shh_1s = kwargs.get('e_shh_1s')
        self.e_shh_2f = kwargs.get('e_shh_2f')
        self.e_shh_2s = kwargs.get('e_shh_2s')
        self.e_sws_1 = kwargs.get('e_sws_1')
        self.e_sws_2 = kwargs.get('e_sws_2')
        self.e_20m_1 = kwargs.get('e_20m_1')
        self.e_20m_2 = kwargs.get('e_20m_2')
        self.e_su = kwargs.get('e_su')
        self.e_ls = kwargs.get('e_ls')
        self.e_rb_1 = kwargs.get('e_rb_1')
        self.e_rb_2 = kwargs.get('e_rb_2')
        self.e_lauf_runden = kwargs.get('e_lauf_runden')
        self.e_lauf_rest = kwargs.get('e_lauf_rest')
        self.e_ball_1 = kwargs.get('e_ball_1')
        self.e_ball_2 = kwargs.get('e_ball_2')
        self.e_ball_3 = kwargs.get('e_ball_3')
        self.creator = kwargs.get('creator')
        self.x_jirou = kwargs.get('x_jirou')
        self.x_shuifen = kwargs.get('x_shuifen')
        self.x_jichudaixie = kwargs.get('x_jichudaixie')

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
    number = serializers.IntegerField(label='测试编号', read_only=True)
    weight = serializers.DecimalField(label='体重（公斤）', max_digits=5, decimal_places=2, required=False)
    height = serializers.IntegerField(label='身高（厘米）', required=False)
    e_bal30_1 = serializers.IntegerField(label='测试成绩 平衡 3.0厘米 第一次（步）', required=False)
    e_bal30_2 = serializers.IntegerField(label='测试成绩 平衡 3.0厘米 第二次（步）', required=False)
    e_bal45_1 = serializers.IntegerField(label='测试成绩 平衡 4.5厘米 第一次（步）', required=False)
    e_bal45_2 = serializers.IntegerField(label='测试成绩 平衡 4.5厘米 第二次（步）', required=False)
    e_bal60_1 = serializers.IntegerField(label='测试成绩 平衡 6.0厘米 第一次（步）', required=False)
    e_bal60_2 = serializers.IntegerField(label='测试成绩 平衡 6.0厘米 第二次（步）', required=False)
    e_shh_1f = serializers.IntegerField(label='测试成绩 侧向跳 第一次跳（错误次数）', required=False)
    e_shh_1s = serializers.IntegerField(label='测试成绩 侧向跳 第一次跳（总次数）', required=False)
    e_shh_2f = serializers.IntegerField(label='测试成绩 侧向跳 第二次跳（错误次数）', required=False)
    e_shh_2s = serializers.IntegerField(label='测试成绩 侧向跳 第二次跳（总次数）', required=False)
    e_sws_1 = serializers.DecimalField(label='测试成绩 跳远 第一次（厘米）', max_digits=5, decimal_places=2, required=False)
    e_sws_2 = serializers.DecimalField(label='测试成绩 跳远 第二次（厘米）', max_digits=5, decimal_places=2, required=False)
    e_20m_1 = serializers.DecimalField(label='测试成绩 20米冲刺跑 第一次（秒）', max_digits=4, decimal_places=2, required=False)
    e_20m_2 = serializers.DecimalField(label='测试成绩 20米冲刺跑 第二次（秒）', max_digits=4, decimal_places=2, required=False)
    e_su = serializers.IntegerField(label='测试成绩 仰卧起坐（重复次数）', required=False)
    e_ls = serializers.IntegerField(label='测试成绩 俯卧撑（重复次数）', required=False)
    e_rb_1 = serializers.DecimalField(label='测试成绩 直身前屈 第一次（厘米）', max_digits=5, decimal_places=2, required=False)
    e_rb_2 = serializers.DecimalField(label='测试成绩 直身前屈 第二次（厘米）', max_digits=5, decimal_places=2, required=False)
    e_lauf_runden = serializers.IntegerField(label='测试成绩 六分跑 已完成圈数', required=False)
    e_lauf_rest = serializers.IntegerField(label='测试成绩 六分跑 最后未完成的一圈所跑距离（米）', required=False)
    e_ball_1 = serializers.DecimalField(label='测试成绩 投掷 第一次（米）', max_digits=5, decimal_places=2, required=False)
    e_ball_2 = serializers.DecimalField(label='测试成绩 投掷 第二次（米）', max_digits=5, decimal_places=2, required=False)
    e_ball_3 = serializers.DecimalField(label='测试成绩 投掷 第三次（米）', max_digits=5, decimal_places=2, required=False)   
    x_jirou = serializers.CharField(label='肌肉', max_length=255, required=False)
    x_shuifen = serializers.CharField(label='水分', max_length=255, required=False)
    x_jichudaixie = serializers.CharField(label='基础代谢', max_length=255, required=False)
    
    def create(self, validated_data):
        instance = StudentEntry(**validated_data)
        schoolName = validated_data.get('school')
        schoolClassName = validated_data.get('schoolClass')
        schoolClass = self.get_schoolClass(schoolName, schoolClassName)
        
        del validated_data['school']
        del validated_data['schoolClass']
        
        validated_data['schoolClass'] = schoolClass
        
        student = Student(**validated_data);
        student.save()
        
        instance.id = student.id
        instance.number = student.number
        return instance
        
    def get_schoolClass(self, schoolName, schoolClassName):
        schoolQuery = School.objects.filter(name=schoolName)
        if schoolQuery.exists():
            school = schoolQuery[0]
        else:
            school = School(name=schoolName, universalName='')
            school.save()
        schoolClassQuery = SchoolClass.objects.filter(school=school, name=schoolClassName)
        if schoolClassQuery.exists():
            schoolClass = schoolClassQuery[0]
        else:
            schoolClass = SchoolClass(school=school, name=schoolClassName, universalName='')
            schoolClass.save()
        return schoolClass
    
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
        'e_ball_1','e_ball_2','e_ball_3',
        'x_jirou', 'x_shuifen', 'x_jichudaixie')

class StudentEvaluationSerializer(serializers.ModelSerializer):
    student = serializers.HyperlinkedIdentityField(view_name='sportsman:Student-detail', format='html')
    certificate = serializers.SerializerMethodField()
    
    def get_certificate(self, obj):
        request = self.context.get('request', None)
        student_evaluation_id = obj.id
        return reverse('sportsman:studentEvaluationCertificateForAPI', args=[student_evaluation_id], request=request)

    class Meta:
        model = StudentEvaluation
        fields = ('id', 'student', 'certificate', 'p_bal', 'p_shh', 'p_sws', 'p_20m', 'p_su', 'p_ls', 'p_rb', 'p_lauf', 'p_ball', 'p_height', 'p_weight', 'p_bmi', 'is_talent', 'is_frail', 'overall_score')