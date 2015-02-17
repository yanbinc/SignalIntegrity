from numpy import empty
from numpy import array
import cmath
import math
import string

class SParameters():
    def __init__(self,f,data,Z0=50.0):
        self.m_f=f
        self.m_d=data
        self.m_Z0=Z0
        if not data is None:
            if len(data)>0:
                self.m_P=len(data[0])
    def __getitem__(self,item):
        return self.m_d[item]
    def __len__(self):
        return len(self.m_f)
    def f(self):
        return self.m_f
    def Data(self):
        return self.m_d
    def Response(self,ToP,FromP):
        return [mat[ToP-1][FromP-1] for mat in self.m_d]
    def Resample(self,f):
        from SignalIntegrity.Splines import Spline
        res=[]
        x=self.m_f
        for r in range(self.m_P):
            resr=[]
            for c in range(self.m_P):
                y=self.Response(r+1,c+1)
                P=Spline(x,y)
                resr.append([P.Evaluate(fi) for fi in f])
            res.append(resr)
        resd = []
        for n in range(len(f)):
            mat=empty(shape=(self.m_P,self.m_P)).tolist()
            for r in range(self.m_P):
                for c in range(self.m_P):
                    mat[r][c]=res[r][c][n]
            resd.append(mat)
        self.m_d=resd
        self.m_f=f
        return self
    def WriteToFile(self,name,formatString=None):
        freqMul = 1e6
        freqToken = 'MHz'
        complexType = 'MA'
        Z0 = 50.0
        #list of tokens separated by ' ' before the first, if any '!'
        if not formatString is None:
            lineList = string.lower(formatString).split('!')[0].split()
            if len(lineList)>0:
                if 'hz' in lineList:
                    freqToken = 'Hz'
                    freqMul = 1.0
                if 'khz' in lineList:
                    freqToken = 'KHz'
                    freqMul = 1e3
                if 'mhz' in lineList:
                    freqToken = 'MHz'
                    freqMul = 1e6
                if 'ghz' in lineList:
                    freqToken = 'GHz'
                    freqMul = 1e9
                if 'ma' in lineList:
                    complexType = 'MA'
                if 'ri' in lineList:
                    complexType = 'RI'
                if 'db' in lineList:
                    complexType = 'DB'
                if 'r' in lineList:
                    Z0=float(lineList[lineList.index('r')+1])
        spfile=open(name,'w')
        spfile.write('# '+freqToken+' '+complexType+' S R '+str(Z0)+'\n')
        for n in range(len(self.m_f)):
            line=[str(self.m_f[n]/freqMul)]
            mat=self.m_d[n]
            if Z0 != self.m_Z0:
                mat=ReferenceImpedance(mat,Z0,self.m_Z0)
            if self.m_P == 2:
                mat=array(mat).transpose().tolist()
            for r in range(self.m_P):
                for c in range(self.m_P):
                    val = mat[r][c]
                    if complexType == 'MA':
                        line.append(str(abs(val)))
                        line.append(str(cmath.phase(val)*180./math.pi))
                    elif complexType == 'RI':
                        line.append(str(val.real))
                        line.append(str(val.imag))
                    elif complexType == 'DB':
                        line.append(str(20*math.log10(abs(val))))
                        line.append(str(cmath.phase(val)*180./math.pi))
            pline = ' '.join(line)+'\n'
            spfile.write(pline)
        spfile.close()
    def AreEqual(self,sp,epsilon):
        if len(self) != len(sp):
            return False
        if len(self.m_d) != len(sp.m_d):
            return False
        for n in range(len(self.Data())):
            if abs(self.m_f[n] - sp.m_f[n]) > epsilon:
                return False
            for r in range(self.m_P):
                for c in range(self.m_P):
                    if abs(self.m_d[n][r][c] - sp.m_d[n][r][c]) > epsilon:
                        return False
        return True
