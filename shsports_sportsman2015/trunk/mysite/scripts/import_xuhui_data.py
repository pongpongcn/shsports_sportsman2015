import tablib
from import_export import resources, fields
from decimal import *
from sportsman.models import Student, School, SchoolClass, StudentEvaluation
from sportsman.admin import calculate_age, calculate_monthdelta, calculate_daydelta

class StudentResource(resources.ModelResource):
    def before_import(self, dataset, dry_run, **kwargs):
        noOfStudentStatuses = []
        schoolClasses = []
        for row in dataset.dict:
            noOfStudentStatus = 'Data_Shanghai-Movement-Check_2015_' + row['id']
            noOfStudentStatuses.append(noOfStudentStatus)
            schoolClass = self.get_schoolClass(row['schoolName'], row['className'], row['universalSchoolName'])
            schoolClasses.append(schoolClass)
        dataset.append_col(noOfStudentStatuses, header='noOfStudentStatus')
        dataset.append_col(schoolClasses, header='schoolClass')
    def get_schoolClass(self, schoolName, schoolClassName, universalSchoolName):
        schoolQuery = School.objects.filter(name=schoolName)
        if schoolQuery.exists():
            school = schoolQuery[0]
        else:
            school = School(name=schoolName, universalName=universalSchoolName)
            school.save()
        schoolClassQuery = SchoolClass.objects.filter(school=school, name=schoolClassName)
        if schoolClassQuery.exists():
            schoolClass = schoolClassQuery[0]
        else:
            schoolClass = SchoolClass(school=school, name=schoolClassName, universalName=schoolClassName)
            schoolClass.save()
        return schoolClass
    
    noOfStudentStatus = fields.Field(attribute='noOfStudentStatus')
    schoolClass = fields.Field(attribute='schoolClass')

    class Meta:
        model = Student
        import_id_fields = ('noOfStudentStatus',)
        fields = ('firstName', 'lastName', 'universalFirstName', 'universalLastName', 'gender', 'dateOfBirth', 'dateOfTesting', 'number', 'street', 'housenumber', 'addition', 'zip', 'city', 'height', 'weight', 'e_20m_1', 'e_20m_2', 'e_bal30_1', 'e_bal30_2', 'e_bal45_1', 'e_bal45_2', 'e_bal60_1', 'e_bal60_2', 'e_ball_1', 'e_ball_2', 'e_ball_3', 'e_lauf_rest', 'e_lauf_runden', 'e_ls', 'e_rb_1', 'e_rb_2', 'e_shh_1f', 'e_shh_1s', 'e_shh_2f', 'e_shh_2s', 'e_slauf_10', 'e_su', 'e_sws_1', 'e_sws_2')
        widgets = {
            'dateOfBirth': {'format': '%Y/%m/%d'},
            'dateOfTesting': {'format': '%Y/%m/%d'},
        }
