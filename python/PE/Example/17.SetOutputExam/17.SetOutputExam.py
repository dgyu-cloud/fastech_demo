#*************************************************************************************************************************************
#** Notification before use																											**
#*************************************************************************************************************************************
#** Depending on the type of product you are using, the definitions of Parameter, IO Logic, AxisStatus, etc. may be different.		**
#** This example is based on Ezi-SERVO2, so please apply the appropriate value depending on the product you are using.				**
#*************************************************************************************************************************************
#** ex)	FM_EZISERVO2_PARAM			// Parameter enum when using Ezi-SERVO2						 									**
#**		FM_EZIMOTIONLINK2_PARAM		// Parameter enum when using Ezi-MOTIONLINK2													**
#*************************************************************************************************************************************
# -*- coding: utf-8 -*-
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

OUTPUTPIN = 16


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


def SetOutput(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~ Fastech's product which has Input (or Output) only (Ezi-IO-I16, Ezi-IO-O16, Ezi-IO-I32, Ezi-IO-O32...), BitMask of Input (or Output) starts from 0x01,	~~
	#~ However, for Input+Output mixed products (Ezi-IO-I8O8, Ezi-IO-I16O16, etc.), the BitMask of Output is allocated after the BitMasks of Input.				~~
	#~ Ezi-IO-I8O8, for example, the BitMask of Input 0 is 0x0001, and the BitMask of Output 0 is 0x0100.														~~
	#~ For detailed allocation methods, please refer to Section 2.3 of the "doc.md" file of this example.														~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    print("-----------------------------------------")
    print("Clearing All outputs (bit 0 ~ bit 15.)")
    uSetMask = 0x00
    uClrMask = 0xFFFF

    if FAS_SetOutput(nBdID, uSetMask, uClrMask) != FMM_OK:
        print("Function(FAS_SetOutput) was failed.")
    else:
        print("FAS_SetOutput Success!")

    # Check OutputPin Status
    status_result, uOutput, uStatus = FAS_GetOutput(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetOutput) was failed.")
    else:
        for i in range(OUTPUTPIN):
            bON = (uOutput & (0x01 << i)) != 0
            print("OutPin[%d] = %s" % (i, "ON" if bON else "OFF"))

    print("-----------------------------------------")
    print("Set output bit #0.")
    uSetMask = 0x01
    uClrMask = 0x00
    if FAS_SetOutput(nBdID, uSetMask, uClrMask) != FMM_OK:
        print("Function(FAS_SetOutput) was failed.")
    else:
        print("FAS_SetOutput Success!")

    # Check OutputPin Status

    status_result, uOutput, uStatus = FAS_GetOutput(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetOutput) was failed.")
    else:
        for i in range(OUTPUTPIN):
            bON = (uOutput & (0x01 << i)) != 0
            print("OutPin[%d] = %s" % (i, "ON" if bON else "OFF"))

    print("-----------------------------------------")
    print("Clear bit #0 and Set bit #3, #4, #5.")
    uSetMask = 0x08 | 0x10 | 0x20
    uClrMask = 0x01
    if FAS_SetOutput(nBdID, uSetMask, uClrMask) != FMM_OK:
        print("Function(FAS_SetOutput) was failed.")
    else:
        print("FAS_SetOutput Success!")

    # Check OutputPin Status

    status_result, uOutput, uStatus = FAS_GetOutput(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetOutput) was failed.")
    else:
        for i in range(OUTPUTPIN):
            bON = (uOutput & (0x01 << i)) != 0
            print("OutPin[%d] = %s" % (i, "ON" if bON else "OFF"))
    return True


def main():
    nBdID = 0

    # Device Connect
    if not Connect(UDP, nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Set Output Status
    if not SetOutput(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
