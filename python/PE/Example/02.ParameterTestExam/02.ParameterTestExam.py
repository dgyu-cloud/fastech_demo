#*************************************************************************************************************************************
#** Notification before use																											**
#*************************************************************************************************************************************
#** Depending on the type of product you are using, the definitions of Parameter, IO Logic, AxisStatus, etc. may be different.		**
#** This example is based on Ezi-SERVO2, so please apply the appropriate value depending on the product you are using.				**
#*************************************************************************************************************************************
#** ex)	FM_EZISERVO2_PARAM			// Parameter enum when using Ezi-SERVO2						 									**
#**		FM_EZIMOTIONLINK2_PARAM		// Parameter enum when using Ezi-MOTIONLINK2													**
#*************************************************************************************************************************************

import sys
import os

try:
    library_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "Library")
    )
except NameError:
    library_path = os.path.abspath(
        os.path.join(os.getcwd(), "..", "..", "Library")
    )
sys.path.append(library_path)

from FAS_EziMOTIONPlusE import *
from MOTION_DEFINE import *
from ReturnCodes_Define import *
from MOTION_EziSERVO2_DEFINE import *


TCP = 0
UDP = 1


def Connect(nCommType: int, nBdID: int) -> bool:
    byIP = [192, 168, 0, 2]  # IP: 192.168.0.2
    bSuccess = True

    # Connection
    if nCommType == TCP:  # TCP Connection
        if FAS_ConnectTCP(byIP[0], byIP[1], byIP[2], byIP[3], nBdID) == 0:
            print("TCP Connection Fail!")
            bSuccess = False
    elif nCommType == UDP:  # UDP Connection
        if FAS_Connect(byIP[0], byIP[1], byIP[2], byIP[3], nBdID) == 0:
            print("UDP Connection Fail!")
            bSuccess = False
    else:
        print("Wrong communication type.")
        bSuccess = False

    if bSuccess:
        print("Connected successfully.")

    return bSuccess


def SetParameter(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    nChangeValue = 100

    print(
        "-----------------------------------------------------------------------------"
    )
    # Check The Axis Start Speed Parameter Status
    status_result, lParamVal = FAS_GetParameter(nBdID, SERVO2_AXISSTARTSPEED)
    if status_result != FMM_OK:
        print("Function(FAS_GetParameter) was failed.")
        return False
    else:
        print("Load Parameter[Before] : Start Speed = %d[pps]" % lParamVal)

    print(
        "-----------------------------------------------------------------------------"
    )
    # Change the (Axis Start Speed Parameter) value to (nChangeValue) value.
    status_result = FAS_SetParameter(nBdID, SERVO2_AXISSTARTSPEED, nChangeValue)
    if status_result != FMM_OK:
        print("Function(FAS_SetParameter) was failed.")
        return False
    else:
        print("Set Parameter: Start Speed = %d[pps]" % nChangeValue)

    print(
        "-----------------------------------------------------------------------------"
    )
    # Check the changed Axis Start Speed Parameter again.
    status_result, lParamVal = FAS_GetParameter(nBdID, SERVO2_AXISSTARTSPEED)
    if status_result != FMM_OK:
        print("Function(FAS_GetParameter) was failed.")
        return False
    else:
        print("Load Parameter[After] : Start Speed = %d[pps]" % lParamVal)

    return True


def main():
    nBdID = 0

    # Device Connect
    if not Connect(TCP, nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Load and Set Parameter
    if not SetParameter(nBdID):
        print("Failed to set parameter.")

    # Connection Close
    FAS_Close(nBdID)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
