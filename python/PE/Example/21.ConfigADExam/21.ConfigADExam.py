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


def SetADConfig(nBdID: int) -> bool:
    byChannel = 0  # Channel = 0
    lADRange = 0  # AD Range = 0
    lFilterLen = 1000  # Filter Length = 1000
    lFilterOffset = -1000  # Filter Offset = -1000

    print("---------------------------------- ")
    # Set AD Range to 0 (-10 ~ 10[V])
    status_result, recv_status = FAS_SetADConfig(
        nBdID, byChannel, TYPE_AD_RANGE, lADRange
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetADConfig) was failed.")
    else:
        print("Set AD Config Success : AD Type %s(TYPE_AD_RANGE)" % TYPE_AD_RANGE)

    # Set Filter Length to 1000
    status_result, recv_status = FAS_SetADConfig(
        nBdID, byChannel, TYPE_AD_FILTER_LENGTH, lFilterLen
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetADConfig) was failed.")
    else:
        print("Set AD Config Success : AD Type %s(TYPE_AD_FILTER_LENGTH)" % TYPE_AD_FILTER_LENGTH)

    # Set Filter Offset to -1000
    status_result, recv_status = FAS_SetADConfig(
        nBdID, byChannel, TYPE_AD_FILTER_OFFSET, lFilterOffset
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetADConfig) was failed")
    else:
        print("Set AD Config Success : AD Type %s(TYPE_AD_FILTER_OFFSET)" % TYPE_AD_FILTER_OFFSET)
    return True


def GetADConfig(nBdID: int) -> bool:

    byChannel = 0  # Channel 0

    print("---------------------------------- ")
    # Get AD Range
    status_result, value = FAS_GetADConfig(nBdID, byChannel, TYPE_AD_RANGE)
    if status_result != FMM_OK:
        print("Function(FAS_GetADConfig) was failed.")
    else:
        print("Get AD Config Success : AD Type %s(TYPE_AD_RANGE), Value = %d " % (TYPE_AD_RANGE, value))

    # Get Filter Length
    status_result, value = FAS_GetADConfig(nBdID, byChannel, TYPE_AD_FILTER_LENGTH)
    if status_result != FMM_OK:
        print("Function(FAS_GetADConfig) was failed.")
    else:
        print("Get AD Config Success : AD Type %s(TYPE_AD_FILTER_LENGTH), Value = %d " % (TYPE_AD_FILTER_LENGTH, value))

    # Get Filter Length
    status_result, value = FAS_GetADConfig(nBdID, byChannel, TYPE_AD_FILTER_OFFSET)
    if status_result != FMM_OK:
        print("Function(FAS_GetADConfig) was failed.")
    else:
        print("Get AD Config Success : AD Type %s(TYPE_AD_FILTER_OFFSET), Value = %d " % (TYPE_AD_FILTER_OFFSET, value))

    return True


def main():
    nBdID = 0

    # Device Connect
    if not Connect(TCP, nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Set AD Config
    if not SetADConfig(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Get AD Config
    if not GetADConfig(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
