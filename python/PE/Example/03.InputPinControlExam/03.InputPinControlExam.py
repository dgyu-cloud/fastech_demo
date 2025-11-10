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


def SetInputPin(nBdID: int) -> bool:
    
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    print(
        "-----------------------------------------------------------------------------"
    )

    # Set Input pin Value.
    byPinNo = 3
    byLevel = LEVEL_LOW_ACTIVE
    dwInputMask = SERVO2_IN_BITMASK_USERIN0

    if FAS_SetIOAssignMap(nBdID, byPinNo, dwInputMask, byLevel) != FMM_OK:
        print("Function(FAS_SetIOAssignMap) was failed.")
        return False
    else:
        print(
            "SERVO2_IN_BITMASK_USERIN0 (Pin%d) : [%s]" 
            % (byPinNo, "Low Active" if byLevel == LEVEL_LOW_ACTIVE else "High Active")
        )

    print(
        "-----------------------------------------------------------------------------"
    )

    # Show Input pins status
    for i in range(INPUTPIN):
        status_result, dwLogicMask, byLevel = FAS_GetIOAssignMap(nBdID, i)
        if status_result != FMM_OK:
            print("Function(FAS_GetIOAssignMap) was failed.")
            return False

        if dwLogicMask != IN_LOGIC_NONE:
            print(
                "Input PIN[%d] : Logic Mask 0x%08x (%s)" 
                % (i, dwLogicMask, "Low Active" if byLevel == LEVEL_LOW_ACTIVE else "High Active")
            )
        else:
            print("Input Pin[%d] : Not Assigned" % i)
    return True


def CheckInputSignal(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    dwInputMask = SERVO2_IN_BITMASK_USERIN0

    print(
        "-----------------------------------------------------------------------------"
    )

    # When the value SERVO2_IN_BITMASK_USERIN0 is entered with the set PinNo, an input confirmation message is displyed.
    # Monitoring input signal for 60 seconds
    for i in range(600):
        status_result, dwInput = FAS_GetIOInput(nBdID)
        if status_result == FMM_OK:
            if dwInput & dwInputMask:
                print("INPUT PIN DETECTED.")
        else:
            print("Function(FAS_GetIOInput) was failed.")
            return False
        time.sleep(0.1)
    print("finish WaitSecond!")
    return True


# Main function for execution
def main():
    nBdID = 0

    # Device Connect
    if not Connect(UDP, nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Set Input pins
    if not SetInputPin(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Check Input Pin Signal
    if not CheckInputSignal(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
