'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
from numpy import matrix,zeros,identity
from numpy.linalg import det

# Error terms are, for P ports, a P x P matrix of lists of three error terms.
# For the diagonal elements, the three error terms are ED, ER, and ES in that order
# for the off diagonal elements, the three error terms are EX, ET and EL in that order
# for r in 0...P-1, and c in 0...P-1,  ET[r][c] = [ED[r],ER[r],ES[r]], when r==c
# ET[r][c]=[EX[r][c],ET[r][c],EL[r][c]] when r !=c
#
# ET[r][c] refers to the error terms at port r when driven at port c
# in other words, if r==c, then:
# ET[r][r][0] = EDr
# ET[r][r][1] = ERr
# ET[r][r][2] = ESr
# and when r!=c, then:
# ET[r][c][0]=EXrc
# ET[r][c][1]=ETrc
# ET[r][c][2]=ELrc
#
class ErrorTerms(object):
    def __init__(self,ET=None):
        self.ET=ET
        if not ET is None:
            self.numPorts=len(ET)
        else:
            self.numPorts=None
    def Initialize(self,numPorts):
        self.numPorts=numPorts
        self.ET=[[[0.,0.,0.] for _ in range(self.numPorts)]
                 for _ in range(self.numPorts)]
        return self
    def __getitem__(self,item):
        return self.ET[item]
    def ReflectCalibration(self,hatGamma,Gamma,m):
        A=[[1.,Gamma[r]*hatGamma[r],-Gamma[r]] for r in range(len(Gamma))]
        B=[[hatGamma[r]] for r in range(len(Gamma))]
        EdEsDeltaS=(matrix(A).getI()*matrix(B)).tolist()
        Ed=EdEsDeltaS[0][0]
        Es=EdEsDeltaS[1][0]
        DeltaS=EdEsDeltaS[2][0]
        Er=Ed*Es-DeltaS
        self[m][m]=[Ed,Er,Es]
        return self
    def ThruCalibration(self,b1a1,b2a1,S,n,m):
        # pragma: silent exclude
        if not isinstance(b1a1,list):
            b1a1=[b1a1]
            b2a1=[b2a1]
            S=[S]
        # pragma: include
        [Ed,Er,Es]=self[m][m]
        Ex=self[n][m][0]
        A=zeros((2*len(b1a1),2)).tolist()
        B=zeros((2*len(b1a1),1)).tolist()
        for i in range(len(b1a1)):
            Sm=S[i]
            detS=det(matrix(Sm))
            A[2*i][0]=(Es*detS-Sm[1][1])*(Ed-b1a1[i])-Er*detS
            A[2*i][1]=0.
            A[2*i+1][0]=(Es*detS-Sm[1][1])*(Ex-b2a1[i])
            A[2*i+1][1]=Sm[1][0]
            B[2*i][0]=(1.-Es*Sm[0][0])*(b1a1[i]-Ed)-Er*Sm[0][0]
            B[2*i+1][0]=(1-Es*Sm[0][0])*(b2a1[i]-Ex)
        ElEt=(matrix(A).getI()*matrix(B)).tolist()
        (El,Et)=(ElEt[0][0],ElEt[1][0])
        self[n][m]=[Ex,Et,El]
        return self
    def ExCalibration(self,b2a1,n,m):
        [_,Et,El]=self[n][m]
        Ex=b2a1
        self[n][m]=[Ex,Et,El]
        return self
    def TransferThruCalibration(self):
        didOne=True
        while didOne:
            didOne=False
            for otherPort in range(self.numPorts):
                for drivenPort in range(self.numPorts):
                    if (otherPort == drivenPort):
                        continue
                    if ((self[otherPort][drivenPort][1]==0) and
                        (self[otherPort][drivenPort][2]==0)):
                        for mid in range(self.numPorts):
                            if ((mid != otherPort) and
                                (mid != drivenPort) and
                                ((self[otherPort][mid][1]!=0) or
                                 (self[otherPort][mid][2]!=0)) and
                                ((self[mid][drivenPort][1]!=0) or
                                 (self[mid][drivenPort][2]!=0))):
                                (_,Etl,_)=self[otherPort][mid]
                                (_,Etr,_)=self[mid][drivenPort]
                                (_,Erm,_)=self[mid][mid]
                                (_,_,Eso)=self[otherPort][otherPort]
                                (Ex,Et,El)=self[otherPort][drivenPort]
                                Et=Etl*Etr/Erm
                                El=Eso
                                self[otherPort][drivenPort]=[Ex,Et,El]
                                didOne=True
                                continue
        return self
    def Fixture(self,m):
        E=[[zeros((self.numPorts,self.numPorts),complex).tolist(),
            zeros((self.numPorts,self.numPorts),complex).tolist()],
           [zeros((self.numPorts,self.numPorts),complex).tolist(),
            zeros((self.numPorts,self.numPorts),complex).tolist()]]
        for n in range(self.numPorts):
            ETn=self[n][m]
            E[0][0][m][n]=ETn[0]
            E[0][1][n][n]=ETn[1]
            E[1][1][n][n]=ETn[2]
        E[1][0][m][m]=1.
        return E
    def DutCalculationAlternate(self,sRaw):
        if self.numPorts==1:
            (Ed,Er,Es)=self[0][0]
            gamma=sRaw[0][0]
            Gamma=(gamma-Ed)/((gamma-Ed)*Es+Er)
            return [[Gamma]]
        else:
            A=zeros((self.numPorts,self.numPorts),complex).tolist()
            B=zeros((self.numPorts,self.numPorts),complex).tolist()
            I=(identity(self.numPorts)).tolist()
            for m in range(self.numPorts):
                E=self.Fixture(m)
                b=matrix([[sRaw[r][m]] for r in range(self.numPorts)])
                Im=matrix([[I[r][m]] for r in range(self.numPorts)])
                bprime=(matrix(E[0][1]).getI()*(b-matrix(E[0][0])*Im)).tolist()
                aprime=(matrix(E[1][0])*Im+matrix(E[1][1])*matrix(bprime)).tolist()
                for r in range(self.numPorts):
                    A[r][m]=aprime[r][0]
                    B[r][m]=bprime[r][0]
            S=(matrix(B)*matrix(A).getI()).tolist()
            return S
    def DutCalculation(self,sRaw):
        B=[[(sRaw[r][c]-self[r][c][0])/self[r][c][1] for c in range(len(sRaw))]
           for r in  range(len(sRaw))]
        A=[[B[r][c]*self[r][c][2]+(1 if r==c else 0) for c in range(len(sRaw))]
           for r in range(len(sRaw))]
        S=(matrix(B)*matrix(A).getI()).tolist()
        return S