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

CW = 0
CCW = 1


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


def SetOriginParameter(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Set Origin Parameter
    nOrgSpeed = 50000
    nOrgSearchSpeed = 1000
    nOrgAccDecTime = 50
    nOrgMethod = (
        0  # Origin Method = 2 is 'Limit Origin' in the Ezi-SERVOII Plus-E model
    )
    nOrgDir = CW
    nOrgOffset = 0
    nOrgPositionSet = 0
    nOrgTorqueRatio = 50

    if FAS_SetParameter(nBdID, SERVO2_ORGSPEED, nOrgSpeed) != FMM_OK:
        print("Function(FAS_SetParameter[SERVO2_ORGSPEED]) was failed.")
        return False

    if FAS_SetParameter(nBdID, SERVO2_ORGSEARCHSPEED, nOrgSearchSpeed) != FMM_OK:
        print("Function(FAS_SetParameter[SERVO2_ORGSEARCHSPEED]) was failed.")
        return False

    if FAS_SetParameter(nBdID, SERVO2_ORGACCDECTIME, nOrgAccDecTime) != FMM_OK:
        print("Function(FAS_SetParameter[SERVO2_ORGACCDECTIME]) was failed.")
        return False

    if FAS_SetParameter(nBdID, SERVO2_ORGMETHOD, nOrgMethod) != FMM_OK:
        print("Function(FAS_SetParameter[SERVO2_ORGMETHOD]) was failed.")
        return False

    if FAS_SetParameter(nBdID, SERVO2_ORGDIR, nOrgDir) != FMM_OK:
        print("Function(FAS_SetParameter[SERVO2_ORGDIR]) was failed.")
        return False

    if FAS_SetParameter(nBdID, SERVO2_ORGOFFSET, nOrgOffset) != FMM_OK:
        print("Function(FAS_SetParameter[SERVO2_ORGOFFSET]) was failed.")
        return False

    if FAS_SetParameter(nBdID, SERVO2_ORGPOSITIONSET, nOrgPositionSet) != FMM_OK:
        print("Function(FAS_SetParameter[SERVO2_ORGPOSITIONSET]) was failed.")
        return False

    if FAS_SetParameter(nBdID, SERVO2_ORGTORQUERATIO, nOrgTorqueRatio) != FMM_OK:
        print("Function(FAS_SetParameter[SERVO2_ORGTORQUERATIO]) was failed.")
        return False

    return True


def OriginSearch(nBdID: int) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Act Origin Search Function
    print("---------------------------")

    # Origin Search Start
    if FAS_MoveOriginSingleAxis(nBdID) != FMM_OK:
        print("Function(FAS_MoveOriginSingleAxis) was failed.")
        return False

    # Check the Axis status until OriginReturning value is released.

    while True:
        time.sleep(0.001)

        status_result, axis_status = FAS_GetAxisStatus(nBdID)
        if status_result != FMM_OK:
            print("Function(FAS_GetAxisStatus) was failed.")
            return False

        if not (axis_status & EZISERVO2_AXISSTATUS.FFLAG_ORIGINRETURNING):
            break

    if axis_status & EZISERVO2_AXISSTATUS.FFLAG_ORIGINRETOK:
        print("Origin Search Success!")
        return True
    else:
        print("Origin Search Fail!")
        return False


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

    # Set Origin Parameter
    if not SetOriginParameter(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Act Origin Search Function
    if not OriginSearch(nBdID):
        input("Press Enter to exit...")
        exit(1)

    # Connection Close
    FAS_Close(nBdID)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
