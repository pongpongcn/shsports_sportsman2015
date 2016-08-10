from import_export import resources, fields
from decimal import Decimal
import pinyin

from .models import Student
from .models import StandardParameter
from .models import Factor
from .models import School
from .models import SchoolClass
from .models import Sport
from .models import SportPotentialFactor

class StandardParameterResource(resources.ModelResource):
    class Meta:
        model = StandardParameter
        import_id_fields = ('version', 'gender','age','percentile')
        exclude = ('id',)
        
class FactorResource(resources.ModelResource):
    class Meta:
        model = Factor
        import_id_fields = ('version', 'gender','month_age')
        exclude = ('id',)

class SportPotentialFactorImportResource(resources.ModelResource):
    def before_import(self, dataset, dry_run, **kwargs):
        sport_ids = []
        for row in dataset.dict:
            sport_code = row['sport']
            sport = self.get_sport_by_code(sport_code)
            sport_ids.append(sport.id)
        dataset.append_col(sport_ids, header='sport_id')
    def get_sport_by_code(self, code):
        sportQuery = Sport.objects.filter(code=code)
        if sportQuery.exists():
            sport = sportQuery[0]
        else:
            sport = None
        return sport
    sport_id = fields.Field(attribute='sport_id')
    class Meta:
        model = SportPotentialFactor
        import_id_fields = ('sport_id',)
        exclude = ('id',)
        fields = ('weight_p_bal', 'weight_p_shh', 'weight_p_sws', 'weight_p_20m', 'weight_p_su', 'weight_p_ls', 'weight_p_rb', 'weight_p_lauf', 'weight_p_ball', 'weight_p_height', 'weight_p_weight', 'weight_p_bmi', 'const')

class SportPotentialFactorExportResource(resources.ModelResource):
    sport = fields.Field()
    class Meta:
        model = SportPotentialFactor
        exclude = ('id',)
    def dehydrate_sport(self, sportPotentialFactor):
        return sportPotentialFactor.sport.code
    