class StudentEvaluationResource(resources.ModelResource):
    def before_import(self, dataset, dry_run, **kwargs):
        student_ids = []
        ages = []
        month_ages = []
        day_ages = []
        bmis = []
        score_sums = []
        percentage_bals = []
        percentage_shhs = []
        percentage_swses = []
        percentage_20ms = []
        percentage_sus = []
        percentage_lses = []
        percentage_rbs = []
        percentage_laufs = []
        percentage_balls = []
        for row in dataset.dict:
            noOfStudentStatus = 'Data_Shanghai-Movement-Check_2015_' + row['id']
            student = self.get_student(noOfStudentStatus)
            student_ids.append(student.id)
            age = calculate_age(student.dateOfBirth, student.dateOfTesting)
            ages.append(age)
            month_age = calculate_monthdelta(student.dateOfBirth, student.dateOfTesting)
            month_ages.append(month_age)
            day_age = calculate_daydelta(student.dateOfBirth, student.dateOfTesting)
            day_ages.append(day_age)
            bmi = round(student.weight / (student.height * Decimal(0.01)) ** 2, 1)
            bmis.append(bmi)
            percentage_bal = Decimal(row['p_bal']) * Decimal(0.01)
            percentage_bals.append(percentage_bal)
            percentage_shh = Decimal(row['p_shh']) * Decimal(0.01)
            percentage_shhs.append(percentage_shh)
            percentage_sws = Decimal(row['p_sws']) * Decimal(0.01)
            percentage_swses.append(percentage_sws)
            percentage_20m = Decimal(row['p_20m']) * Decimal(0.01)
            percentage_20ms.append(percentage_20m)
            percentage_su = Decimal(row['p_su']) * Decimal(0.01)
            percentage_sus.append(percentage_su)
            percentage_ls = Decimal(row['p_ls']) * Decimal(0.01)
            percentage_lses.append(percentage_ls)
            percentage_rb = Decimal(row['p_rb']) * Decimal(0.01)
            percentage_rbs.append(percentage_rb)
            percentage_lauf = Decimal(row['p_lauf']) * Decimal(0.01)
            percentage_laufs.append(percentage_lauf)
            percentage_ball = Decimal(row['p_ball']) * Decimal(0.01)
            percentage_balls.append(percentage_ball)
            score_sum = 0
            score_sum += percentage_bal * 100
            score_sum += percentage_shh * 100
            score_sum += percentage_sws * 100
            score_sum += percentage_20m * 100
            score_sum += percentage_su * 100
            score_sum += percentage_ls * 100
            score_sum += percentage_rb * 100
            score_sum += percentage_lauf * 100
            score_sum += percentage_ball * 100
            score_sums.append(score_sum)
        dataset.append_col(student_ids, header='student_id')
        dataset.append_col(ages, header='age')
        dataset.append_col(month_ages, header='month_age')
        dataset.append_col(day_ages, header='day_age')
        dataset.append_col(bmis, header='bmi')
        dataset.append_col(score_sums, header='score_sum')
        dataset.append_col(percentage_bals, header='percentage_bal')
        dataset.append_col(percentage_shhs, header='percentage_shh')
        dataset.append_col(percentage_swses, header='percentage_sws')
        dataset.append_col(percentage_20ms, header='percentage_20m')
        dataset.append_col(percentage_sus, header='percentage_su')
        dataset.append_col(percentage_lses, header='percentage_ls')
        dataset.append_col(percentage_rbs, header='percentage_rb')
        dataset.append_col(percentage_laufs, header='percentage_lauf')
        dataset.append_col(percentage_balls, header='percentage_ball')
    def get_student(self, noOfStudentStatus):
        studentQuery = Student.objects.filter(noOfStudentStatus=noOfStudentStatus)
        if studentQuery.exists():
            student = studentQuery[0]
        else:
            student = None
        return student

    student_id = fields.Field(attribute='student_id')
    original_score_bal = fields.Field(attribute='original_score_bal', column_name='e_bal')
    original_score_shh = fields.Field(attribute='original_score_shh', column_name='e_shh')
    original_score_sws = fields.Field(attribute='original_score_sws', column_name='e_sws')
    original_score_20m = fields.Field(attribute='original_score_20m', column_name='e_20m')
    original_score_su = fields.Field(attribute='original_score_su', column_name='e_su')
    original_score_ls = fields.Field(attribute='original_score_ls', column_name='e_ls')
    original_score_rb = fields.Field(attribute='original_score_rb', column_name='e_rb')
    original_score_lauf = fields.Field(attribute='original_score_lauf', column_name='e_lauf')
    original_score_ball = fields.Field(attribute='original_score_ball', column_name='e_ball')

    class Meta:
        model = StudentEvaluation
        import_id_fields = ('student_id',)
        fields = ('age','month_age','day_age','bmi','score_sum','percentage_bal','percentage_shh','percentage_sws','percentage_20m','percentage_su','percentage_ls','percentage_rb','percentage_lauf','percentage_ball')
        
def run():
    dataset = tablib.import_set(open('Data_Shanghai-Movement-Check_2015.csv').read())
    StudentResource().import_data(dataset, dry_run=False)
    StudentEvaluationResource().import_data(dataset, dry_run=False)
    print('Done!')
