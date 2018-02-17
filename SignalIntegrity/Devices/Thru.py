"""
 Thru
"""
# Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
# Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
# All Rights Reserved.
#
# Explicit license in accompanying README.txt file.  If you don't have that file
# or do not agree to the terms in that file, then you are not licensed to use
# this material whatsoever.

## Thru
#
# @returns the list of list s-parameter matrix of an ideal thru.
#
# this is simply a 2x2 matrix [[0,1][1,0]]
#
def Thru():
    return [[0.,1.],[1.,0.]]