class StudentResource(resources.ModelResource):
    numberTalentCheck = fields.Field()
    className = fields.Field()
    universalClassName = fields.Field()
    schoolName = fields.Field()
    universalSchoolName = fields.Field()
    dateOfTalentCheck = fields.Field()
    selectedForTalentCheck = fields.Field()
    addressClearance = fields.Field()
    e_20m = fields.Field()
    e_bal = fields.Field()
    e_shh = fields.Field()
    e_rb = fields.Field()
    e_sws = fields.Field()
    e_ball = fields.Field()
    e_lauf = fields.Field()
    comment = fields.Field()
    e_15m_sw = fields.Field()
    e_15m_sw_bbs = fields.Field()
    e_15m_sw_ns = fields.Field()
    e_10m_ped_1 = fields.Field()
    e_10m_ped_2 = fields.Field()
    e_10m_ped = fields.Field()
    e_tt_15s_1 = fields.Field()
    e_tt_15s_2 = fields.Field()
    e_tt_15s = fields.Field()
    e_fb_drib_ob_1 = fields.Field()
    e_fb_drib_ob_2 = fields.Field()
    e_fb_drib_ob = fields.Field()
    e_fb_drib_mb_1 = fields.Field()
    e_fb_drib_mb_2 = fields.Field()
    e_fb_drib_mb = fields.Field()
    z_20m = fields.Field()
    z_bal = fields.Field()
    z_shh = fields.Field()
    z_rb = fields.Field()
    z_sws = fields.Field()
    z_ball = fields.Field()
    z_lauf = fields.Field()
    z_ls = fields.Field()
    z_su = fields.Field()
    z_10m_ped = fields.Field()
    z_15m_sw = fields.Field()
    z_fb_drib_mb = fields.Field()
    z_fb_drib_ob = fields.Field()
    z_tt_15s = fields.Field()
    z_slauf_10 = fields.Field()
    z_height = fields.Field()
    z_weight = fields.Field()
    z_bmi = fields.Field()
    p_20m = fields.Field()
    p_bal = fields.Field()
    p_shh = fields.Field()
    p_rb = fields.Field()
    p_ls = fields.Field()
    p_su = fields.Field()
    p_sws = fields.Field()
    p_ball = fields.Field()
    p_lauf = fields.Field()
    p_height = fields.Field()
    p_weight = fields.Field()
    p_bmi = fields.Field()
    p_10m_ped = fields.Field()
    p_15m_sw = fields.Field()
    p_fb_drib_mb = fields.Field()
    p_fb_drib_ob = fields.Field()
    p_tt_15s = fields.Field()
    p_slauf_10 = fields.Field()
    error = fields.Field()
    
    class Meta:
        model = Student
        export_order = ('id','firstName','lastName','universalFirstName','universalLastName','street','housenumber','addition','zip','city','gender','questionary','number','numberTalentCheck','weight','height','dateOfBirth','className','universalClassName','schoolName','universalSchoolName','dateOfTesting','dateOfTalentCheck','selectedForTalentCheck','addressClearance','e_20m_1','e_20m_2','e_20m','e_bal60_1','e_bal60_2','e_bal45_1','e_bal45_2','e_bal30_1','e_bal30_2','e_bal','e_shh_1s','e_shh_1f','e_shh_2s','e_shh_2f','e_shh','e_rb_1','e_rb_2','e_rb','e_ls','e_su','e_sws_1','e_sws_2','e_sws','e_ball_1','e_ball_2','e_ball_3','e_ball','e_lauf_runden','e_lauf_rest','e_lauf','comment','e_15m_sw','e_15m_sw_bbs','e_15m_sw_ns','e_10m_ped_1','e_10m_ped_2','e_10m_ped','e_slauf_10','e_tt_15s_1','e_tt_15s_2','e_tt_15s','e_fb_drib_ob_1','e_fb_drib_ob_2','e_fb_drib_ob','e_fb_drib_mb_1','e_fb_drib_mb_2','e_fb_drib_mb','z_20m','z_bal','z_shh','z_rb','z_sws','z_ball','z_lauf','z_ls','z_su','z_10m_ped','z_15m_sw','z_fb_drib_mb','z_fb_drib_ob','z_tt_15s','z_slauf_10','z_height','z_weight','z_bmi','p_20m','p_bal','p_shh','p_rb','p_ls','p_su','p_sws','p_ball','p_lauf','p_height','p_weight','p_bmi','p_10m_ped','p_15m_sw','p_fb_drib_mb','p_fb_drib_ob','p_tt_15s','p_slauf_10','error')
        fields = ('id','firstName','lastName','universalFirstName','universalLastName','street','housenumber','addition','zip','city','gender','questionary','number','weight','height','dateOfBirth','dateOfTesting','e_20m_1','e_20m_2','e_bal60_1','e_bal60_2','e_bal45_1','e_bal45_2','e_bal30_1','e_bal30_2','e_shh_1s','e_shh_1f','e_shh_2s','e_shh_2f','e_rb_1','e_rb_2','e_ls','e_su','e_sws_1','e_sws_2','e_ball_1','e_ball_2','e_ball_3','e_lauf_runden','e_lauf_rest','e_slauf_10','error')
    def dehydrate_className(self, student):
        if student.schoolClass:
            return student.schoolClass.name
        else:
            return None
    def dehydrate_universalClassName(self, student):
        if student.schoolClass:
            return student.schoolClass.universalName
        else:
            return None
    def dehydrate_schoolName(self, student):
        if student.schoolClass:
            return student.schoolClass.school.name
        else:
            return None
    def dehydrate_universalSchoolName(self, student):
        if student.schoolClass:
            return student.schoolClass.school.universalName
        else:
            return None
    def dehydrate_selectedForTalentCheck(self, student):
        return 'false'
    def dehydrate_addressClearance(self, student):
        return 'true' if student.addressClearance else 'false'

    def dehydrate_weight(self, student):
        if student.weight != None:
            return student.weight
        else:
            return Decimal('0.00')
    def dehydrate_height(self, student):
        if student.height != None:
            return round(Decimal(student.height), 2)
        else:
            return Decimal('0.00')
    def dehydrate_e_20m_1(self, student):
        if student.e_20m_1 != None:
            return student.e_20m_1
        else:
            return Decimal('0.00')
    def dehydrate_e_20m_2(self, student):
        if student.e_20m_2 != None:
            return student.e_20m_2
        else:
            return Decimal('0.00')
    def dehydrate_e_bal60_1(self, student):
        if student.e_bal60_1 != None:
            return student.e_bal60_1
        else:
            return 0
    def dehydrate_e_bal60_2(self, student):
        if student.e_bal60_2 != None:
            return student.e_bal60_2
        else:
            return 0
    def dehydrate_e_bal45_1(self, student):
        if student.e_bal45_1 != None:
            return student.e_bal45_1
        else:
            return 0
    def dehydrate_e_bal45_2(self, student):
        if student.e_bal45_2 != None:
            return student.e_bal45_2
        else:
            return 0
    def dehydrate_e_bal30_1(self, student):
        if student.e_bal30_1 != None:
            return student.e_bal30_1
        else:
            return 0
    def dehydrate_e_bal30_2(self, student):
        if student.e_bal30_2 != None:
            return student.e_bal30_2
        else:
            return 0
    def dehydrate_e_shh_1s(self, student):
        if student.e_shh_1s != None:
            return student.e_shh_1s
        else:
            return 0
    def dehydrate_e_shh_1f(self, student):
        if student.e_shh_1f != None:
            return student.e_shh_1f
        else:
            return 0
    def dehydrate_e_shh_2s(self, student):
        if student.e_shh_2s != None:
            return student.e_shh_2s
        else:
            return 0
    def dehydrate_e_shh_2f(self, student):
        if student.e_shh_2f != None:
            return student.e_shh_2f
        else:
            return 0
    def dehydrate_e_rb_1(self, student):
        if student.e_rb_1 != None:
            return student.e_rb_1
        else:
            return Decimal('0.00')
    def dehydrate_e_rb_2(self, student):
        if student.e_rb_2 != None:
            return student.e_rb_2
        else:
            return Decimal('0.00')
    def dehydrate_e_ls(self, student):
        if student.e_ls != None:
            return student.e_ls
        else:
            return 0
    def dehydrate_e_su(self, student):
        if student.e_su != None:
            return student.e_su
        else:
            return 0
    def dehydrate_e_sws_1(self, student):
        if student.e_sws_1 != None:
            return student.e_sws_1
        else:
            return Decimal('0.00')
    def dehydrate_e_sws_2(self, student):
        if student.e_sws_2 != None:
            return student.e_sws_2
        else:
            return Decimal('0.00')
    def dehydrate_e_ball_1(self, student):
        if student.e_ball_1 != None:
            return student.e_ball_1
        else:
            return Decimal('0.00')
    def dehydrate_e_ball_2(self, student):
        if student.e_ball_2 != None:
            return student.e_ball_2
        else:
            return Decimal('0.00')
    def dehydrate_e_ball_3(self, student):
        if student.e_ball_3 != None:
            return student.e_ball_3
        else:
            return Decimal('0.00')
    def dehydrate_e_lauf_runden(self, student):
        if student.e_lauf_runden != None:
            return student.e_lauf_runden
        else:
            return 0
    def dehydrate_e_lauf_rest(self, student):
        if student.e_lauf_rest != None:
            return student.e_lauf_rest
        else:
            return 0
    
    def dehydrate_e_20m(self, student):
        values = (student.e_20m_1, student.e_20m_2)
        if all(value != None for value in values):
            return min(values)
        else:
            return Decimal('0.00')
    def dehydrate_e_bal(self, student):
        values = (student.e_bal60_1, student.e_bal60_2, student.e_bal45_1, student.e_bal45_2, student.e_bal30_1, student.e_bal30_2)
        if all(value != None for value in values):
            return sum(values)
        else:
            return 0
    def dehydrate_e_shh(self, student):
        values = (student.e_shh_1s, student.e_shh_1f, student.e_shh_2s, student.e_shh_2f)
        if all(value != None for value in values):
            return round(Decimal((student.e_shh_1s - student.e_shh_1f + student.e_shh_2s - student.e_shh_2f) / 2), 2)
        else:
            return Decimal('0.00')
    def dehydrate_e_rb(self, student):
        values = (student.e_rb_1, student.e_rb_2)
        if all(value != None for value in values):
            return max(values)
        else:
            return Decimal('0.00')
    def dehydrate_e_sws(self, student):
        values = (student.e_sws_1, student.e_sws_2)
        if all(value != None for value in values):
            return max(values)
        else:
            return Decimal('0.00')
    def dehydrate_e_ball(self, student):
        values = (student.e_ball_1, student.e_ball_2, student.e_ball_3)
        if all(value != None for value in values):
            return max(values)
        else:
            return Decimal('0.00')
    def dehydrate_e_lauf(self, student):
        values = (student.e_lauf_runden, student.e_lauf_rest)
        if all(value != None for value in values):
            return student.e_lauf_runden * 54 + student.e_lauf_rest
        else:
            return 0
    def dehydrate_error(self, student):
        return check_student_error(student)

