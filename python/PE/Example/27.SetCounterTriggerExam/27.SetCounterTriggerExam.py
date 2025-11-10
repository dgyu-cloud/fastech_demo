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


def Connect(nCommType: int, nBdID: int, nBdID2: int) -> bool:
    byIP = [192, 168, 0, 2]  # IP: 192.168.0.2   Encoder
    byIP2 = [192, 168, 0, 3]  # IP: 192.168.0.3  I/O Counter
    bSuccess = True

    # Connection
    if nCommType == TCP:  # TCP Connection
        if FAS_ConnectTCP(byIP[0], byIP[1], byIP[2], byIP[3], nBdID) == 0:
            print("TCP Connection Fail!")
            bSuccess = False
        if FAS_ConnectTCP(byIP2[0], byIP2[1], byIP2[2], byIP2[3], nBdID2) == 0:
            print("TCP Connection Fail!")
            bSuccess = False
    elif nCommType == UDP:  # UDP Connection
        if FAS_Connect(byIP[0], byIP[1], byIP[2], byIP[3], nBdID) == 0:
            print("UDP Connection Fail!")
            bSuccess = False
        if FAS_Connect(byIP2[0], byIP2[1], byIP2[2], byIP2[3], nBdID2) == 0:
            print("TCP Connection Fail!")
            bSuccess = False
    else:
        print("Wrong communication type.")
        bSuccess = False

    if bSuccess:
        print("Connected successfully.")

    return bSuccess


def CheckDriveErr(nBdID: int) -> bool:

    # Check Drive's Error
    status_result, axis_status = FAS_GetAxisStatus(nBdID)

    if status_result != FMM_OK:
        print("Function(FAS_GetAxisStatus) was failed.")
        return False

    if axis_status & EZISERVO2_AXISSTATUS.FFLAG_ERRORALL:
        # if Drive's Error was detected, Reset the ServoAlarm
        if FAS_ServoAlarmReset(nBdID) != FMM_OK:
            print("Function(FAS_ServoAlarmReset) was failed.")
            return False

    return True


def SetServoOn(nBdID: int) -> bool:
    # Check Drive's Servo Status
    status_result, axis_status = FAS_GetAxisStatus(nBdID)

    if status_result != FMM_OK:
        print("Function(FAS_GetAxisStatus) was failed.")
        return False

    # if ServoOnFlagBit is OFF("0"), switch to ON("1")
    if (axis_status & EZISERVO2_AXISSTATUS.FFLAG_SERVOON) == 0:
        if FAS_ServoEnable(nBdID, 1) != FMM_OK:
            print("Function(FAS_ServoEnable) was failed.")
            return False

        while (
            axis_status & EZISERVO2_AXISSTATUS.FFLAG_SERVOON
        ) == 0:  # Wait until FFLAG_SERVOON is ON
            time.sleep(0.001)

            status_result, axis_status = FAS_GetAxisStatus(nBdID)
            if status_result != FMM_OK:
                print("Function(FAS_GetAxisStatus) was failed.")
                return False

            if (axis_status & EZISERVO2_AXISSTATUS.FFLAG_SERVOON) != 0:
                print("Servo ON")

    else:
        print("Servo is already ON")

    return True


def SetCounterTrigger(nBdID: int, nBdID2: int) -> bool:
    byChannel = 0
    bStartTrigger = True
    lStartPos = 50000
    dwPeriod = 50000
    dwPulseTime = 500
    dwTriggerCount = 10

    # Set Counter Enable
    if FAS_CounterCommand(nBdID2, byChannel, CNTCMD_CH_ENABLE, 1) != FMM_OK:
        print("Function(FAS_CounterCommand) was failed.")
        return False
    else:
        print("FAS_CounterCommand Success!")

    # Reset Counter
    if FAS_CounterCommand(nBdID2, byChannel, CNTCMD_RESET_ALL, 0) != FMM_OK:
        print("Function(FAS_CounterCommand) was failed.")
        return False
    else:
        print("FAS_CounterCommand Success!")

    # Set Counter Trigger
    if (
        FAS_SetCounterTrigger(
            nBdID2,
            byChannel,
            bStartTrigger,
            lStartPos,
            dwPeriod,
            dwPulseTime,
            dwTriggerCount,
        )
        != FMM_OK
    ):
        print("Function(FAS_SetCounterTrigger) was failed.")
        return False
    else:
        print("FAS_SetCounterTrigger Success!")

    print("---------------------------")
    # Increase the motor by 500000 pulse (target position : Relative position)
    lIncPos = 500000
    lVelocity = 30000

    print("[Inc Mode] Move Motor !")

    if FAS_MoveSingleAxisIncPos(nBdID, lIncPos, lVelocity) != FMM_OK:
        print("Function(FAS_MoveSingleAxisIncPos) was failed.")
        return False

    # Check the Axis status until motor stops and the Inposition value is checked
    while True:
        time.sleep(0.001)
        status_result, axis_status = FAS_GetAxisStatus(nBdID)
        if status_result != FMM_OK:
            print("Function(FAS_GetAxisStatus) was failed.")
            return False

        if not (axis_status & EZISERVO2_AXISSTATUS.FFLAG_MOTIONING) and (
            axis_status & EZISERVO2_AXISSTATUS.FFLAG_INPOSITION
        ):
            break

    return True


def main():
    # nBdID: Encoder,	nBdID2: I/O Counter
    nBdID = 0
    nBdID2 = 1

    # Device Connect
    if not Connect(TCP, nBdID, nBdID2):
        input("Press Enter to exit...")
        exit(1)

    # Drive Error Check
    if not CheckDriveErr(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # ServoOn
    if not SetServoOn(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Set Counter Trigger
    if not SetCounterTrigger(nBdID, nBdID2):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)
    FAS_Close(nBdID2)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
