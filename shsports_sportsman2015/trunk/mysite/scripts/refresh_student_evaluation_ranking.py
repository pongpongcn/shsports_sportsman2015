import tablib, os, datetime, json
from django.db import transaction
from import_export import resources, fields, widgets
from sportsman.models import StudentEvaluation, TestPlan

def run():
    for testPlanName in ('2015年3月上海运动能力测试', '2015年10月上海运动能力测试'):
        testPlanQuery = TestPlan.objects.filter(name=testPlanName)
        if testPlanQuery.exists():
            testPlan = testPlanQuery[0]
            try:
                refresh_ranking(testPlan)
                print('Test plan %s student evaluation ranking refreshed!' % testPlanName)
            except Error:
                print(Error)
        else:
            print('Test plan %s can not be found!' % testPlanName)

def refresh_ranking(testPlan):
    studentEvaluationQuery = StudentEvaluation.objects.filter(testPlan=testPlan)
    studentEvaluations = list(studentEvaluationQuery)
    
    for studentEvaluation in studentEvaluations:
        values = (studentEvaluation.p_bal, 
studentEvaluation.p_shh, 
studentEvaluation.p_sws, 
studentEvaluation.p_20m, 
studentEvaluation.p_su, 
studentEvaluation.p_ls, 
studentEvaluation.p_rb, 
studentEvaluation.p_lauf, 
studentEvaluation.p_ball,)
        studentEvaluation.overall_score = sum(values)
    
    isTalentStudentEvaluations = []
    studentEvaluations.sort(key=lambda item: item.overall_score, reverse=True)
    for studentEvaluation in studentEvaluations:
        if studentEvaluation.is_talent:
            isTalentStudentEvaluations.append(studentEvaluation)
        else:
            break
    
    calc_talent_rank_number(isTalentStudentEvaluations)
    
    isFrailStudentEvaluations = []
    studentEvaluations.sort(key=lambda item: item.overall_score)
    for studentEvaluation in studentEvaluations:
        if studentEvaluation.is_frail:
            isFrailStudentEvaluations.append(studentEvaluation)
        else:
            break
    
    calc_frail_rank_number(isFrailStudentEvaluations)
    
    with transaction.atomic():
        for studentEvaluation in studentEvaluations:
            studentEvaluation.save()
        
def calc_talent_rank_number(studentEvaluations):
    lastScore = None
    lastNumber = 0
    lastSameCount = 1
    for studentEvaluation in studentEvaluations:
        if studentEvaluation.overall_score == lastScore:
            studentEvaluation.talent_rank_number = lastNumber
            lastSameCount += 1
        else:
            studentEvaluation.talent_rank_number = lastNumber + lastSameCount
            lastScore = studentEvaluation.overall_score
            lastNumber = studentEvaluation.talent_rank_number
            lastSameCount = 1
            
def calc_frail_rank_number(studentEvaluations):
    lastScore = None
    lastNumber = 0
    lastSameCount = 1
    for studentEvaluation in studentEvaluations:
        if studentEvaluation.overall_score == lastScore:
            studentEvaluation.frail_rank_number = lastNumber
            lastSameCount += 1
        else:
            studentEvaluation.frail_rank_number = lastNumber + lastSameCount
            lastScore = studentEvaluation.overall_score
            lastNumber = studentEvaluation.frail_rank_number
            lastSameCount = 1