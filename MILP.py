import numpy as np
import copy

GS = [1,10, 4,12, 6,15, 3, 9, 2,13,11, 7, 5, 0, 8,14]
DDT = np.zeros((len(GS), len(GS)))
def genDDT():
  for i in range(16):
    for j in range(16):
      DDT[i^j][GS[i]^GS[j]]+=1 


Inequalities = []
def GenerateEquations():
  impCoeff = []
  for alpha in range(16):
    for beta in range(16):
      if(DDT[alpha][beta]==0):
        a=[]
        t1 = alpha
        t2 = beta
        while(t1):
          a.append(t1%2)
          t1=t1//2
        a+=[0]*(4-len(a))
        while(t2):
          a.append(t2%2)
          t2=t2//2
        a+=[0]*(8-len(a))
        impCoeff.append(copy.deepcopy(a))
  x = ['x0','x1','x2','x3','y0','y1','y2','y3']
  for a in impCoeff:
    s = np.sum(a)
    stri=''
    for i in range(8):
      if(a[i]==1):
        stri+=' - {} '.format(x[i])
      else:
        if(i==0):
          stri+=' {} '.format(x[i])
        else:
          stri+=' + {} '.format(x[i])

    Inequalities.append(stri + ' >= ' + str(1-s))

genDDT()
GenerateEquations()  
print('---------------------------------------------------------------------------\n\t\tNumber of inequalities generated = {}\n---------------------------------------------------------------------------\n'.format(len(Inequalities)))

FILE = open('Equations.txt','w')
for eqn in Inequalities:
  FILE.write(eqn)
  FILE.write('\n')

print('Inequalities saved to Equations.txt file.')