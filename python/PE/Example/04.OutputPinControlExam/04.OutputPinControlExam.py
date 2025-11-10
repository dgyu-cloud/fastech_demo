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

import time


TCP = 0
UDP = 1
INPUTPIN = 12
OUTPUTPIN = 10


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


def SetOutputPin(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print(
        "-----------------------------------------------------------------------------"
    )

    # Check OutputPin Status
    for i in range(OUTPUTPIN):
        status_result, dwLogicMask, byLevel = FAS_GetIOAssignMap(nBdID, INPUTPIN + i)
        if status_result != FMM_OK:
            print("Function(FAS_GetIOAssignMap) was failed.")
            return False

        if dwLogicMask != IN_LOGIC_NONE:
            print(
                "Output Pin[%d] : Logic Mask 0x%08x (%s)" 
                % (i, dwLogicMask, "Low Active" if byLevel == LEVEL_LOW_ACTIVE else "High Active")
            )
        else:
            print("Output Pin[%d] : Not Assigned" % i)

    print(
        "-----------------------------------------------------------------------------"
    )

    # Set Output pin Value.
    byPinNo = 3
    byLevel = LEVEL_HIGH_ACTIVE
    dwOutputMask = SERVO2_OUT_BITMASK_USEROUT0

    if FAS_SetIOAssignMap(nBdID, INPUTPIN + byPinNo, dwOutputMask, byLevel) != FMM_OK:
        print("Function(FAS_SetIOAssignMap) was failed.")
        return False

    # Show Output pins status
    for i in range(OUTPUTPIN):
        status_result, dwLogicMask, byLevel = FAS_GetIOAssignMap(nBdID, INPUTPIN + i)
        if status_result != FMM_OK:
            print("Function(FAS_GetIOAssignMap) was failed.")
            return False

        if dwLogicMask != IN_LOGIC_NONE:
            print(
                "Output Pin[%d] : Logic Mask 0x%08x (%s)" 
                % (i, dwLogicMask, "Low Active" if byLevel == LEVEL_LOW_ACTIVE else "High Active")
            )
        else:
            print("Output Pin[%d] : Not Assigned" % i)
    return True


def ControlOutputSignal(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    dwOutputMask = SERVO2_OUT_BITMASK_USEROUT0

    print(
        "-----------------------------------------------------------------------------"
    )

    # Control output signal on and off for 60 seconds
    for i in range(30):
        time.sleep(1)
        # USEROUT0: ON
        if FAS_SetIOOutput(nBdID, dwOutputMask, 0) != FMM_OK:
            print("Function(FAS_SetIOOutput) was failed.")
            return False

        time.sleep(1)
        # USEROUT0: OFF
        if FAS_SetIOOutput(nBdID, 0, dwOutputMask) != FMM_OK:
            print("Function(FAS_SetIOOutput) was failed.")
            return False

    print("finish WaitSecond!")
    return True


def main():
    nBdID = 0

    # Device Connect
    if not Connect(UDP, nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Set Output pin
    if not SetOutputPin(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Control output pin signal
    if not ControlOutputSignal(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
