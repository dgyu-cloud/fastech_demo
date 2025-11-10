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


def ReadADValue(nBdID: int) -> bool:
    byChannel = 0  # Channel 0

    print("---------------------------------- ")
    # Read AD (Channel 0)
    status_result, advalue = FAS_ReadADValue(nBdID, byChannel)
    if status_result != FMM_OK:
        print("Function(FAS_ReadADValue) was failed.")
    else:
        print("Read AD Success : Channel[%d] %d" % (byChannel + 1, advalue))
    return True


def ReadADAllValue(nBdID: int) -> bool:
    byOffset = 0  # Offset Should be 0

    print("---------------------------------- ")
    # Read All AD
    status_result, advalue = FAS_ReadADAllValue(nBdID, byOffset)
    if status_result != FMM_OK:
        print("Function(FAS_ReadADAllValue) was failed.")
    else:
        print("Read AD All Success")
        for i in range(8):
            print("Channel[%d] : %d" % (i + 1, advalue[i]))

        return True


def main():
    nBdID = 0

    # Device Connect
    if not Connect(TCP, nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Read AD
    if not ReadADValue(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Read All AD
    if not ReadADAllValue(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
