from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render

from .models import District
from .models import TestPlan
from .models import StudentEvaluation

# Create your views here.
class IndexView(TemplateView):
    template_name = "sportsman/index.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        
        test_plan = self.get_current_test_plan()
        district = self.get_current_district()

        context['test_plan'] = test_plan
        context['talent_rankings'] = self.get_talent_rankings(test_plan=test_plan, district=district)
        context['frail_rankings'] = self.get_frail_rankings(test_plan=test_plan, district=district)
        
        return context
    
    def get_current_test_plan(self):
        available_test_plans = self.get_available_test_plans()
        if len(available_test_plans) > 0:
            return available_test_plans[0]
        else:
            return None
    
    def get_current_district(self):
        return District.objects.filter(name='杨浦区')[0]
    
    def get_available_test_plans(self):
        test_plans = list(TestPlan.objects.filter(isPublished=True).order_by('-startDate', '-endDate'))
        return test_plans
    
    def get_talent_rankings(self, test_plan, district=None):
        if test_plan == None:
            return []
        
        ranking_query = StudentEvaluation.objects.filter(testPlan=test_plan, is_talent=True)
        if district != None:
            ranking_query = ranking_query.filter(student__schoolClass__school__district=district)
            
        talent_ranking_list = ranking_query.order_by('talent_rank_number')
        
        return self.get_rankings(talent_ranking_list, 'talent')
        
    def get_frail_rankings(self, test_plan, district=None):
        if test_plan == None:
            return []
        
        ranking_query = StudentEvaluation.objects.filter(testPlan=test_plan, is_frail=True)
        if district != None:
            ranking_query = ranking_query.filter(student__schoolClass__school__district=district)
            
        talent_ranking_list = ranking_query.order_by('frail_rank_number')
        
        return self.get_rankings(talent_ranking_list, 'frail')
    
    def get_rankings(self, studentEvaluationsOrdered, category):
        studentRankings = []
        
        lastScore = None
        lastNumber = 0
        lastSameCount = 1
        
        for studentEvaluation in studentEvaluationsOrdered:
            student = studentEvaluation.student
            name = '%s%s' % (student.lastName, student.firstName)
            
            if category=='talent':
                rank_number = studentEvaluation.talent_rank_number
            elif category=='frail':
                rank_number = studentEvaluation.frail_rank_number
            else:
                rank_number = None
                
            if studentEvaluation.overall_score == lastScore:
                local_rank_number = lastNumber
                lastSameCount += 1
            else:
                local_rank_number = lastNumber + lastSameCount
                lastScore = studentEvaluation.overall_score
                lastNumber = local_rank_number
                lastSameCount = 1
                
            studentRanking = StudentRanking(name=name,
                                gender=student.get_gender_display(),
                                birthdate=student.dateOfBirth,
                                school=student.schoolClass.school,
                                schoolClass=student.schoolClass,
                                overall_score=studentEvaluation.overall_score,
                                rank_number=rank_number,
                                local_rank_number=local_rank_number)
            studentRankings.append(studentRanking)
            
        return studentRankings
        
'''View Models'''
class StudentRanking():
    def __init__(self, name, gender, birthdate, school, schoolClass, overall_score, rank_number, local_rank_number = None):
        self.name = name
        self.gender = gender
        self.birthdate = birthdate
        self.school = school
        self.schoolClass = schoolClass
        self.overall_score = overall_score
        self.rank_number = rank_number
        self.local_rank_number = local_rank_number