#
""" Common Facilities For Remote Operations Scenarios For Verification Of Petstore Service. 
    
    Common Parameter Specification.

    To be imported by Petstore Service opScn-s.
"""

from unisos.mmwsIcm import ro
from unisos import icm

def deploySvcSpecObtain():
    return "../svcSpec/petstore.json"


def deploySvcPerfSapObtain():
    return "http://localhost:8080"


def verify_deploySvcCommonRo(opExpectation):
    roOp = opExpectation.roOp
    opResults = roOp.roResults
    if opResults.httpResultCode < 400:
        icm.ANN_write("* ==:: SUCCESS")
    else:
        icm.ANN_write("* ==:: FAILED")        

