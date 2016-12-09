from sportsman.models import OverallScoreNormParameters
import statistics

def genOverallScoreNormParameters(overallScoreList):   
    overallScoreMean = round(statistics.mean(overallScoreList), 2)
    overallScoreDev = round(statistics.pstdev(overallScoreList), 2)
    
    return OverallScoreNormParameters(overallScoreMean, overallScoreDev)
    