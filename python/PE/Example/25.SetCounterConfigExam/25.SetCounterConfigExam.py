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


def SetCounterConfig(nBdID: int) -> bool:

    byChannel = 0  # Channel = 0

    print("----------------------------------")
    # Set Counter Input Mode
    status_result, recv_status = FAS_SetCounterConfig(
        nBdID, byChannel, CFG_INPUT_MODE, 1
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetCounterConfig) was failed.")
    else:
        print("Set Counter Config Success : Counter Type %d(CFG_INPUT_MODE)" % CFG_INPUT_MODE)

    # Set Counter Direction
    status_result, recv_status = FAS_SetCounterConfig(
        nBdID, byChannel, CFG_COUNT_DIRECTION, 1
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetCounterConfig) was failed.")
    else:
        print("Set Counter Config Success : Counter Type %d(CFG_COUNT_DIRECTION)" % CFG_COUNT_DIRECTION)

    # Set Counter Latch A Mode
    status_result, recv_status = FAS_SetCounterConfig(
        nBdID, byChannel, CFG_LATCHA_MODE, 1
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetCounterConfig) was failed.")
    else:
         print("Set Counter Config Success : Counter Type %d(CFG_LATCHA_MODE)" % CFG_LATCHA_MODE)

    # Set Counter Latch B Mode
    status_result, recv_status = FAS_SetCounterConfig(
        nBdID, byChannel, CFG_LATCHB_MODE, 1
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetCounterConfig) was failed.")
    else:
        print("Set Counter Config Success : Counter Type %d(CFG_LATCHB_MODE)" % CFG_LATCHB_MODE)

    # Set Counter Z-Phase Latch Mode
    status_result, recv_status = FAS_SetCounterConfig(
        nBdID, byChannel, CFG_ZLATCH_MODE, 1
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetCounterConfig) was failed.")
    else:
        print("Set Counter Config Success : Counter Type %d(CFG_ZLATCH_MODE)" % CFG_ZLATCH_MODE)

    # Set Counter Latch A Logic
    status_result, recv_status = FAS_SetCounterConfig(
        nBdID, byChannel, CFG_LATCHA_LOGIC, 1
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetCounterConfig) was failed.")
    else:
        print("Set Counter Config Success : Counter Type %d(CFG_LATCHA_LOGIC)" % CFG_LATCHA_LOGIC)

    # Set Counter Latch B Logic
    status_result, recv_status = FAS_SetCounterConfig(
        nBdID, byChannel, CFG_LATCHB_LOGIC, 1
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetCounterConfig) was failed.")
    else:
        print("Set Counter Config Success : Counter Type %d(CFG_LATCHB_LOGIC)" % CFG_LATCHB_LOGIC)

    # Set Counter Z-Phase Latch Logic
    status_result, recv_status = FAS_SetCounterConfig(
        nBdID, byChannel, CFG_ZLATCH_LOGIC, 1
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetCounterConfig) was failed.")
    else:
        print("Set Counter Config Success : Counter Type %d(CFG_ZLATCH_LOGIC)" % CFG_ZLATCH_LOGIC)

    # Set Counter Reset Logic
    status_result, recv_status = FAS_SetCounterConfig(
        nBdID, byChannel, CFG_RESET_LOGIC, 1
    )
    if status_result != FMM_OK:
        print("Function(FAS_SetCounterConfig) was failed.")
    else:
        print("Set Counter Config Success : Counter Type %d(CFG_RESET_LOGIC)" % CFG_RESET_LOGIC)

    # Set Counter Comparison Output Logic
    status_result, recv_status = FAS_SetCounterConfig(nBdID, byChannel, CFG_CP_LOGIC, 1)
    if status_result != FMM_OK:
        print("Function(FAS_SetCounterConfig) was failed.")
    else:
        print("Set Counter Config Success : Counter Type %d(CFG_CP_LOGIC)" % CFG_CP_LOGIC)
    return True


