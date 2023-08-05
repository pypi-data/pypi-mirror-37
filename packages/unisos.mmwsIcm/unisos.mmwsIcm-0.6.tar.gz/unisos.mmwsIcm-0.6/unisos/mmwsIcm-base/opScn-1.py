#
""" Remote Operations Scenarios For Verification Of Petstore Service. 
    rosList creates a list of Ro_Op-s which are to be invoked/validated/etc.
"""

from unisos.mmwsIcm import ro

import opScnCommon

petstoreSvcSpec = opScnCommon.petstoreSvcSpecObtain()
petstoreSvcPerfSap = opScnCommon.petstoreSvcPerfSapObtain()

headerParams = opScnCommon.petstoreSvcHeaderParamsObtain()

verify_petstoreSvcCommonRo = opScnCommon.verify_petstoreSvcCommonRo  # Alias function, for brevity

rosList = ro.Ro_OpsList()
roExpectationsList = ro.Ro_OpExpectationsList()

hostParamObj = {
    'az': 'AZ-2-2',
    'uuid': '55555555-bf72-4845-8fa4-f218872412af',    
    'datacenterCode': 'DC-1-1',
    'ip': '47.4.74.158',
    'region': 'R1',
    'hostname':
    'HostAZ-1-10',
    'rack': 'rack1',
    }

pkgParamObj = {
    'id': 'NOTYET',
    }    

thisRo = ro.Ro_Op(
    svcSpec=petstoreSvcSpec,
    perfSap=petstoreSvcPerfSap,
    resource="Hosts",
    opName="addHostOrUpdate",
    roParams=ro.Ro_Params(headerParams=headerParams, urlParams=None, bodyParams=hostParamObj,),
    roResults=None,
    )

rosList.opAppend(thisRo)

thisExpectation = ro.Ro_OpExpectation(
    roOp=thisRo,
    preInvokeCallables=[],
    postInvokeCallables=[ verify_petstoreSvcCommonRo, ],    
    expectedResults=None,
    )

roExpectationsList.opExpectationAppend(thisExpectation)