class StudentImportResource(resources.ModelResource):
    def before_import(self, dataset, dry_run, **kwargs):
        schoolClasses = []
        genders = []
        universalFirstNames = []
        universalLastNames = []
        for row in dataset.dict:
            schoolClass = self.get_schoolClass(row['学校'], row['班级'])
            schoolClasses.append(schoolClass)
            gender = self.get_gender(row['性别'])
            genders.append(gender)
            universalFirstNames.append(pinyin.get(row['名'], format="strip").capitalize())
            universalLastNames.append(pinyin.get(row['姓'], format="strip").capitalize())
        dataset.append_col(schoolClasses, header='schoolClass')
        dataset.append_col(genders, header='gender')
        dataset.append_col(universalFirstNames, header='universalFirstName')
        dataset.append_col(universalLastNames, header='universalLastName')
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
    def get_gender(self, genderName):
        if genderName == '男':
            return 'MALE'
        elif genderName == '女':
            return 'FEMALE'
        else:
            return None

    noOfStudentStatus = fields.Field(attribute='noOfStudentStatus', column_name='学籍号')
    firstName = fields.Field(attribute='firstName', column_name='名')
    lastName = fields.Field(attribute='lastName', column_name='姓')
    dateOfBirth = fields.Field(attribute='dateOfBirth', column_name='出生日期')
    dateOfTesting = fields.Field(attribute='dateOfTesting', column_name='测试日期')
    schoolClass = fields.Field(attribute='schoolClass')
    gender = fields.Field(attribute='gender')
    universalFirstName = fields.Field(attribute='universalFirstName', column_name='First Name')
    universalLastName = fields.Field(attribute='universalLastName', column_name='Last Name')
    class Meta:
        model = Student
        import_id_fields = ('noOfStudentStatus',)
        fields = ()
        #Does not working until now.
        skip_unchanged = True
        
