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

    # if ServoOnFlagBit is OFF("0"), switch to ON("1")
    status_result, axis_status = FAS_GetAxisStatus(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetAxisStatus) was failed.")
        return False

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


def JogMove(nBdID: int, nAccDecTime: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # SetParameter & MoveVelocity
    nTargetVeloc = 100000
    nDirect = 1
    nSeconds = 3  # Wait 3 Sec

    # Set Jog Acc/Dec Time
    if FAS_SetParameter(nBdID, SERVO2_JOGACCDECTIME, nAccDecTime) != FMM_OK:
        print("Function(FAS_SetParameter) was failed.")
        return False

    print("---------------------------")
    if FAS_MoveVelocity(nBdID, nTargetVeloc, nDirect) != FMM_OK:
        print("Function(FAS_MoveVelocity) was failed.")
        return False

    print("Move Motor(Jog Mode)!")
    time.sleep(nSeconds)

    if FAS_MoveStop(nBdID) != FMM_OK:
        print("Function(FAS_MoveStop) was failed.")
        return False

    # Wait until FFLAG_MOTIONING is OFF
    while True:
        time.sleep(0.001)
        status_result, axis_status = FAS_GetAxisStatus(nBdID)
        if status_result != FMM_OK:
            print("Function(FAS_GetAxisStatus) was failed.")
            return False

        if not (axis_status & EZISERVO2_AXISSTATUS.FFLAG_MOTIONING):
            print("Move Stop!")
            break

    return True


def JogExMove(nBdID: int, nAccDecTime: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # MoveVelocityEx

    # Set velocity
    nDirect = 1
    lVelocity = 30000
    nSeconds = 3  # Wait 3 Sec

    # set user setting bit(BIT_USE_CUSTOMACCDEC) and acel/decel time value
    opt = VELOCITY_OPTION_EX(BIT_USE_CUSTOMACCDEC=1, wCustomAccDecTime=nAccDecTime)

    print("-----------------------------------------------------------")
    if FAS_MoveVelocityEx(nBdID, lVelocity, nDirect, opt) != FMM_OK:
        print("Function(FAS_MoveVelocityEx) was failed.")
        return False

    print("Move Motor(Jog Ex Mode)!")
    time.sleep(nSeconds)

    if FAS_MoveStop(nBdID) != FMM_OK:
        print("Function(FAS_MoveStop) was failed.")
        return False

    # Wait until FFLAG_MOTIONING is OFF
    while True:
        time.sleep(0.001)
        status_result, axis_status = FAS_GetAxisStatus(nBdID)
        if status_result != FMM_OK:
            print("Function(FAS_GetAxisStatus) was failed.")
            return False

        if not (axis_status & EZISERVO2_AXISSTATUS.FFLAG_MOTIONING):
            print("Move Stop!")
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

    # MoveVelocity with AccDecTime = 100
    if not JogMove(nBdID, 100):
        input("Press Enter to exit...")
        exit(1)

    # MoveVelocity with AccDecTime = 200
    if not JogMove(nBdID, 200):
        input("Press Enter to exit...")
        exit(1)

    # MoveVelocity with AccDecTime = 300
    if not JogMove(nBdID, 300):
        input("Press Enter to exit...")
        exit(1)

    # MoveVelocityEx with AccDecTime = 100
    if not JogExMove(nBdID, 100):
        input("Press Enter to exit...")
        exit(1)

    # MoveVelocityEx with AccDecTime = 200
    if not JogExMove(nBdID, 200):
        input("Press Enter to exit...")
        exit(1)

    # MoveVelocityEx with AccDecTime = 300
    if not JogExMove(nBdID, 300):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
