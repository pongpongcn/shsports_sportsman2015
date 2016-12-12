from sportsman.models import Student

def run():
    for student in Student.objects.filter(contains_e=None):
        print(student)
        student.save()