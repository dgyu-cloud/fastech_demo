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


def LatchCount(nBdID: int) -> bool:

    cInputNo = 1  # Pin 0

    cntLatchAll = [0] * 16

    print("Monitor a specific pin Input latch signal while 1 min... ")

    # Monitor the specific pin input result value.
    for i in range(600):
        # Latch status
        status_result, uInput, uLatch = FAS_GetInput(nBdID)
        if status_result != FMM_OK:
            print("Function(FAS_GetInput) was failed.")
            return False

        # Latch count
        status_result, nLatchCount = FAS_GetLatchCount(nBdID, cInputNo)
        if status_result != FMM_OK:
            print("Function(FAS_GetLatchCount) was failed.")
            return False

        print(
            "Pin %d is %s and %s (latch count %d)" % (
                cInputNo,
                "ON" if (uInput & (0x01 << cInputNo)) else "OFF",
                "latched" if (uLatch & (0x01 << cInputNo)) else "not latched",
                nLatchCount
            )
        )
        time.sleep(0.1)

    # Clear the specific pin's Latch status
    uLatchMask = 0x01 << cInputNo
    if FAS_ClearLatch(nBdID, uLatchMask) != FMM_OK:
        print("Function(FAS_ClearLatch) was failed.")
        return False
    else:
        print("FAS_ClearLatch Success!")

    # Get Latch status again
    status_result, uInput, uLatch = FAS_GetInput(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetInput) was failed.")
        return False
    print(
        "Pin %d is %s" % (
            cInputNo,
            "latched" if (uLatch & (0x01 << cInputNo)) else "not latched"
        )
    )

    # Get latch counts of all inputs (16 inputs)
    status_result, cntLatchAll = FAS_GetLatchCountAll(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetLatchCountAll) was failed.")
        return False
    else:
        for i in range(16):
            print("[fas_get_latch_count_all] Pin[%d] : [%d] count" % (i, cntLatchAll[i]))

    # Clear the latch count of the specific pin
    if FAS_ClearLatchCount(nBdID, uLatchMask) != FMM_OK:
        print("Function(FAS_ClearLatchCount) was failed.")
        return False
    else:
        print("FAS_ClearLatchCount Success!")
    return True


def main():
    nBdID = 0

    # Device Connect
    if not Connect(UDP, nBdID):
        input("Press Enter to exit...")
        exit(1)

    # get input pin latch signal, get a specific pin latch count, get all pin latch count, clear latch
    if not LatchCount(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
