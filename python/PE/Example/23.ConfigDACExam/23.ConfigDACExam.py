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


def SetDACConfig(nBdID: int) -> bool:

    byChannel = 0  # Channel = 0
    lDACRange = 0  # AD Range = 0
    lCalbrationHigh = 24000  # Calibration High = 24000
    lCalbrationLow = -1000  # Calibration Low = -1000

    print("---------------------------------- ")
    # Set DAC Range to 0 (0 ~ 5[V])
    status_result, recv_result = FAS_SetDACConfig(
        nBdID, byChannel, DAC_RANGE, lDACRange
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetDACConfig) was failed.")
    else:
        print("Set DAC Config Success : DAC Type %d(DAC_RANGE)" % DAC_RANGE)

    # Set DAC Calibration High to 24000
    status_result, recv_result = FAS_SetDACConfig(
        nBdID, byChannel, DAC_CALIBRATION_HIGH, lCalbrationHigh
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetDACConfig) was failed.")
    else:
        print("Set DAC Config Success : DAC Type %d(DAC_CALIBRATION_HIGH)" % DAC_CALIBRATION_HIGH)

    # Set DAC Calibration Low to -1000
    status_result, recv_result = FAS_SetDACConfig(
        nBdID, byChannel, DAC_CALIBRATION_LOW, lCalbrationLow
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetDACConfig) was failed.")
    else:
        print("Set DAC Config Success : DAC Type %d(DAC_CALIBRATION_LOW)" % DAC_CALIBRATION_LOW)
    return True


def GetDACConfig(nBdID: int) -> bool:

    byChannel = 0  # Channel 0

    print("---------------------------------- ")
    # Get DAC Range
    status_result, data = FAS_GetDACConfig(nBdID, byChannel, DAC_RANGE)
    if status_result != FMM_OK:
        print("Function(FAS_GetDACConfig) was failed.")
    else:
        print("Get DAC Config Success : DAC Type %d(DAC_RANGE), Value = %d" % (DAC_RANGE, data))

    # Get DAC Calibration High
    status_result, data = FAS_GetDACConfig(nBdID, byChannel, DAC_CALIBRATION_HIGH)
    if status_result != FMM_OK:
        print("Function(FAS_GetDACConfig) was failed.")
    else:
        print("Get DAC Config Success : DAC Type %d(DAC_CALIBRATION_HIGH), Value = %d" % (DAC_CALIBRATION_HIGH, data))

    # Get DAC Calibration Low
    status_result, data = FAS_GetDACConfig(nBdID, byChannel, DAC_CALIBRATION_LOW)
    if status_result != FMM_OK:
        print("Function(FAS_GetDACConfig) was failed.")
    else:
        print("Get DAC Config Success : DAC Type %d(DAC_CALIBRATION_LOW), Value = %d" % (DAC_CALIBRATION_LOW, data))

    return True


def main():
    nBdID = 0

    # Device Connect
    if not Connect(TCP, nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Set DAC Config
    if not SetDACConfig(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Get DAC Config
    if not GetDACConfig(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
