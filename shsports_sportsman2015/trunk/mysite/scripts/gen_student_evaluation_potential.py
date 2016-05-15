from sportsman.services import evaluation_student, potential_student

import csv

from sportsman.models import Student
from sportsman.models import StudentEvaluation
from sportsman.models import Factor
from sportsman.models import SportPotentialFactor

def run():
    factors = list(Factor.objects.filter(version="china_201604"))
    sportPotentialFactors = SportPotentialFactor.objects.all()
    
    with open('student_evaluation_potential.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['noOfStudentStatus', 'firstName', 'lastName', 'gender', 'dateOfTesting', 'number', 'badminton', 'basketball', 'soccer', 'gymnastics', 'canoe', 'athletics_running', 'athletics_sprinting_jumping_throwing', 'swimming', 'table_tennis', 'volleyball'])
        for student in Student.objects.filter(studentevaluation=None).order_by('testPlan', 'dateOfTesting', 'number'):
            gender = student.gender
            months_of_age = student.months_of_age
            
            factors_matched = list(filter(lambda x:x.gender==gender and x.month_age==months_of_age, factors))
            if len(factors_matched) != 1:
                continue
            else:
                factor = factors_matched[0]
            
            evaluation_student(student, factor)
            studentevaluation = student.studentevaluation
            
            potential_student(studentevaluation, sportPotentialFactors)
            
            writer.writerow([student.noOfStudentStatus,
                                student.firstName,
                                student.lastName,
                                student.gender,
                                student.dateOfTesting,
                                student.number,
                                studentevaluation.potential_badminton,
                                studentevaluation.potential_basketball,
                                studentevaluation.potential_soccer,
                                studentevaluation.potential_gymnastics,
                                studentevaluation.potential_canoe,
                                studentevaluation.potential_athletics_running,
                                studentevaluation.potential_athletics_sprinting_jumping_throwing,
                                studentevaluation.potential_swimming,
                                studentevaluation.potential_table_tennis,
                                studentevaluation.potential_volleyball])
        