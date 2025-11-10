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


def CounterCommand(nBdID: int) -> bool:
    byChannel = 0  # Channel = 0

    print("----------------------------------")
    # Set Counter Command Channel Enable
    if FAS_CounterCommand(nBdID, byChannel, CNTCMD_CH_ENABLE, 1) != FMM_OK:
        print("Function(FAS_CounterCommand) was failed.")
    else:
        print("Set Counter Command Success : Counter Type %d(CNTCMD_CH_ENABLE)" % CNTCMD_CH_ENABLE)

    # Set Counter Command Latch A Enable
    if FAS_CounterCommand(nBdID, byChannel, CNTCMD_LATCHA_ENABLE, 1) != FMM_OK:
        print("Function(FAS_CounterCommand) was failed.")
    else:
        print("Set Counter Command Success : Counter Type %d(CNTCMD_LATCHA_ENABLE)" % CNTCMD_LATCHA_ENABLE)

    # Set Counter Command Latch B Enable
    if FAS_CounterCommand(nBdID, byChannel, CNTCMD_LATCHB_ENABLE, 1) != FMM_OK:
        print("Function(FAS_CounterCommand) was failed.")
    else:
        print("Set Counter Command Success : Counter Type %d(CNTCMD_LATCHB_ENABLE)" % CNTCMD_LATCHB_ENABLE)

    # Set Counter Command Z-Phase Latch Enable
    if FAS_CounterCommand(nBdID, byChannel, CNTCMD_ZLATCH_ENABLE, 1) != FMM_OK:
        print("Function(FAS_CounterCommand) was failed.")
    else:
        print("Set Counter Command Success : Counter Type %d(CNTCMD_ZLATCH_ENABLE)" % CNTCMD_ZLATCH_ENABLE)

    # Set Counter Command Reset All
    if FAS_CounterCommand(nBdID, byChannel, CNTCMD_RESET_ALL, 1) != FMM_OK:
        print("Function(FAS_CounterCommand) was failed.")
    else:
        print("Set Counter Command Success : Counter Type %d(CNTCMD_RESET_ALL)" % CNTCMD_RESET_ALL)

    # Set Counter Command Reset Count
    if FAS_CounterCommand(nBdID, byChannel, CNTCMD_RESET_COUNT, 1) != FMM_OK:
        print("Function(FAS_CounterCommand) was failed.")
    else:
        print("Set Counter Command Success : Counter Type %d(CNTCMD_RESET_COUNT)" % CNTCMD_RESET_COUNT)

    # Set Counter Command Reset Latch
    if FAS_CounterCommand(nBdID, byChannel, CNTCMD_RESET_LATCH, 1) != FMM_OK:
        print("Function(FAS_CounterCommand) was failed.")
    else:
        print("Set Counter Command Success : Counter Type %d(CNTCMD_RESET_LATCH)" % CNTCMD_RESET_LATCH)

    return True


def GetCounterStatus(nBdID: int) -> bool:

    print("----------------------------------")
    # Get Counter Status
    status_result, dwStatus = FAS_GetCounterStatus(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetCounterStatus) was failed.")
    else:
        print("Counter Status : 0x%08x" % dwStatus)

    return True


def main():
    nBdID = 0

    # Device Connect
    if not Connect(UDP, nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Get Counter Config
    if not GetCounterStatus(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Set Counter Config
    if not CounterCommand(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Get Counter Config
    if not GetCounterStatus(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
