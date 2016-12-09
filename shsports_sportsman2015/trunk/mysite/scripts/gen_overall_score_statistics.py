from sportsman.models import StudentEvaluation
import statistics
from scipy.stats import norm

def run():
    overallScoreValuesList = StudentEvaluation.objects.filter(studentDataComplete=True).values_list('overall_score')
    overallScoreList = []
    for overallScoreValues in overallScoreValuesList:
        overallScore = overallScoreValues[0]
        overallScoreList.append(overallScore)
        
    overallScoreMean = round(statistics.mean(overallScoreList), 2)
    overallScoreDev = round(statistics.pstdev(overallScoreList), 2)
    
    lq_value = int(norm.ppf(0.2,loc=overallScoreMean,scale=overallScoreDev))
    uq_value = int(norm.ppf(0.8,loc=overallScoreMean,scale=overallScoreDev))
    
    print('mean: %s' % overallScoreMean)
    print('dev: %s' % overallScoreDev)
    print('lq: %s' % lq_value)
    print('uq: %s' % uq_value)

'''
20160301
Mean: 457.3
Dev: 149.01
LQ: 331
UQ: 582

20161209
Mean: 459.67
Dev: 143.85
LQ: 338
UQ: 580
'''