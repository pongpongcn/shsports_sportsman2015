from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import tempfile, os
from scipy.stats import norm
from django.conf import settings

from .models import TestPlan
from .models import StudentEvaluation
from .models import Student
from .serializers import StudentSerializer, StudentCreateSerializer, StudentEvaluationSerializer

from .utils.certificate_generator import CertificateGenerator

test_plan_id_field_name = 'p_id'

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
        available_test_plans = self.get_available_test_plans()
        
        context['test_plan'] = test_plan
        context['district'] = district
        context['available_test_plans'] = available_test_plans
        context['test_plan_id_field_name'] = test_plan_id_field_name
        context['talent_rankings'] = self.get_talent_rankings(test_plan=test_plan, district=district)
        context['frail_rankings'] = self.get_frail_rankings(test_plan=test_plan, district=district)
        context['local_statistics'] = self.get_statistics(test_plan=test_plan,district=district)
        context['global_statistics'] = self.get_statistics(test_plan=test_plan,district=None)
        
        return context
    
    def get_current_test_plan(self):
        try:
            test_plan_id = int(self.request.GET.get(test_plan_id_field_name))
        except:
            test_plan_id = None

        available_test_plans = self.get_available_test_plans()
        
        if test_plan_id != None:
            for test_plan in available_test_plans:
                if test_plan.id == test_plan_id:
                    return test_plan
            return None
        else:
            if len(available_test_plans) > 0:
                return available_test_plans[0]
            else:
                return None

    def get_current_district(self):
        currentUser = self.request.user
        if currentUser.groups.filter(name='district_users').count() > 0:
            district = None
            try:
                userprofile = currentUser.userprofile
                if userprofile.district != None:
                    district = currentUser.userprofile.district
            except:
                pass
            return district
        else:
            return None
    
    def get_available_test_plans(self):
        test_plans = list(TestPlan.objects.filter(isPublished=True).order_by('-startDate', '-endDate'))
        return test_plans
    
    def get_talent_rankings(self, test_plan, district=None):
        if test_plan == None:
            return []
        
        ranking_query = StudentEvaluation.objects.select_related('student','student__schoolClass','student__schoolClass__school','student__schoolClass__school__district').filter(testPlan=test_plan, is_talent=True)
        if district != None:
            ranking_query = ranking_query.filter(student__schoolClass__school__district=district)
            
        talent_ranking_list = ranking_query.order_by('talent_rank_number')
        
        return self.get_rankings(talent_ranking_list, 'talent')
        
    def get_frail_rankings(self, test_plan, district=None):
        if test_plan == None:
            return []
        
        ranking_query = StudentEvaluation.objects.select_related('student','student__schoolClass','student__schoolClass__school','student__schoolClass__school__district').filter(testPlan=test_plan, is_frail=True)
        if district != None:
            ranking_query = ranking_query.filter(student__schoolClass__school__district=district)
            
        talent_ranking_list = ranking_query.order_by('frail_rank_number')
        
        return self.get_rankings(talent_ranking_list, 'frail')
    
    def get_rankings(self, studentEvaluationsOrdered, category):
        studentEvaluationsOrdered = studentEvaluationsOrdered[:10]
    
        studentRankings = []
        
        lastScore = None
        lastNumber = 0
        lastSameCount = 1
        
        overallScoreNormParameters = settings.OVERALL_SCORE_NORM_PARAMETERS
        
        for studentEvaluation in studentEvaluationsOrdered:
            student = studentEvaluation.student
            name = '%s%s' % (student.lastName, student.firstName)
            
            overall_score_ppf = round(norm.cdf(studentEvaluation.overall_score,loc=overallScoreNormParameters.mean,scale=overallScoreNormParameters.dev), 4)
            rank_number = "{0:.2f}%".format((1 - overall_score_ppf) * 100)
                
            if studentEvaluation.overall_score == lastScore:
                district_rank_number = lastNumber
                lastSameCount += 1
            else:
                district_rank_number = lastNumber + lastSameCount
                lastScore = studentEvaluation.overall_score
                lastNumber = district_rank_number
                lastSameCount = 1
                
            studentRanking = StudentRanking(name=name,
                                gender=student.get_gender_display(),
                                birthdate=student.dateOfBirth,
                                school=student.schoolClass.school,
                                schoolClass=student.schoolClass,
                                overall_score=studentEvaluation.overall_score,
                                rank_number=rank_number,
                                district = student.schoolClass.school.district,
                                district_rank_number=district_rank_number)
            studentRankings.append(studentRanking)
            
        return studentRankings
    
    def get_student_evaluations(self, test_plan, district):
        if test_plan == None:
            return []
        
        ranking_query = StudentEvaluation.objects.filter(testPlan=test_plan, is_talent=True)
        if district != None:
            ranking_query = ranking_query.filter(student__schoolClass__school__district=district)
            
        talent_ranking_list = ranking_query.order_by('talent_rank_number')
        
        return self.get_rankings(talent_ranking_list, 'talent')
    
    def get_statistics(self, test_plan, district):
        if test_plan == None:
            studentEvaluations = []
        else:
            studentEvaluations = StudentEvaluation.objects.filter(testPlan=test_plan)
            if district is not None:
                studentEvaluations = studentEvaluations.filter(student__schoolClass__school__district=district)
        
        male_talent=studentEvaluations.filter(student__gender='MALE', is_talent=True).count()
        male_frail=studentEvaluations.filter(student__gender='MALE', is_frail=True).count()
        male_other=studentEvaluations.filter(student__gender='MALE').count() - male_talent - male_frail
        female_talent=studentEvaluations.filter(student__gender='FEMALE', is_talent=True).count()
        female_frail=studentEvaluations.filter(student__gender='FEMALE', is_frail=True).count()
        female_other=studentEvaluations.filter(student__gender='FEMALE').count() - female_talent - female_frail
        
        return StudentStatistics(male_talent=male_talent,
                                male_frail=male_frail,
                                male_other=male_other,
                                female_talent=female_talent,
                                female_frail=female_frail,
                                female_other=female_other)

                                
