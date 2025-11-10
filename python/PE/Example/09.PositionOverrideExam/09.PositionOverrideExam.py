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

INCPOS = 200000  # IncMove Target Position
ABSPOS = 0  # AbsMove Target Position


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


def CheckDriveErr(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


def PosIncOverride(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Move AxisIncPos & PositionIncOverride
    lIncPos = INCPOS
    lVelocity = 20000
    lActualPos = 0
    lChangePos = 0
    lPosDetect = 100000

    print("---------------------------")
    print("[Inc Mode] Move Motor Start!")

    # 1. Move Command
    # Move the motor by INCPOS(200000) [pulse]
    if FAS_MoveSingleAxisIncPos(nBdID, lIncPos, lVelocity) != FMM_OK:
        print("Function(FAS_MoveSingleAxisIncPos) was failed.")
        return False

    # 2. Check Condition
    # Check current position
    while True:
        time.sleep(0.001)
        status_result, lActualPos = FAS_GetActualPos(nBdID)
        if status_result != FMM_OK:
            print("Funtion(FAS_GetActualPos) was failed.")
            return False
        if lActualPos > lPosDetect:
            break

    # 3. Change Position
    # If the current position is less than the target position, change final position.
    lChangePos += lIncPos
    if FAS_PositionIncOverride(nBdID, lChangePos) != FMM_OK:
        print("Function(FAS_PositionIncOverride) was failed.")
        return False
    else:
        print(
            "[Before] Target Position : %d[pulse] / [After] Target Position : %d[pulse]"
            % (lIncPos, lChangePos + lIncPos)
        )
    # 4. Confirm Move Complete
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


def PosAbsOvrride(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # Move AxisAbsPos & PositionAbsOverride
    lVelocity = 40000
    lIncEndPos = 0
    lActualPos = 0
    lAbsPos = 0
    lChangePos = 0

    status_result, lIncEndPos = FAS_GetActualPos(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetActualPos) was failed.")
        return False

    print("---------------------------")

    # 1. Move Command
    # Move the motor by ((lIncEndPos)* 1/ 4) pulse (target position : Absolute position)
    lAbsPos = lIncEndPos // 4

    if FAS_MoveSingleAxisAbsPos(nBdID, lAbsPos, lVelocity) != FMM_OK:
        print("Function(FAS_MoveSingleAxisAbsPos) was failed.")
        return False
    print("[ABS Mode] Move Motor Start!")

    # 2. Check Condition
    # Check current position
    while True:
        time.sleep(0.001)

        status, lActualPos = FAS_GetActualPos(nBdID)
        if status != FMM_OK:
            print("Function(FAS_GetActualPos) was failed.")
            break

        if lActualPos < (lIncEndPos / 2):
            break

    # 3. Change Position
    # if the current position falls below half the INC End position, change the target position to zero.
    lChangePos = ABSPOS
    if FAS_PositionAbsOverride(nBdID, lChangePos) != FMM_OK:
        print("Function(FAS_PositionAbsOverride) was failed.")
        return False
    else:
        print(
            "Before Target Position: %d[pulse] / Change Target Position: %d[pulse]"
            % (lAbsPos, lChangePos)
        )

    # 4. Confirm Move Complete
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
    nBdID = 0

    # Device Connect
    if not Connect(TCP, nBdID):
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

    # Move AxisIncPos & PositionIncOverride
    if not PosIncOverride(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Move AxisAbsPos & PositionAbsOverride
    if not PosAbsOvrride(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
