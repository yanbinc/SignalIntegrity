'''
2-4 Port Transresistance Amplifiers
'''
# Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
# Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
# All Rights Reserved.
# 
# Explicit license in accompanying README.txt file.  If you don't have that file
# or do not agree to the terms in that file, then you are not licensed to use
# this material whatsoever.

## TransresistanceAmplifier
#
# @param P integer number of ports (2-4)
# @param G float transresistance gain
# @param Zi float or complex input impedance
# @param Zo float or complex output impedance
# @param Z0 (optional) float reference impedance (defaults to 50 Ohms)
# @return list of list s-parameter matrix for a transresistance amplifier
#
# The transresistance amplifier can be two, three or four ports
#
# @see TransresistanceAmplifierFourPort
# @see TransresistanceAmplifierThreePort
# @see TransresistanceAmplifierTwoPort
#
def TransresistanceAmplifier(P,G,Zi,Zo,Z0=50.):
    if P==2:
        return TransresistanceAmplifierTwoPort(G,Zi,Zo,Z0=50.)
    elif P==3:
        return TransresistanceAmplifierThreePort(G,Zi,Zo,Z0=50.)
    elif P==4:
        return TransresistanceAmplifierFourPort(G,Zi,Zo,Z0=50.)

## TransresistanceAmplifierFourPort
#
# @param G float transresistance gain
# @param Zi float or complex input impedance
# @param Zo float or complex output impedance
# @param Z0 (optional) float reference impedance (defaults to 50 Ohms)
# @return list of list s-parameter matrix for a transresistance amplifier
#
# The current sense element senses the current entering port 1 and exiting port 2
# with a series resistance in the current sense path of Zi.
#
# The voltage generated by the amplifier has the plus terminal at port 4 and 
# and the minus terminal at port 3 with Zo in series.
#
def TransresistanceAmplifierFourPort(G,Zi,Zo,Z0=50.):
    S11=Zi/(Zi+2.*Z0)
    S12=2.*Z0/(Zi+2.*Z0)
    S13=0
    S14=0
    S21=S12
    S22=S11
    S23=0
    S24=0
    S31=2.*G*Z0/((Zi+2.*Z0)*(Zo+2.*Z0))
    S32=-S31
    S33=Zo/(Zo+2.*Z0)
    S34=2.*Z0/(Zo+2.*Z0)
    S41=S32
    S42=S31
    S43=S34
    S44=S33
    return [[S11,S12,S13,S14],
            [S21,S22,S23,S24],
            [S31,S32,S33,S34],
            [S41,S42,S43,S44]]

## TransresistanceAmplifierThreePort
#
# @param G float transresistance gain
# @param Zi float or complex input impedance
# @param Zo float or complex output impedance
# @param Z0 (optional) float reference impedance (defaults to 50 Ohms)
# @return list of list s-parameter matrix for a transresistance amplifier
#
# The three port transresistance amplifier is the same as the four port transresistance amplifier with
# ports two and three connected together and exposed as a single port.
#
# The current sense element senses the current entering port 3 and exiting port 1
# with a series resistance in the current sense path of Zi.
#
# The voltage generated by the amplifier has the plus terminal at port 2 and 
# and the minus terminal at port 3 with Zo in series.
# 
def TransresistanceAmplifierThreePort(G,Zi,Zo,Z0=50.):
    D=3.*Z0*Z0+(2.*Zo+2.*Zi-G)*Z0+Zo*Zi
    S11=(Zo*Zi+Z0*(2.*Zi-G)-Z0*Z0)/D
    S12=(2.*Z0*Z0)/D
    S13=(2.*Z0*Z0+2.*Zo*Z0)/D
    S21=(2.*Z0*Z0+2.*G*Z0)/D
    S22=(Zo*Zi+Z0*(2.*Zo-G)-Z0*Z0)/D
    S23=(2.*Z0*Z0+Z0*(2.*Zi-2.*G))/D
    S31=(2.*Z0*Z0+Z0*(2.*Zo-2.*G))/D
    S32=(2.*Z0*Z0+2.*Zi*Z0)/D
    S33=(Zo*Zi-Z0*Z0+G*Z0)/D
    return [[S11,S12,S13],
            [S21,S22,S23],
            [S31,S32,S33]]


## TransresistanceAmplifierTwoPort
#
# @param G float transresistance gain
# @param Zi float or complex input impedance
# @param Zo float or complex output impedance
# @param Z0 (optional) float reference impedance (defaults to 50 Ohms)
# @return list of list s-parameter matrix for a transresistance amplifier
#
# The two port transresistance amplifier is the same as the three port transresistance amplifier with
# port 3 grounded.
#
# The current sense element senses the current entering port 1
# with a series resistance in the current sense path of Zi.
#
# The voltage generated by the amplifier is at port 2 referenced to ground 
# with Zo in series with the output.
# 
def TransresistanceAmplifierTwoPort(G,Zi,Zo,Z0=50.):
    return [[(Zi-Z0)/(Zi+Z0),0.],[2.*G*Z0/((Zi+Z0)*(Zo+Z0)),(Zo-Z0)/(Zo+Z0)]]