class StudentEvaluationListView(TemplateView):
    template_name = "sportsman/student_evaluation_list.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentEvaluationListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudentEvaluationListView, self).get_context_data(**kwargs)
        
        test_plan = self.get_current_test_plan()
        district = self.get_current_district()
        available_test_plans = self.get_available_test_plans()
        
        context['test_plan'] = test_plan
        context['district'] = district
        context['available_test_plans'] = available_test_plans
        context['test_plan_id_field_name'] = test_plan_id_field_name
        context['overall_score_rankings'] = self.get_overall_score_rankings(test_plan=test_plan, district=district)
        
        return context
        
    def get_current_test_plan(self):
        try:
            test_plan_id = int(self.request.GET.get(test_plan_id_field_name))
        except:
            test_plan_id = None

        available_test_plans = self.get_available_test_plans()
        
        if test_plan_id != None:
            for test_plan in available_test_plans:
                if test_plan.id == test_plan_id:
                    return test_plan
            return None
        else:
            if len(available_test_plans) > 0:
                return available_test_plans[0]
            else:
                return None

    def get_current_district(self):
        currentUser = self.request.user
        if currentUser.groups.filter(name='district_users').count() > 0:
            district = None
            try:
                userprofile = currentUser.userprofile
                if userprofile.district != None:
                    district = currentUser.userprofile.district
            except:
                pass
            return district
        else:
            return None
    
    def get_available_test_plans(self):
        test_plans = list(TestPlan.objects.filter(isPublished=True).order_by('-startDate', '-endDate'))
        return test_plans
    
    def get_overall_score_rankings(self, test_plan, district=None):
        if test_plan == None:
            return []
        
        ranking_query = StudentEvaluation.objects.select_related('student','student__schoolClass','student__schoolClass__school','student__schoolClass__school__district').filter(testPlan=test_plan)
        if district != None:
            ranking_query = ranking_query.filter(student__schoolClass__school__district=district)
            
        talent_ranking_list = ranking_query.order_by('-overall_score')
        
        return self.get_rankings(talent_ranking_list)

    def get_rankings(self, studentEvaluationsOrdered):
        studentRankings = []
        
        lastScore = None
        lastNumber = 0
        lastSameCount = 1
        
        overallScoreNormParameters = settings.OVERALL_SCORE_NORM_PARAMETERS
        
        for studentEvaluation in studentEvaluationsOrdered:
            student = studentEvaluation.student
            name = '%s%s' % (student.lastName, student.firstName)
            
            overall_score_ppf = round(norm.cdf(studentEvaluation.overall_score,loc=overallScoreNormParameters.mean,scale=overallScoreNormParameters.dev), 4)
            rank_number = "{0:.2f}%".format((1 - overall_score_ppf) * 100)
                
            if studentEvaluation.overall_score == lastScore:
                district_rank_number = lastNumber
                lastSameCount += 1
            else:
                district_rank_number = lastNumber + lastSameCount
                lastScore = studentEvaluation.overall_score
                lastNumber = district_rank_number
                lastSameCount = 1
                
            studentRanking = StudentRanking(name=name,
                                gender=student.get_gender_display(),
                                birthdate=student.dateOfBirth,
                                school=student.schoolClass.school,
                                schoolClass=student.schoolClass,
                                overall_score=studentEvaluation.overall_score,
                                rank_number=rank_number,
                                district = student.schoolClass.school.district,
                                district_rank_number=district_rank_number,
                                is_talent = studentEvaluation.is_talent,
                                is_frail = studentEvaluation.is_frail,
                                student_evaluation_id = studentEvaluation.id,
                                certificate_file = studentEvaluation.certificate_file)
            studentRankings.append(studentRanking)
            
        return studentRankings

