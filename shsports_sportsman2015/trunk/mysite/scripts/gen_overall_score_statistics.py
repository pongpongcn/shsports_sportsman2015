from sportsman.models import StudentEvaluation
import statistics

def run():
    overallScoreValuesList = StudentEvaluation.objects.all().values_list('overall_score')
    overallScoreList = []
    for overallScoreValues in overallScoreValuesList:
        overallScore = overallScoreValues[0]
        overallScoreList.append(overallScore)
        
    overallScoreMean = round(statistics.mean(overallScoreList), 2)
    overallScoreDev = round(statistics.pstdev(overallScoreList), 2)
    print('mean: %s' % overallScoreMean)
    print('dev: %s' % overallScoreDev)