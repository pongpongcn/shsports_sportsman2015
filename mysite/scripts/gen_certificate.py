from sportsman.models import StudentEvaluation
from sportsman.utils.certificate_generator import CertificateGenerator

def run():
    studentEvaluation = StudentEvaluation.objects.all()[0]
    _gen_certificates([studentEvaluation,], True)

def _gen_certificates(studentEvaluations, isAdmin):
    '''
    输出PDF内容到临时文件，随后分段发送到客户端。
    从而避免内存过多消耗，同时临时文件会自动移除。
    '''
    
    fp = open('Certificate.pdf', 'wb')

    generator = CertificateGenerator(fp, isAdmin)
    
    generator.build(studentEvaluations)
    
    fp.close()
    