@login_required
def gen_certificate(request, student_evaluation_id):
    studentEvaluations = get_student_evaluation_queryset(request)
    
    studentEvaluations = studentEvaluations.filter(pk=student_evaluation_id)
    
    '''若有options参数，则输出选项证书'''
    try:
        options = request.GET.get('options')
    except:
        options = None
    
    if options is not None:
        if len(studentEvaluations) == 1:
            studentEvaluation = studentEvaluations[0]
            
            fp = open(studentEvaluation.certificate_file.path, 'rb')
            filesize = os.path.getsize(studentEvaluation.certificate_file.path)
            filename = 'Certificate.pdf'
            
            response = StreamingHttpResponse(FileWrapper(fp), content_type='application/pdf')
            response['Content-Length'] = filesize
            response['Content-Disposition'] = "inline; filename=%s" % filename
            
            return response
    else:
        isAdmin = _is_admin(request)
        
        return _gen_certificates(studentEvaluations, isAdmin)
        
@login_required
def gen_certificates(request):
    studentEvaluations = get_student_evaluation_queryset(request)
    isAdmin = _is_admin(request)
    
    return _gen_certificates(studentEvaluations, isAdmin)

def _gen_certificates(studentEvaluations, isAdmin):
    '''
    输出PDF内容到临时文件，随后分段发送到客户端。
    从而避免内存过多消耗，同时临时文件会自动移除。
    '''
    
    fp = tempfile.NamedTemporaryFile()

    generator = CertificateGenerator(fp, isAdmin)
    
    generator.build(studentEvaluations)
    
    filesize = fp.tell()
    fp.seek(0)
    
    if len(studentEvaluations) == 1:
        filename = 'Certificate.pdf'
    else:
        filename = 'Certificates.pdf'
    
    response = StreamingHttpResponse(FileWrapper(fp), content_type='application/pdf')
    response['Content-Length'] = filesize
    response['Content-Disposition'] = "inline; filename=%s" % filename
    
    return response

