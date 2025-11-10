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


def Connect(nCommType: int, nBdID: int) -> bool:
    byIP = [192, 168, 0, 4]  # IP: 192.168.0.2
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


def SetTrigger(nBdID: int) -> bool:
    Trg_Info = TRIGGER_INFO()
    uCount = 0

    # Set Trigger value
    cOutputNo = 0  # Output pin #0
    Trg_Info.wCount = 20  # Set the number of Trigger outputs
    Trg_Info.wOnTime = 250  # On Time Setting : 250 [ms]
    Trg_Info.wPeriod = 500  # Set Trigger period : 500 [ms]

    if FAS_SetTrigger(nBdID, cOutputNo, Trg_Info) != FMM_OK:
        print("Function(FAS_SetTrigger) was failed.")
        return False

    else:
        print("FAS_SetTrigger Success!")

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~ Fastech's product which has Input (or Output) only (Ezi-IO-I16, Ezi-IO-O16, Ezi-IO-I32, Ezi-IO-O32...), BitMask of Input (or Output) starts from 0x01,	~~
	#~ However, for Input+Output mixed products (Ezi-IO-I8O8, Ezi-IO-I16O16, etc.), the BitMask of Output is allocated after the BitMasks of Input.				~~
	#~ Ezi-IO-I8O8, for example, the BitMask of Input 0 is 0x0001, and the BitMask of Output 0 is 0x0100.														~~
	#~ For detailed allocation methods, please refer to Section 2.2 of the "doc.md" file of this example.														~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Run Output
    uRunMask = 0x01 << cOutputNo  # Run Output Pin #0
    uStopMask = 0x00000000
    if FAS_SetRunStop(nBdID, uRunMask, uStopMask) != FMM_OK:
        print("Function(FAS_SetRunStop) was failed.")
        return False
    else:
        print("FAS_SetRunStop Success!")

    while True:
        time.sleep(0.1)

        status_result, uCount = FAS_GetTriggerCount(nBdID, cOutputNo)
        if status_result != FMM_OK:
            print("Function(FAS_GetTriggerCount) was failed.")
            return False
        else:
            print("Get Trigger [%d] count" % uCount)

        if Trg_Info.wCount <= uCount:
            break
    return True


def main():
    nBdID = 0

    # Device Connect
    if not Connect(UDP, nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Trigger Set and Check Count
    if not SetTrigger(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
