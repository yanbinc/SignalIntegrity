"""
 Series Capacitance
"""
# Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
# Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
# All Rights Reserved.
#
# Explicit license in accompanying README.txt file.  If you don't have that file
# or do not agree to the terms in that file, then you are not licensed to use
# this material whatsoever.

from SignalIntegrity.Devices.SeriesG import SeriesG
from numpy import math

## SeriesC
#
# @param C float capacitance
# @param f float frequency
# @param Z0 (optional) float of complex reference impedance (defaults to 50 Ohms)
# @param df (optional) float dissipation factor (or loss-tangent) (defaults to 0)
# @param esr (optional) float effective-series-resistance (defaults to 0)
# @return the list of list s-parameter matrix for a series capacitance
#
def SeriesC(C,f,Z0=None,df=0.,esr=0.):
    G=C*2.*math.pi*f*(1j+df)
    try: G=G+1/esr
    except: pass
    return SeriesG(G,Z0)