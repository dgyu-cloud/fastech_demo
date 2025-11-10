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

TRUE = 1
FALSE = 0


def Connect(nCommType: int, nBdID: int) -> bool:
    byIP = [192, 168, 0, 2]  # IP: 192.168.0.2
    bSuccess = True

    # Connection
    if nCommType == TCP:  # TCP Connection
        if FAS_ConnectTCP(byIP[0], byIP[1], byIP[2], byIP[3], nBdID) == FALSE:
            print("TCP Connection Fail!")
            bSuccess = False
    elif nCommType == UDP:  # UDP Connection
        if FAS_Connect(byIP[0], byIP[1], byIP[2], byIP[3], nBdID) == FALSE:
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

    # if ServoOnFlagBit is OFF("0"), switch to ON("1")
    if status_result != FMM_OK:
        print("Function(FAS_GetAxisStatus) was failed.")
        return False

    # If the servo is OFF("0"), switch to ON("1")
    if (axis_status & EZISERVO2_AXISSTATUS.FFLAG_SERVOON) == 0:
        if FAS_ServoEnable(nBdID, TRUE) != FMM_OK:
            print("Function(FAS_ServoEnable) was failed.")
            return False

        # Wait until FFLAG_SERVOON is ON
        while (axis_status & EZISERVO2_AXISSTATUS.FFLAG_SERVOON) == 0:
            time.sleep(0.001)  # Wait for 1 millisecond

            status_result, axis_status = FAS_GetAxisStatus(nBdID)
            if status_result != FMM_OK:
                print("Function(FAS_GetAxisStatus) was failed.")
                return False

            if (axis_status & EZISERVO2_AXISSTATUS.FFLAG_SERVOON) != 0:
                print("Servo ON")

    else:
        print("Servo is already ON")

    return True


def MovePos(nBdID: int, nDistance: int, nAccDecTime: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # SetParameter & MoveSingleAxisIncPos
    lIncPos = nDistance
    lVelocity = 40000

    # Set Acc Time
    if FAS_SetParameter(nBdID, SERVO2_AXISACCTIME, nAccDecTime) != FMM_OK:
        print("Function(FAS_SetParameter) was failed.")
        return False

    # Set Dec Time
    if FAS_SetParameter(nBdID, SERVO2_AXISDECTIME, nAccDecTime) != FMM_OK:
        print("Function(FAS_SetParameter) was failed.")
        return False

    print("---------------------------")

    # Move the motor by [nDistance] pulse (target position : Absolute position)
    lIncPos = nDistance
    lVelocity = 40000

    print("Move Motor! \n")

    if FAS_MoveSingleAxisIncPos(nBdID, lIncPos, lVelocity) != FMM_OK:
        print("Function(FAS_MoveSingleAxisIncPos) was failed.")
        return False

    # Check the Axis status until FFLAG_MOTIONING is ON
    while True:
        time.sleep(0.001)
        status_result, axis_status = FAS_GetAxisStatus(nBdID)
        if status_result != FMM_OK:
            print("Function(FAS_GetAxisStatus) was failed.")
            return False

        if not axis_status & EZISERVO2_AXISSTATUS.FFLAG_MOTIONING:
            break

    return True


def MovePosEx(nBdID: int, nDistance: int, nAccDecTime: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # MoveSingleAxisIncPosEx
    opt = MOTION_OPTION_EX(
        BIT_IGNOREEXSTOP=0,
        BIT_USE_CUSTOMACCEL=1,
        BIT_USE_CUSTOMDECEL=1,
        wCustomAccelTime=nAccDecTime,
        wCustomDecelTime=nAccDecTime
    )
    lIncPos = nDistance
    lVelocity = 40000

    print("---------------------------")
    print("Move Motor! [Ex]\n")

    if FAS_MoveSingleAxisIncPosEx(nBdID, lIncPos, lVelocity, opt) != FMM_OK:
        print("Function(FAS_MoveSingleAxisIncPosEx) was failed.")
        return False

    # Check the Axis status until motor stops and the Inposition value is checked
    while True:
        time.sleep(0.001)
        status_result, axis_status = FAS_GetAxisStatus(nBdID)
        if status_result != FMM_OK:
            print("Function(FAS_GetAxisStatus) was failed.")
            return False

        if (
            not axis_status & EZISERVO2_AXISSTATUS.FFLAG_MOTIONING
            and axis_status & EZISERVO2_AXISSTATUS.FFLAG_INPOSITION
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

    # SetParameter and Move

    # AccDecTime = 100 ms
    distance = 100000
    accdec = 100
    if not MovePos(nBdID, distance, accdec):
        input("Press Enter to exit...")

    # AccDecTime = 200 ms
    distance = -100000
    accdec = 200
    if not MovePos(nBdID, distance, accdec):
        input("Press Enter to exit...")

    # AccDecTime = 300 ms
    distance = 100000
    accdec = 300
    if not MovePos(nBdID, distance, accdec):
        input("Press Enter to exit...")

    # MoveEX

    # AccDecTime = 100 ms
    distance = -100000
    accdec = 100
    if not MovePosEx(nBdID, distance, accdec):
        input("Press Enter to exit...")

    # AccDecTime = 200 ms
    distance = 100000
    accdec = 2000
    if not MovePosEx(nBdID, distance, accdec):
        input("Press Enter to exit...")

    # AccDecTime = 300 ms
    distance = -100000
    accdec = 300
    if not MovePosEx(nBdID, distance, accdec):
        input("Press Enter to exit...")

    # Connection close
    FAS_Close(nBdID)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
