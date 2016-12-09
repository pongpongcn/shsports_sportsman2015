from sportsman.models import StudentEvaluation
from scipy.stats import norm
from sportsman.utils.misc import genOverallScoreNormParameters

def run():
    overallScoreValuesList = StudentEvaluation.objects.filter(studentDataComplete=True).values_list('overall_score')
    overallScoreList = []
    for overallScoreValues in overallScoreValuesList:
        overallScore = overallScoreValues[0]
        overallScoreList.append(overallScore)
    
    overallScoreNormParameters = genOverallScoreNormParameters(overallScoreList) 
    
    lq_value = int(norm.ppf(0.2,loc=overallScoreNormParameters.mean,scale=overallScoreNormParameters.dev))
    uq_value = int(norm.ppf(0.8,loc=overallScoreNormParameters.mean,scale=overallScoreNormParameters.dev))
    
    print('mean: %s' % overallScoreNormParameters.mean)
    print('dev: %s' % overallScoreNormParameters.dev)
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