from scipy.stats import norm
from decimal import *

from .models import Factor
from .models import Student
from .models import StudentEvaluation
from .models import UserProfile
from .models import District
from .models import School
from .models import SchoolClass
from .models import SequenceNumber
from .models import Genders
from .models import StandardParameter
from .models import TestPlan
from .models import Sport
from .models import SportPotentialFactor

def calc_percentile(original_score, mean, standard_deviation):
    r = norm.cdf(float(original_score), float(mean), float(standard_deviation))
    percentile = int(round(r, 2) * 100)
    return percentile

def calc_sport_potential(studentEvaluation, sportPotentialFactor):
    r = 0
    if studentEvaluation.p_bal is None:
        return None
    r += studentEvaluation.p_bal * Decimal(0.01) * sportPotentialFactor.weight_p_bal
    
    if studentEvaluation.p_shh is None:
        return None
    r += studentEvaluation.p_shh * Decimal(0.01) * sportPotentialFactor.weight_p_shh
    
    if studentEvaluation.p_sws is None:
        return None
    r += studentEvaluation.p_sws * Decimal(0.01) * sportPotentialFactor.weight_p_sws
    
    if studentEvaluation.p_20m is None:
        return None
    r += studentEvaluation.p_20m * Decimal(0.01) * sportPotentialFactor.weight_p_20m
    
    if studentEvaluation.p_su is None:
        return None
    r += studentEvaluation.p_su * Decimal(0.01)* sportPotentialFactor.weight_p_su
    
    if studentEvaluation.p_ls is None:
        return None
    r += studentEvaluation.p_ls * Decimal(0.01) * sportPotentialFactor.weight_p_ls
    
    if studentEvaluation.p_rb is None:
        return None
    r += studentEvaluation.p_rb * Decimal(0.01) * sportPotentialFactor.weight_p_rb
    
    if studentEvaluation.p_lauf is None:
        return None
    r += studentEvaluation.p_lauf * Decimal(0.01) * sportPotentialFactor.weight_p_lauf
    
    if studentEvaluation.p_ball is None:
        return None
    r += studentEvaluation.p_ball * Decimal(0.01) * sportPotentialFactor.weight_p_ball
    
    if studentEvaluation.p_height is None:
        return None
    r += studentEvaluation.p_height * Decimal(0.01) * sportPotentialFactor.weight_p_height
    
    if studentEvaluation.p_weight is None:
        return None
    r += studentEvaluation.p_weight * Decimal(0.01) * sportPotentialFactor.weight_p_weight
    
    if studentEvaluation.p_bmi is None:
        return None
    r += studentEvaluation.p_bmi * Decimal(0.01) * sportPotentialFactor.weight_p_bmi
    
    r += sportPotentialFactor.const
    potential = round(r, 6)
    return potential

def evaluation_student(student, factor):
    studentEvaluation = StudentEvaluation()
    studentEvaluation.student = student
    studentEvaluation.testPlan = student.testPlan

    stand_score_sum = 0
    
    if student.e_bal is not None:
        studentEvaluation.p_bal = calc_percentile(student.e_bal, factor.mean_bal, factor.standard_deviation_bal)
        stand_score_sum += studentEvaluation.p_bal
        
    if student.e_shh is not None:
        studentEvaluation.p_shh = calc_percentile(student.e_shh, factor.mean_shh, factor.standard_deviation_shh)
        stand_score_sum += studentEvaluation.p_shh
        
    if student.e_sws is not None:
        studentEvaluation.p_sws = calc_percentile(student.e_sws, factor.mean_sws, factor.standard_deviation_sws)
        stand_score_sum += studentEvaluation.p_sws
        
    if student.e_20m is not None:
        studentEvaluation.p_20m = 100 - calc_percentile(student.e_20m, factor.mean_20m, factor.standard_deviation_20m)
        stand_score_sum += studentEvaluation.p_20m
        
    if student.e_su is not None:
        studentEvaluation.p_su = calc_percentile(student.e_su, factor.mean_su, factor.standard_deviation_su)
        stand_score_sum += studentEvaluation.p_su
        
    if student.e_ls is not None:
        studentEvaluation.p_ls = calc_percentile(student.e_ls, factor.mean_ls, factor.standard_deviation_ls)
        stand_score_sum += studentEvaluation.p_ls
        
    if student.e_rb is not None:
        studentEvaluation.p_rb = calc_percentile(student.e_rb, factor.mean_rb, factor.standard_deviation_rb)
        stand_score_sum += studentEvaluation.p_rb
        
    if student.e_lauf is not None:
        studentEvaluation.p_lauf = calc_percentile(student.e_lauf, factor.mean_lauf, factor.standard_deviation_lauf)
        stand_score_sum += studentEvaluation.p_lauf
        
    if student.e_ball is not None:
        studentEvaluation.p_ball = calc_percentile(student.e_ball, factor.mean_ball, factor.standard_deviation_ball)
        stand_score_sum += studentEvaluation.p_ball
        
    if student.height is not None:
        studentEvaluation.p_height = calc_percentile(student.height, factor.mean_height, factor.standard_deviation_height)
    if student.weight is not None:
        studentEvaluation.p_weight = calc_percentile(student.weight, factor.mean_weight, factor.standard_deviation_weight)
    if student.bmi is not None:
        studentEvaluation.p_bmi = calc_percentile(student.bmi, factor.mean_bmi, factor.standard_deviation_bmi)

        
    studentEvaluation.overall_score = stand_score_sum
            
    studentEvaluation.save()

def potential_student(studentEvaluation, sportPotentialFactors):
    for sportPotentialFactor in sportPotentialFactors:
        sport_code = sportPotentialFactor.sport.code
        potential = calc_sport_potential(studentEvaluation, sportPotentialFactor)
        
        exec('studentEvaluation.potential_'+sport_code+'='+str(potential))

    studentEvaluation.save()