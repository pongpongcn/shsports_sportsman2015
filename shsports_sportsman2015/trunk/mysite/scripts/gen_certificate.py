from sportsman.models import StudentEvaluation
from sportsman.utils.certificate_generator import CertificateGenerator
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

def run():
    studentEvaluation = StudentEvaluation.objects.all()[0]
    _gen_certificates([studentEvaluation,], True)
    
    mean = 457.3
    dev = 149.01
    
    x = np.arange(0,900,1)
    y = norm.pdf(x,loc=mean,scale=dev)#正态曲线的概率密度函数
    
    plt.plot(x, y)
    plt.plot([300,300],[0,norm.pdf(-0.1)],'k')#作一条直线
    '''plt.axis([0, 6, 0, 20])'''
    plt.savefig('xxx')

def _gen_certificates(studentEvaluations, isAdmin):
    '''
    输出PDF内容到临时文件，随后分段发送到客户端。
    从而避免内存过多消耗，同时临时文件会自动移除。
    '''
    
    fp = open('Certificate.pdf', 'wb')

    generator = CertificateGenerator(fp, isAdmin)
    
    generator.build(studentEvaluations)
    
    fp.close()
    