from sportsman.models import StudentEvaluation
from sportsman.utils.certificate_generator import CertificateGenerator
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from matplotlib.path import Path
from matplotlib.patches import PathPatch

def runx():
    xx=np.arange(0,10,0.01)
    yy=xx*np.exp(-xx)

    path = Path(np.array([xx,yy]).transpose())
    patch = PathPatch(path, facecolor='none')
    plt.gca().add_patch(patch)

    im = plt.imshow(xx.reshape(yy.size,1),  cmap=plt.cm.gist_rainbow,interpolation="bicubic",
                    origin='lower',extent=[0,10,-0.0,0.40],aspect="auto", clip_path=patch, clip_on=True)

    plt.show()

def run():
    studentEvaluation = StudentEvaluation.objects.all()[0]
    _gen_certificates([studentEvaluation,], True)
    
    mean = 457.3
    dev = 149.01
    
    x = np.arange(0, 900, 1)
    y = norm.pdf(x,loc=mean,scale=dev)#正态曲线的概率密度函数
    
    ylimmax = max(y) * 1.2
    
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    #plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    
    #rainbow_fill(x,y)
    
    #plt.figure(figsize=(1,1))
    
    z = [[z] * 10 for z in range(10)]
    num_bars = 100  # more bars = smoother gradient
    
    path = Path(np.array([x,y]).transpose())
    patch = PathPatch(path, edgecolor='none', facecolor='none')
    plt.gca().add_patch(patch)

    im = plt.imshow(np.vstack((x, x)),  cmap=plt.cm.gist_rainbow, origin='lower',extent=[0,900,0,max(y)],aspect="auto", alpha=0.8, clip_path=patch, clip_on=True)
    
    plt.plot([200,200],[0,ylimmax * 1.2],'r')#作一条直线
    plt.text(200, ylimmax * 1.2, 'LQ',
        verticalalignment='bottom', horizontalalignment='center', fontsize=15)
    
    plt.plot([700,700],[0,ylimmax * 1.5],'y')#作一条直线
    plt.text(700, ylimmax * 1.5, 'UQ',
        verticalalignment='bottom', horizontalalignment='center', fontsize=15)
    
    plt.plot([500,500],[0,ylimmax],'k')#作一条直线
    plt.text(500, ylimmax, 'SELF',
        verticalalignment='bottom', horizontalalignment='center', fontsize=15)
        
    '''plt.axis([0, 6, 0, 20])'''
    #plt.ylim(0,ylimmax * 2)
    plt.legend()
    plt.axis('off')
    
    plt.text(100, -1*ylimmax*0.01, 'BELOW STANDARD',
        verticalalignment='top', horizontalalignment='center', fontsize=15)
        
    plt.text(mean, -1*ylimmax*0.01, 'PASS',
        verticalalignment='top', horizontalalignment='center', fontsize=15)
    
    plt.text(800, -1*ylimmax*0.01, 'OPTIMAL',
        verticalalignment='top', horizontalalignment='center', fontsize=15)
    
    #plt.show()
    plt.savefig('x1')

def rect(x,y,w,h,c):
    ax = plt.gca()
    polygon = plt.Rectangle((x,y),w,h,color=c)
    ax.add_patch(polygon)

def rainbow_fill(X,Y, cmap=plt.get_cmap("jet")):
    plt.plot(X,Y,lw=0)  # Plot so the axes scale correctly

    dx = X[1]-X[0]
    N  = float(X.size)

    for n, (x,y) in enumerate(zip(X,Y)):
        color = cmap(n/N)
        rect(x,0,dx,y,color)
    
def _gen_certificates(studentEvaluations, isAdmin):
    '''
    输出PDF内容到临时文件，随后分段发送到客户端。
    从而避免内存过多消耗，同时临时文件会自动移除。
    '''
    
    fp = open('Certificate.pdf', 'wb')

    generator = CertificateGenerator(fp, isAdmin)
    
    generator.build(studentEvaluations)
    
    fp.close()
    