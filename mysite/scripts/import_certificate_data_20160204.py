import tablib, os
from import_export import resources, fields, widgets
from decimal import *
from sportsman.models import Student, School, SchoolClass, StudentEvaluation
from sportsman.admin import calculate_age, calculate_monthdelta, calculate_daydelta
import datetime

class StudentEvaluationResource(resources.ModelResource):
    def before_import(self, dataset, dry_run, **kwargs):
        student_ids = []
        for row in dataset.dict:
            number = int(row['number'])
            dateOfTesting = datetime.datetime.strptime(row['dateOfTesting'], '%Y-%m-%d').date()
            student = self.get_student(number=number, dateOfTesting=dateOfTesting)
            student_ids.append(student.id)
        dataset.append_col(student_ids, header='student_id')
    def before_save_instance(self, instance, dry_run):
        p_values = (instance.p_bal,instance.p_shh,instance.p_sws,instance.p_20m,instance.p_su,instance.p_ls,instance.p_rb,instance.p_lauf,instance.p_ball)
        p_total = sum(p_values)
        if p_total >= 712:
            instance.is_talent = True
        elif p_total < 350:
            instance.is_frail = True
    def get_student(self, number, dateOfTesting):
        studentQuery = Student.objects.filter(number=number, dateOfTesting=dateOfTesting)
        if studentQuery.exists():
            student = studentQuery[0]
        else:
            student = None
        return student

    student_id = fields.Field(attribute='student_id')
    potential_badminton = fields.Field(attribute='potential_badminton', widget=widgets.DecimalWidget(), column_name='Badminton')
    potential_basketball = fields.Field(attribute='potential_basketball', widget=widgets.DecimalWidget(), column_name='Basketball')
    potential_soccer = fields.Field(attribute='potential_soccer', widget=widgets.DecimalWidget(), column_name='Fußball')
    potential_gymnastics = fields.Field(attribute='potential_gymnastics', widget=widgets.DecimalWidget(), column_name='Gerätturnen')
    potential_canoe = fields.Field(attribute='potential_canoe', widget=widgets.DecimalWidget(), column_name='Kanu')
    potential_athletics_running = fields.Field(attribute='potential_athletics_running', widget=widgets.DecimalWidget(), column_name='Leichtathletik - Lauf')
    potential_athletics_sprinting_jumping_throwing = fields.Field(attribute='potential_athletics_sprinting_jumping_throwing', widget=widgets.DecimalWidget(), column_name='Leichtathletik - Sprint/Sprung/Wurf')
    potential_swimming = fields.Field(attribute='potential_swimming', widget=widgets.DecimalWidget(), column_name='Schwimmen')
    potential_table_tennis = fields.Field(attribute='potential_table_tennis', widget=widgets.DecimalWidget(), column_name='Tischtennis')
    potential_volleyball = fields.Field(attribute='potential_volleyball', widget=widgets.DecimalWidget(), column_name='Volleyball')

    class Meta:
        model = StudentEvaluation
        import_id_fields = ('student_id',)
        fields = ('p_bal','p_shh','p_sws','p_20m','p_su','p_ls','p_rb','p_lauf','p_ball','p_height','p_weight','p_bmi')
        
def run():
    datasheetPath = os.path.join(os.path.dirname(__file__), 'data/certificate-data-04.02.2016.csv')
    dataset = tablib.import_set(open(datasheetPath, encoding='utf-8').read())
    StudentEvaluationResource().import_data(dataset)
    print('Done!')
