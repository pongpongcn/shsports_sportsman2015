import tablib, os, datetime
from import_export import resources, fields, widgets
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
        for row in dataset.dict:
            number = int(row['number'])
            dateOfTesting = datetime.datetime.strptime(row['dateOfTesting'], '%Y/%m/%d').date()
            student = self.get_student(number=number, dateOfTesting=dateOfTesting)
            student_ids.append(student.id)
        dataset.append_col(student_ids, header='student_id')
    def before_save_instance(self, instance, dry_run):
        #根据名单
        #instance.is_talent = True
        #根据证书
        #instance.is_frail = True
        potential_items = []
        potential_items.append(self.PotentialItem('badminton', instance.potential_badminton))
        potential_items.append(self.PotentialItem('basketball', instance.potential_basketball))
        potential_items.append(self.PotentialItem('soccer', instance.potential_soccer))
        potential_items.append(self.PotentialItem('gymnastics', instance.potential_gymnastics))
        potential_items.append(self.PotentialItem('canoe', instance.potential_canoe))
        potential_items.append(self.PotentialItem('discus', instance.potential_discus))
        potential_items.append(self.PotentialItem('shot_put', instance.potential_shot_put))
        potential_items.append(self.PotentialItem('pole_vault', instance.potential_pole_vault))
        potential_items.append(self.PotentialItem('high_jump', instance.potential_high_jump))
        potential_items.append(self.PotentialItem('javelin', instance.potential_javelin))
        potential_items.append(self.PotentialItem('long_jump', instance.potential_long_jump))
        potential_items.append(self.PotentialItem('huerdles', instance.potential_huerdles))
        potential_items.append(self.PotentialItem('sprint', instance.potential_sprint))
        potential_items.append(self.PotentialItem('rowing', instance.potential_rowing))
        potential_items.append(self.PotentialItem('swimming', instance.potential_swimming))
        potential_items.append(self.PotentialItem('tennis', instance.potential_tennis))
        potential_items.append(self.PotentialItem('table_tennis', instance.potential_table_tennis))
        potential_items.append(self.PotentialItem('volleyball', instance.potential_volleyball))
        potential_items.sort(key=lambda item: item.value, reverse=True)
        temp_potential_item_names = []
        if instance.is_frail != True:
            for potential_item in potential_items[:3]:
                temp_potential_item_names.append(potential_item.name)

        certificate_template = 'ShanghaiMovementCheck2015'
        certificate_data = {'template':certificate_template, 'potential_items':temp_potential_item_names}
        instance.certificate_data = json.dumps(certificate_data)
    def get_student(self, number, dateOfTesting):
        studentQuery = Student.objects.filter(number=number, dateOfTesting=dateOfTesting)
        if studentQuery.exists():
            student = studentQuery[0]
        else:
            student = None
        return student

    student_id = fields.Field(attribute='student_id')
    potential_badminton = fields.Field(attribute='potential_badminton', widget=widgets.DecimalWidget(), column_name='badminton')
    potential_basketball = fields.Field(attribute='potential_basketball', widget=widgets.DecimalWidget(), column_name='basketball')
    potential_soccer = fields.Field(attribute='potential_soccer', widget=widgets.DecimalWidget(), column_name='soccer')
    potential_gymnastics = fields.Field(attribute='potential_gymnastics', widget=widgets.DecimalWidget(), column_name='gymnastics')
    potential_canoe = fields.Field(attribute='potential_canoe', widget=widgets.DecimalWidget(), column_name='canoe/kayak')
    potential_discus = fields.Field(attribute='potential_discus', widget=widgets.DecimalWidget(), column_name='discus')
    potential_shot_put = fields.Field(attribute='potential_shot_put', widget=widgets.DecimalWidget(), column_name='shot put')
    potential_pole_vault = fields.Field(attribute='potential_pole_vault', widget=widgets.DecimalWidget(), column_name='pole vault')
    potential_high_jump = fields.Field(attribute='potential_high_jump', widget=widgets.DecimalWidget(), column_name='high jump')
    potential_javelin = fields.Field(attribute='potential_javelin', widget=widgets.DecimalWidget(), column_name='javelin')
    potential_long_jump = fields.Field(attribute='potential_long_jump', widget=widgets.DecimalWidget(), column_name='long jump')
    potential_huerdles = fields.Field(attribute='potential_huerdles', widget=widgets.DecimalWidget(), column_name='huerdles')
    potential_sprint = fields.Field(attribute='potential_sprint', widget=widgets.DecimalWidget(), column_name='sprint')
    potential_rowing = fields.Field(attribute='potential_rowing', widget=widgets.DecimalWidget(), column_name='rowing')
    potential_swimming = fields.Field(attribute='potential_swimming', widget=widgets.DecimalWidget(), column_name='swimming')
    potential_tennis = fields.Field(attribute='potential_tennis', widget=widgets.DecimalWidget(), column_name='tennis')
    potential_table_tennis = fields.Field(attribute='potential_table_tennis', widget=widgets.DecimalWidget(), column_name='table tennis')
    potential_volleyball = fields.Field(attribute='potential_volleyball', widget=widgets.DecimalWidget(), column_name='volleyball')
    
    class Meta:
        model = StudentEvaluation
        import_id_fields = ('student_id',)
        fields = ('p_bal','p_shh','p_sws','p_20m','p_su','p_ls','p_rb','p_lauf','p_ball','p_height','p_weight','p_bmi')

    class PotentialItem:
        def __init__(self, name, value):
            self.name = name
            self.value = value
        
def run():
    datasheetPath = os.path.join(os.path.dirname(__file__), 'data/Data_Shanghai-Movement-Check_2015.csv')
    dataset = tablib.import_set(open(datasheetPath, encoding='utf-8').read())
    StudentResource().import_data(dataset)
    StudentEvaluationResource().import_data(dataset)
    print('Done!')
