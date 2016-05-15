from django.test import TestCase
from decimal import *
import datetime
from .services import *
from .models import School
from .models import SchoolClass
from .models import Student
from .models import TestPlan
from .models import Factor
from .models import Sport
from .models import SportPotentialFactor

# Create your tests here.
class ServicesTests(TestCase):
    def test_calc_percentile(self):
        original_score = Decimal(5)
        mean = Decimal(5)
        standard_deviation = Decimal(0.1)
        
        self.assertEqual(calc_percentile(original_score, mean, standard_deviation), 50)
        
class StudentTests(TestCase):
    def setUp(self):
        school = School.objects.create(name="宝山区实验小学", universalName="Baoshan District Experimental Primary School")
        school_class = SchoolClass.objects.create(school=school, name="二(2)", universalName="Class 2, Grade 2")
        Factor.objects.create(version="china_201604",
                                month_age=91,
                                gender="FEMALE",
                                mean_20m=4.76,
                                standard_deviation_20m=0.3279,
                                mean_bal=32.13,
                                standard_deviation_bal=7.3036,
                                mean_shh=23.77,
                                standard_deviation_shh=4.5920,
                                mean_rb=9.35,
                                standard_deviation_rb=5.3828,
                                mean_ls=12.54,
                                standard_deviation_ls=3.0825,
                                mean_su=10.73,
                                standard_deviation_su=5.5416,
                                mean_sws=121.62,
                                standard_deviation_sws=15.0047,
                                mean_ball=7.83,
                                standard_deviation_ball=1.8389,
                                mean_lauf=821.32,
                                standard_deviation_lauf=74.5622,
                                mean_weight=24.24,	
                                standard_deviation_weight=3.8137,
                                mean_height=126.1,
                                standard_deviation_height=5.0556,
                                mean_bmi=15.2,
                                standard_deviation_bmi=1.6041)
        sport = Sport.objects.create(code="badminton", name="羽毛球", universalName="badminton")
        SportPotentialFactor.objects.create(sport=sport,
                                weight_p_bal=0.0000,
                                weight_p_shh=0.1613,
                                weight_p_sws=0.0323,
                                weight_p_20m=0.0645,
                                weight_p_su=0.0000,
                                weight_p_ls=0.0000,
                                weight_p_rb=0.0000,
                                weight_p_lauf=0.0645,
                                weight_p_ball=0.0968,
                                weight_p_height=0.0565,
                                weight_p_weight=0.0000,
                                weight_p_bmi=-0.0242,
                                const=0.5242)
        test_plan = TestPlan.objects.create(name="2015年10月上海运动能力测试", startDate=datetime.date(2015, 10, 28), endDate=datetime.date(2016, 1, 20))
        Student.objects.create(noOfStudentStatus="3101130001120140233",
                                testPlan=test_plan,
                                schoolClass=school_class,
                                firstName="一",
                                lastName="丁",
                                universalFirstName="Yi",
                                universalLastName="Ding",
                                gender="FEMALE",
                                dateOfBirth=datetime.date(2008, 3, 31),
                                dateOfTesting=datetime.date(2015, 11, 20),
                                number=71,
                                weight=39.10,
                                height=129,
                                e_bal30_1=1,
                                e_bal30_2=5,
                                e_bal45_1=2,
                                e_bal45_2=1,
                                e_bal60_1=2,
                                e_bal60_2=3,
                                e_shh_1f=2,
                                e_shh_1s=22,
                                e_shh_2f=3,
                                e_shh_2s=24,
                                e_sws_1=123.00,
                                e_sws_2=130.00,
                                e_20m_1=4.68,
                                e_20m_2=4.73,
                                e_su=11,
                                e_ls=18,
                                e_rb_1=17.70,
                                e_rb_2=17.20,
                                e_lauf_runden=12,
                                e_lauf_rest=26,
                                e_ball_1=5.20,
                                e_ball_2=8.10,
                                e_ball_3=4.80)
    
    def test_evaluation_student(self):
        student = Student.objects.filter(noOfStudentStatus="3101130001120140233")[0]
        factor = Factor.objects.filter(version="china_201604", month_age=student.months_of_age, gender=student.gender)[0]
        evaluation_student(student, factor)
        studentevaluation = student.studentevaluation
        sportPotentialFactors = SportPotentialFactor.objects.all()
        potential_student(studentevaluation, sportPotentialFactors)
        