def check_student_error(student):
    if not (student.weight != None and student.weight >= 10 and student.weight <= 100):
        return '体重'
    if not (student.height != None and student.height >= 80 and student.height <= 210):
        return '身高'
    e_20m_values = (student.e_20m_1, student.e_20m_2)
    if not all(value != None and value >=3.00 and value <= 9.00 for value in e_20m_values):
        return '20米跑'
    e_bal_values = (student.e_bal60_1, student.e_bal60_2, student.e_bal45_1, student.e_bal45_2, student.e_bal30_1, student.e_bal30_2)
    if not all(value != None and value >=0 and value <= 8 for value in e_bal_values):
        return '后退平衡'
    e_shh_values = (student.e_shh_1s, student.e_shh_1f, student.e_shh_2s, student.e_shh_2f)        
    if not (all(value != None for value in e_shh_values) and (student.e_shh_1s >= 8 and student.e_shh_1s <= 80 and student.e_shh_2s >= 8 and student.e_shh_2s <= 80 and student.e_shh_1f >=0 and student.e_shh_1f <= student.e_shh_1s and student.e_shh_2f >=0 and student.e_shh_2f <= student.e_shh_2s)):
        return '侧向跳'
    e_rb_values = (student.e_rb_1, student.e_rb_2)
    if not all(value != None and value >= -35 and value <= 35 for value in e_rb_values):
        return '立位体前屈'
    if not (student.e_ls != None and student.e_ls >= 0 and student.e_ls <=60):
        return '俯卧撑'
    if not (student.e_su != None and student.e_su >= 0 and student.e_su <=60):
        return '仰卧起坐'
    e_sws_values = (student.e_sws_1, student.e_sws_2)
    if not all(value != None and value >=20 and value <= 300 for value in e_sws_values):
        return '立定跳远'
    if not (student.e_lauf_runden != None and student.e_lauf_runden >= 0 and student.e_lauf_runden <= 30 and student.e_lauf_rest != None and student.e_lauf_rest >= 0 and student.e_lauf_rest <= 53):
        return '6分钟跑'
    e_ball_values = (student.e_ball_1, student.e_ball_2, student.e_ball_3)
    if not all(value != None and value >=0 and value <= 30 for value in e_ball_values):
        return '投掷球'
    return None