def GetCounterConfig(nBdID: int) -> bool:

    byChannel = 0  # Channel = 0

    print("----------------------------------")
    # Get Counter Input Mode
    status_result, data_status = FAS_GetCounterConfig(nBdID, byChannel, CFG_INPUT_MODE)
    if status_result != FMM_OK:
        print("Function(FAS_GetCounterConfig) was failed.")
    else:
        print("Counter Type %d(CFG_INPUT_MODE) : %d" % (CFG_INPUT_MODE, data_status))

    # Get Counter Direction
    status_result, data_status = FAS_GetCounterConfig(
        nBdID, byChannel, CFG_COUNT_DIRECTION
    )
    if status_result != FMM_OK:
        print("Function(FAS_GetCounterConfig) was failed.")
    else:
        print("Counter Type %d(CFG_COUNT_DIRECTION) : %d" % (CFG_COUNT_DIRECTION, data_status))

    # Get Counter Latch A Mode
    status_result, data_status = FAS_GetCounterConfig(nBdID, byChannel, CFG_LATCHA_MODE)
    if status_result != FMM_OK:
        print("Function(FAS_GetCounterConfig) was failed.")
    else:
        print("Counter Type %d(CFG_LATCHA_MODE) : %d" % (CFG_LATCHA_MODE, data_status))

    # Get Counter Latch B Mode
    status_result, data_status = FAS_GetCounterConfig(nBdID, byChannel, CFG_LATCHB_MODE)
    if status_result != FMM_OK:
        print("Function(FAS_GetCounterConfig) was failed.")
    else:
        print("Counter Type %d(CFG_LATCHB_MODE) : %d" % (CFG_LATCHB_MODE, data_status))
    # Get Counter Z-Phase Latch Mode
    status_result, data_status = FAS_GetCounterConfig(nBdID, byChannel, CFG_ZLATCH_MODE)
    if status_result != FMM_OK:
        print("Function(FAS_GetCounterConfig) was failed.")
    else:
        print("Counter Type %d(CFG_ZLATCH_MODE) : %d" % (CFG_ZLATCH_MODE, data_status))

    # Get Counter Latch A Logic
    status_result, data_status = FAS_GetCounterConfig(
        nBdID, byChannel, CFG_LATCHA_LOGIC
    )
    if status_result != FMM_OK:
        print("Function(FAS_GetCounterConfig) was failed.")
    else:
        print("Counter Type %d(CFG_LATCHA_LOGIC) : %d" % (CFG_LATCHA_LOGIC, data_status))

    # Get Counter Latch B Logic
    status_result, data_status = FAS_GetCounterConfig(
        nBdID, byChannel, CFG_LATCHB_LOGIC
    )
    if status_result != FMM_OK:
        print("Function(FAS_GetCounterConfig) was failed.")
    else:
        print("Counter Type %d(CFG_LATCHB_LOGIC) : %d" % (CFG_LATCHB_LOGIC, data_status))

    # Get Counter Z-Phase Latch Logic
    status_result, data_status = FAS_GetCounterConfig(
        nBdID, byChannel, CFG_ZLATCH_LOGIC
    )
    if status_result != FMM_OK:
        print("Function(FAS_GetCounterConfig) was failed.")
    else:
        print("Counter Type %d(CFG_ZLATCH_LOGIC) : %d" % (CFG_ZLATCH_LOGIC, data_status))

    # Get Counter Reset Logic
    status_result, data_status = FAS_GetCounterConfig(nBdID, byChannel, CFG_RESET_LOGIC)
    if status_result != FMM_OK:
        print("Function(FAS_GetCounterConfig) was failed.")
    else:
        print("Counter Type %d(CFG_RESET_LOGIC) : %d" % (CFG_RESET_LOGIC, data_status))

    # Get Counter Comparison Output Logic
    status_result, data_status = FAS_GetCounterConfig(nBdID, byChannel, CFG_CP_LOGIC)
    if status_result != FMM_OK:
        print("Function(FAS_GetCounterConfig) was failed.")
    else:
        print("Counter Type %d(CFG_CP_LOGIC) : %d" % (CFG_CP_LOGIC, data_status))

    return True


def main():
    nBdID = 0

    # Device Connect
    if not Connect(UDP, nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Get Counter Config
    if not GetCounterConfig(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Set Counter Config
    if not SetCounterConfig(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Get Counter Config
    if not GetCounterConfig(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
