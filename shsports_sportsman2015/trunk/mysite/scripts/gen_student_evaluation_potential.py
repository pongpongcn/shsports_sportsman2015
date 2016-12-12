from sportsman.services import evaluation_student, potential_student

import csv, json

from sportsman.models import Student
from sportsman.models import Factor
from sportsman.models import SportPotentialFactor
from django.db.models import Q,F

class PotentialItem:
    def __init__(self, name, value):
        self.name = name
        self.value = value

def run():
    factors = list(Factor.objects.filter(version="china_201604"))
    sportPotentialFactors = SportPotentialFactor.objects.all()
    
    with open('student_evaluation_potential.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['noOfStudentStatus', 'firstName', 'lastName', 'gender', 'dateOfTesting', 'number', 'badminton', 'basketball', 'soccer', 'gymnastics', 'canoe', 'athletics_running', 'athletics_sprinting_jumping_throwing', 'swimming', 'table_tennis', 'volleyball'])
        #for student in Student.objects.filter(dataVersion=None):
        for student in Student.objects.filter(Q(contains_e=True) & (Q(studentevaluation=None) | Q(studentevaluation__correspondWithStudentDataVersion__lt=F('dataVersion')) | (~Q(dataVersion=None) & Q(studentevaluation__correspondWithStudentDataVersion=None)))).order_by('testPlan', 'dateOfTesting', 'number'):            
            gender = student.gender
            months_of_age = student.months_of_age
            
            factors_matched = list(filter(lambda x:x.gender==gender and x.month_age==months_of_age, factors))
            if len(factors_matched) != 1:
                continue
            else:
                factor = factors_matched[0]
            
            try:
                studentEvaluation = student.studentevaluation
                studentEvaluation.delete()
            except:
                pass
                
            evaluation_student(student, factor)
            studentevaluation = student.studentevaluation
            
            potential_student(studentevaluation, sportPotentialFactors)
            
            potential_items = []
            if studentevaluation.potential_badminton is not None:
                potential_items.append(PotentialItem('badminton', studentevaluation.potential_badminton))
            if studentevaluation.potential_basketball is not None:
                potential_items.append(PotentialItem('basketball', studentevaluation.potential_basketball))
            if studentevaluation.potential_soccer is not None:
                potential_items.append(PotentialItem('soccer', studentevaluation.potential_soccer))
            if studentevaluation.potential_gymnastics is not None:
                potential_items.append(PotentialItem('gymnastics', studentevaluation.potential_gymnastics))
            if studentevaluation.potential_canoe is not None:
                potential_items.append(PotentialItem('canoe', studentevaluation.potential_canoe))
            if studentevaluation.potential_discus is not None:
                potential_items.append(PotentialItem('discus', studentevaluation.potential_discus))
            if studentevaluation.potential_shot_put is not None:
                potential_items.append(PotentialItem('shot_put', studentevaluation.potential_shot_put))
            if studentevaluation.potential_pole_vault is not None:
                potential_items.append(PotentialItem('pole_vault', studentevaluation.potential_pole_vault))
            if studentevaluation.potential_high_jump is not None:
                potential_items.append(PotentialItem('high_jump', studentevaluation.potential_high_jump))
            if studentevaluation.potential_javelin is not None:
                potential_items.append(PotentialItem('javelin', studentevaluation.potential_javelin))
            if studentevaluation.potential_long_jump is not None:
                potential_items.append(PotentialItem('long_jump', studentevaluation.potential_long_jump))
            if studentevaluation.potential_huerdles is not None:
                potential_items.append(PotentialItem('huerdles', studentevaluation.potential_huerdles))
            if studentevaluation.potential_sprint is not None:
                potential_items.append(PotentialItem('sprint', studentevaluation.potential_sprint))
            if studentevaluation.potential_rowing is not None:
                potential_items.append(PotentialItem('rowing', studentevaluation.potential_rowing))
            if studentevaluation.potential_swimming is not None:
                potential_items.append(PotentialItem('swimming', studentevaluation.potential_swimming))
            if studentevaluation.potential_tennis is not None:
                potential_items.append(PotentialItem('tennis', studentevaluation.potential_tennis))
            if studentevaluation.potential_table_tennis is not None:
                potential_items.append(PotentialItem('table_tennis', studentevaluation.potential_table_tennis))
            if studentevaluation.potential_volleyball is not None:
                potential_items.append(PotentialItem('volleyball', studentevaluation.potential_volleyball))
            potential_items.sort(key=lambda item: item.value, reverse=True)
            temp_potential_item_names = []
            if studentevaluation.is_frail != True:
                for potential_item in potential_items[:3]:
                    temp_potential_item_names.append(potential_item.name)

            certificate_template = 'ShanghaiMovementCheck2015'
            certificate_data = {'template':certificate_template, 'potential_items':temp_potential_item_names}
            studentevaluation.certificate_data = json.dumps(certificate_data)
            
            studentevaluation.save()
            
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