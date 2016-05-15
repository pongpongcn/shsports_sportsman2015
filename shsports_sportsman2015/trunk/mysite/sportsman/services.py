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
    r += studentEvaluation.p_bal * Decimal(0.01) * sportPotentialFactor.weight_p_bal
    r += studentEvaluation.p_shh * Decimal(0.01) * sportPotentialFactor.weight_p_shh
    r += studentEvaluation.p_sws * Decimal(0.01) * sportPotentialFactor.weight_p_sws
    r += studentEvaluation.p_20m * Decimal(0.01) * sportPotentialFactor.weight_p_20m
    r += studentEvaluation.p_su * Decimal(0.01)* sportPotentialFactor.weight_p_su
    r += studentEvaluation.p_ls * Decimal(0.01) * sportPotentialFactor.weight_p_ls
    r += studentEvaluation.p_rb * Decimal(0.01) * sportPotentialFactor.weight_p_rb
    r += studentEvaluation.p_lauf * Decimal(0.01) * sportPotentialFactor.weight_p_lauf
    r += studentEvaluation.p_ball * Decimal(0.01) * sportPotentialFactor.weight_p_ball
    r += studentEvaluation.p_height * Decimal(0.01) * sportPotentialFactor.weight_p_height
    r += studentEvaluation.p_weight * Decimal(0.01) * sportPotentialFactor.weight_p_weight
    r += studentEvaluation.p_bmi * Decimal(0.01) * sportPotentialFactor.weight_p_bmi
    r += sportPotentialFactor.const
    potential = round(r, 4)
    return potential

def evaluation_student(student, factor):
    studentEvaluation = StudentEvaluation()
    studentEvaluation.student = student
    studentEvaluation.testPlan = student.testPlan

    studentEvaluation.p_bal = calc_percentile(student.e_bal, factor.mean_bal, factor.standard_deviation_bal)
    studentEvaluation.p_shh = calc_percentile(student.e_shh, factor.mean_shh, factor.standard_deviation_shh)
    studentEvaluation.p_sws = calc_percentile(student.e_sws, factor.mean_sws, factor.standard_deviation_sws)
    studentEvaluation.p_20m = 100 - calc_percentile(student.e_20m, factor.mean_20m, factor.standard_deviation_20m)
    studentEvaluation.p_su = calc_percentile(student.e_su, factor.mean_su, factor.standard_deviation_su)
    studentEvaluation.p_ls = calc_percentile(student.e_ls, factor.mean_ls, factor.standard_deviation_ls)
    studentEvaluation.p_rb = calc_percentile(student.e_rb, factor.mean_rb, factor.standard_deviation_rb)
    studentEvaluation.p_lauf = calc_percentile(student.e_lauf, factor.mean_lauf, factor.standard_deviation_lauf)
    studentEvaluation.p_ball = calc_percentile(student.e_ball, factor.mean_ball, factor.standard_deviation_ball)
    studentEvaluation.p_height = calc_percentile(student.height, factor.mean_height, factor.standard_deviation_height)
    studentEvaluation.p_weight = calc_percentile(student.weight, factor.mean_weight, factor.standard_deviation_weight)
    studentEvaluation.p_bmi = calc_percentile(student.bmi, factor.mean_bmi, factor.standard_deviation_bmi)

    stand_score_sum = 0
    stand_score_sum += studentEvaluation.p_bal
    stand_score_sum += studentEvaluation.p_shh
    stand_score_sum += studentEvaluation.p_sws
    stand_score_sum += studentEvaluation.p_20m
    stand_score_sum += studentEvaluation.p_su
    stand_score_sum += studentEvaluation.p_ls
    stand_score_sum += studentEvaluation.p_rb
    stand_score_sum += studentEvaluation.p_lauf
    stand_score_sum += studentEvaluation.p_ball
    studentEvaluation.overall_score = stand_score_sum
            
    studentEvaluation.save()

def potential_student(studentEvaluation, sportPotentialFactors):
    for sportPotentialFactor in sportPotentialFactors:
        sport_code = sportPotentialFactor.sport.code
        potential = calc_sport_potential(studentEvaluation, sportPotentialFactor)
        
        exec('studentEvaluation.potential_'+sport_code+'='+str(potential))

    studentEvaluation.save()