def get_student_evaluation_queryset(request):
    test_plan = get_current_test_plan(request)
    district = get_current_district(request)
    
    studentEvaluations = StudentEvaluation.objects.select_related('student','student__schoolClass','student__schoolClass__school','student__schoolClass__school__district').filter(testPlan=test_plan)
    
    if district is not None:
        studentEvaluations = studentEvaluations.filter(student__schoolClass__school__district=district)
    
    return studentEvaluations

def _is_admin(request):
    district = get_current_district(request)
    if district is None:
        return True
    else:
        return False
    
def get_current_test_plan(request):
    try:
        test_plan_id = int(request.GET.get(test_plan_id_field_name))
    except:
        test_plan_id = None
    
    available_test_plans = get_available_test_plans()
    
    if test_plan_id != None:
        for test_plan in available_test_plans:
            if test_plan.id == test_plan_id:
                return test_plan
        return None
    else:
        return None

def get_current_district(request):
    currentUser = request.user
    if currentUser.groups.filter(name='district_users').count() > 0:
        district = None
        try:
            userprofile = currentUser.userprofile
            if userprofile.district != None:
                district = currentUser.userprofile.district
        except:
            pass
        return district
    else:
        return None    

def get_available_test_plans():
    test_plans = list(TestPlan.objects.filter(isPublished=True).order_by('-startDate', '-endDate'))
    return test_plans
        
'''View Models'''
class StudentRanking():
    def __init__(self, name, gender, birthdate, school, schoolClass, overall_score, rank_number, district, district_rank_number = None, is_talent = None, is_frail = None, student_evaluation_id = None, certificate_file = None):
        self.name = name
        self.gender = gender
        self.birthdate = birthdate
        self.school = school
        self.schoolClass = schoolClass
        self.overall_score = overall_score
        self.rank_number = rank_number
        self.district = district
        self.district_rank_number = district_rank_number
        self.is_talent = is_talent
        self.is_frail = is_frail
        self.student_evaluation_id = student_evaluation_id
        self.certificate_file = certificate_file

class StudentStatistics():
    def __init__(self, male_talent, male_frail, male_other, female_talent, female_frail, female_other):
        self.male_talent = male_talent
        self.male_frail = male_frail
        self.male_other = male_other
        self.female_talent = female_talent
        self.female_frail = female_frail
        self.female_other = female_other
    def _get_total(self):
        return sum((self.male_talent, self.male_frail, self.male_other, self.female_talent, self.female_frail, self.female_other))
    total = property(_get_total, None, None, '总数')
    def _get_talent(self):
        return sum((self.male_talent, self.female_talent))
    talent = property(_get_talent, None, None, '优秀')
    def _get_frail(self):
        return sum((self.male_frail, self.female_frail))
    frail = property(_get_frail, None, None, '干预')
    def _get_other(self):
        return sum((self.male_other, self.female_other))
    other = property(_get_other, None, None, '正常')
    def _get_male(self):
        return sum((self.male_talent, self.male_frail, self.male_other))
    male = property(_get_male, None, None, '男')
    def _get_female(self):
        return sum((self.female_talent, self.female_frail, self.female_other))
    female = property(_get_female, None, None, '女')

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Student.objects.filter(creator=user)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        else:
            return super(StudentViewSet, self).get_serializer_class()
            
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        
class StudentEvaluationViewSet(viewsets.ModelViewSet):
    serializer_class = StudentEvaluationSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = StudentEvaluation.objects.filter(student__creator=user)
        studentId = self.request.query_params.get('student_id', None)
        if(studentId is not None):
            queryset = queryset.filter(student__id=studentId)
        return queryset
        
@api_view(['GET'])
def gen_certificate_for_api(request, student_evaluation_id):
    studentEvaluations = StudentEvaluation.objects.filter(student__creator=request.user)
    studentEvaluations = studentEvaluations.filter(pk=student_evaluation_id)
    
    if len(studentEvaluations) == 1:
        return _gen_certificates(studentEvaluations, True)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)