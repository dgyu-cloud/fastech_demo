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

SLAVE_CNT = 2


def Connect(nCommType: int, byIP: int, nBdID: int) -> bool:
    bSuccess = True

    # Connection
    if nCommType == TCP:
        # TCP Connection
        if not FAS_ConnectTCP(byIP[0], byIP[1], byIP[2], byIP[3], nBdID):
            print("[nBdID : %d ] TCP Connection Fail!" % nBdID)
            bSuccess = False
    elif nCommType == UDP:
        # UDP Connection
        if not FAS_Connect(byIP[0], byIP[1], byIP[2], byIP[3], nBdID):
            print("[nBdID : %d ] UDP Connection Fail!" % nBdID)
            bSuccess = False
    else:
        print("[nBdID : %d ] Wrong communication type." % nBdID)
        bSuccess = False

    if bSuccess:
        print("[nBdID : %d ] Connected successfully." % nBdID)

    return bSuccess


def CheckDriveErr(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Check Drive's Error
    status_result, axis_status = FAS_GetAxisStatus(nBdID)

    if status_result != FMM_OK:
        print("[nBdID : %d ] Function(FAS_GetAxisStatus) was failed." % nBdID)
        return False

    if axis_status & EZISERVO2_AXISSTATUS.FFLAG_ERRORALL:
        # if Drive's Error was detected, Reset the ServoAlarm
        if FAS_ServoAlarmReset(nBdID) != FMM_OK:
            print("[nBdID : %d ] Function(FAS_ServoAlarmReset) was failed." % nBdID)
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
        print("[nBdID : %d ] Function(FAS_GetAxisStatus) was failed." % nBdID)
        return False

    # if ServoOnFlagBit is OFF("0"), switch to ON("1")
    if (axis_status & EZISERVO2_AXISSTATUS.FFLAG_SERVOON) == 0:
        if FAS_ServoEnable(nBdID, 1) != FMM_OK:
            print("[nBdID : %d ] Function(FAS_ServoEnable) was failed." % nBdID)
            return False

        while (
            axis_status & EZISERVO2_AXISSTATUS.FFLAG_SERVOON
        ) == 0:  # Wait until FFLAG_SERVOON is ON
            time.sleep(0.001)

            status_result, axis_status = FAS_GetAxisStatus(nBdID)
            if status_result != FMM_OK:
                print("[nBdID : %d ] Function(FAS_GetAxisStatus) was failed." % nBdID)
                return False

            if (axis_status & EZISERVO2_AXISSTATUS.FFLAG_SERVOON) != 0:
                print("[nBdID : %d ] Servo ON" % nBdID)

    else:
        print("[nBdID : %d ] Servo is already ON" % nBdID)

    return True


def MoveLinearIncPos(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Move Linear IncPos
    lIncPos = [370000, 370000]
    wAccelTime = 100

    print("---------------------------")
    # Increase the motor by 370000 pulse (target position : Relative position)

    lVelocity = 40000

    print("[Linear Inc Mode] Move Motor!")

    if FAS_MoveLinearIncPos2(2, nBdID, lIncPos, lVelocity, wAccelTime) != FMM_OK:
        print("Function(FAS_MoveLinearIncPos2) was failed.")
        return False
    # Check the Axis status until motor stops and the Inposition value is checked
    for nID in range(SLAVE_CNT):
        while True:
            time.sleep(0.001)
            status_result, axis_status = FAS_GetAxisStatus(nID)

            if status_result != FMM_OK:
                print("[nBdID : %d ] Function(FAS_GetAxisStatus) was failed." % nID)
                return False

            if (
                not axis_status & EZISERVO2_AXISSTATUS.FFLAG_MOTIONING
                and axis_status & EZISERVO2_AXISSTATUS.FFLAG_INPOSITION
            ):
                break
    return True


def MoveLinearAbsPos(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Move Linear AbsPos
    lAbsPos = [0, 0]
    wAccelTime = 100

    print("---------------------------")

    # Move the motor by 0 pulse (target position : Absolute position)
    lVelocity = 40000

    print("[Linear Abs Mode] Move Motor!")
    if FAS_MoveLinearAbsPos2(2, nBdID, lAbsPos, lVelocity, wAccelTime) != FMM_OK:
        print("Function(FAS_MoveLinearAbsPos2) was failed.")
        return False

    # Check the Axis status until motor stops and the Inposition value is checked
    for nID in range(SLAVE_CNT):
        while True:
            time.sleep(0.001)
            status_result, axis_status = FAS_GetAxisStatus(nID)
            if status_result != FMM_OK:
                print("[nBdID : %d ] Function(FAS_GetAxisStatus) was failed." % nID)
                return False

            if (
                not axis_status & EZISERVO2_AXISSTATUS.FFLAG_MOTIONING
                and axis_status & EZISERVO2_AXISSTATUS.FFLAG_INPOSITION
            ):
                break
    return True


def main():
    byIP = [[192, 168, 0, 2], [192, 168, 0, 5]]

    nBdID = [0, 1]
    for nID in range(SLAVE_CNT):
        # Device Connect
        if not Connect(TCP, byIP[nID], nBdID[nID]):
            input("Press Enter to exit...")
            sys.exit(1)

        # Drive Error Check
        if not CheckDriveErr(nBdID[nID]):
            input("Press Enter to exit...")
            sys.exit(1)

        # Servo On
        if not SetServoOn(nBdID[nID]):
            input("Press Enter to exit...")
            sys.exit(1)

    # Move Linear IncPos
    if not MoveLinearIncPos(nBdID):
        input("Press Enter to exit...")
        sys.exit(1)

    # Move Linear AbsPos
    if not MoveLinearAbsPos(nBdID):
        input("Press Enter to exit...")
        sys.exit(1)

    # Connection Close
    for nID in range(SLAVE_CNT):
        FAS_Close(nBdID[nID])

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
