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
    byIP = [192, 168, 0, 3]  # IP: 192.168.0.2
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


def GetIOLevel(nBdID: int) -> bool:

    print("----------------------------------")
    # [Before] Check IO Level Status
    status_result, uIOLevel = FAS_GetIOLevel(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetIOLevel) was failed.")
        return False
    print("Load IO Level Status : 0x%08x" % uIOLevel)

    for i in range(16):
        bLevel = (uIOLevel & (0x01 << i)) != 0
        print("I/O pin %d : %s" % (i, "High Active" if bLevel else "Low Active"))

    return True


def SetIOLevel(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~ Fastech's product which has Input (or Output) only (Ezi-IO-I16, Ezi-IO-O16, Ezi-IO-I32, Ezi-IO-O32...), BitMask of Input (or Output) starts from 0x01,	~~
	#~ However, for Input+Output mixed products (Ezi-IO-I8O8, Ezi-IO-I16O16, etc.), the BitMask of Output is allocated after the BitMasks of Input.				~~
	#~ Ezi-IO-I8O8, for example, the BitMask of Input 0 is 0x0001, and the BitMask of Output 0 is 0x0100.														~~
	#~ For detailed allocation methods, please refer to Section 2.1 of the "doc.md" file of this example.														~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    uIOLevel = 0x0000FF00

    print("----------------------------------")

    # Set IO Level Status
    if FAS_SetIOLevel(nBdID, uIOLevel) != FMM_OK:
        print("Function(FAS_SetIOLevel) was failed.")

    else:
        print("Set IO Level Status : 0x%08x" % uIOLevel)
    return True


def main():
    nBdID = 0

    # Device Connect
    if not Connect(TCP, nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Get IO Level
    if not GetIOLevel(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Set IO Level
    if not SetIOLevel(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
