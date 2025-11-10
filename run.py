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
import matplotlib.pyplot as plt

try:
    library_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "python","PE", "Library")
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

MTSPEED = 100000

def Connect(nCommType: int, nBdID: int, ip: list) -> bool:
    # ip = [192, 168, 0, 3]  # IP: 192.168.0.2
    bSuccess = True

    # Connection
    if nCommType == TCP:  # TCP Connection
        if FAS_ConnectTCP(ip[0], ip[1], ip[2], ip[3], nBdID) == 0:
            print("TCP Connection Fail!")
            bSuccess = False
    elif nCommType == UDP:  # UDP Connection
        if FAS_Connect(ip[0], ip[1], ip[2], ip[3], nBdID) == 0:
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
    nOrgSearchSpeed = 50000
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
    



def updateAbsPos(nBdID: int, targetAbsPos: int) -> bool:
    print("update initiated")

    status_result, axis_status = FAS_GetAxisStatus(nBdID)
    print( EZISERVO2_AXISSTATUS.FFLAG_MOTIONING)
    print(f"axis status: {axis_status}")
    if (axis_status & EZISERVO2_AXISSTATUS.FFLAG_MOTIONING):
        print("moving MT detected")
        print("moving MT detected")
        print("moving MT detected")
        print("moving MT detected")

        if FAS_PositionAbsOverride(nBdID,targetAbsPos) != FMM_OK:
            print("position override failed")
           
            return False
        else: print(f"posiion Abs Overrided to {targetAbsPos}")
    else:
       
        if FAS_MoveSingleAxisAbsPos(nBdID,targetAbsPos,MTSPEED) != FMM_OK:
            print("position set failed")
            # err_code = FAS_GetPosError(nBdID)
            # err_msg ="w"
            # print(f"Error {err_code}: {err_msg}")
            return False
        else:
            print(f"posiion Abs set to {targetAbsPos}")
            


    return True






# def MoveAbsPos(nBdID: int, targetAbsPos: int) -> bool:

# 	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 	#~~ In this function,												~~
# 	#~~ please modify the value depending on the product you are using.	~~
# 	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#     # Move AxisAbsPos

#     # Move the motor by 0 pulse (target position: Absolute position)
#     nAbsPos = targetAbsPos
#     nVelocity = MTSPEED

#     print("---------------------------")
#     print("[Abs Mode] Move Motor!")

#     if FAS_MoveSingleAxisAbsPos(nBdID, nAbsPos, nVelocity) != FMM_OK:
#         print("Function(FAS_MoveSingleAxisAbsPos) was failed.")
#         return False

#     # Check the Axis status until motor stops and the Inposition value is checked
#     while True:
#         time.sleep(0.001)
#         status_result, axis_status = FAS_GetAxisStatus(nBdID)
#         if status_result != FMM_OK:
#             print("Function(FAS_GetAxisStatus) was failed.")
#             return False

#         if not (axis_status & EZISERVO2_AXISSTATUS.FFLAG_MOTIONING) and (
#             axis_status & EZISERVO2_AXISSTATUS.FFLAG_INPOSITION
#         ):
#             break

#     return True


# def PosAbsOvrride(nBdID: int) -> bool:

# 	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 	#~~ In this function,												~~
# 	#~~ please modify the value depending on the product you are using.	~~
# 	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#     # Move AxisAbsPos & PositionAbsOverride
#     lVelocity = 40000
#     lIncEndPos = 0
#     lActualPos = 0
#     lAbsPos = 0
#     lChangePos = 0

#     status_result, lIncEndPos = FAS_GetActualPos(nBdID)
#     if status_result != FMM_OK:
#         print("Function(FAS_GetActualPos) was failed.")
#         return False

#     print("---------------------------")

#     # 1. Move Command
#     # Move the motor by ((lIncEndPos)* 1/ 4) pulse (target position : Absolute position)
#     lAbsPos = lIncEndPos // 4

#     if FAS_MoveSingleAxisAbsPos(nBdID, lAbsPos, lVelocity) != FMM_OK:
#         print("Function(FAS_MoveSingleAxisAbsPos) was failed.")
#         return False
#     print("[ABS Mode] Move Motor Start!")

#     # 2. Check Condition
#     # Check current position
#     while True:
#         time.sleep(0.001)

#         status, lActualPos = FAS_GetActualPos(nBdID)
#         if status != FMM_OK:
#             print("Function(FAS_GetActualPos) was failed.")
#             break

#         if lActualPos < (lIncEndPos / 2):
#             break

#     # 3. Change Position
#     # if the current position falls below half the INC End position, change the target position to zero.
#     lChangePos = 400000
#     if FAS_PositionAbsOverride(nBdID, lChangePos) != FMM_OK:
#         print("Function(FAS_PositionAbsOverride) was failed.")
#         return False
#     else:
#         print(
#             "Before Target Position: %d[pulse] / Change Target Position: %d[pulse]"
#             % (lAbsPos, lChangePos)
#         )

#     # 4. Confirm Move Complete
#     # Check the Axis status until motor stops and the Inposition value is checked
#     while True:
#         time.sleep(0.001)
#         status_result, axis_status = FAS_GetAxisStatus(nBdID)
#         if status_result != FMM_OK:
#             print("Function(FAS_GetAxisStatus) was failed.")
#             return False

#         if not (axis_status & EZISERVO2_AXISSTATUS.FFLAG_MOTIONING) and (
#             axis_status & EZISERVO2_AXISSTATUS.FFLAG_INPOSITION
#         ):
#             break

#     return True
def calculateTargetAbsPositionAtTime(t:float) -> float:

    # max_pos = 200000
    match t:
        case _ if t < 2.5:
            absPos = 80000 * t
        case _ if 2.5 <= t < 5:
            absPos = -40000*t + 300000
        case _ if 5<=t<7.5:
            absPos = 40000*t - 100000
        case _ if 7.5<=t<10:
            absPos = -80000 * t +800000
        case _ :
            absPos = 0
    return absPos
def getCurrentPosition(nBdID: int) -> int:
    status, lActualPos = FAS_GetActualPos(nBdID)
    return lActualPos

def plotChart(times,targetPositions,currentPositions):
    plt.figure(figsize=(8,4))
    plt.plot(times, currentPositions, label='Current Position')
    plt.plot(times, targetPositions, label='Target Position', linestyle='--')
    plt.xlabel('Time [s]')
    plt.ylabel('Position')
    plt.title('Position Tracking')
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig("logs/plot_position.png")

def main():
    nBdIDPosition = 0
    ipPosition = [192,168,0,3]
    nBdIDAngular = 1
    ipAngular = [192,168,0,2]
    currentTime = 0
    dt = 0.1
    currentPositions = []
    targetPositions = []
    times = []

    # Device Connect
    if not Connect(TCP, nBdIDPosition,ipPosition) or not Connect(TCP, nBdIDAngular, ipAngular):
        input("Press Enter to exit...")
        exit(1)

    # Drive Error Check
    if not CheckDriveErr(nBdIDPosition) or not CheckDriveErr(nBdIDAngular):
        input("Press Enter to exit...")
        exit(1)

    # ServoOn
    if not SetServoOn(nBdIDPosition) or not SetServoOn(nBdIDAngular):
        input("Press Enter to exit...")
        exit(1)

    
       # Set Origin Parameter
    if not SetOriginParameter(nBdIDPosition)or not SetOriginParameter(nBdIDAngular):
        input("Press Enter to exit...")
        exit(1)

    # Act Origin Search Function
    if not OriginSearch(nBdID):
        input("Press Enter to exit...")
        exit(1)

        

    # Move AxisAbsPos & PositionAbsOverride
    
    for i in range(0,100):

        targetAbsPos = round(calculateTargetAbsPositionAtTime(t=currentTime))

        if not updateAbsPos(nBdID,targetAbsPos=targetAbsPos):
            input("updated failed: Press Enter to exit...")
            exit(1)
        times.append(currentTime)
        currentPosition = getCurrentPosition(nBdID)
        currentPositions.append(currentPosition)
        targetPositions.append(targetAbsPos)

        currentTime += dt
        time.sleep(dt)

    # Connection Close
    print("fas close called")
    FAS_Close(nBdID)
    plotChart(times,targetPositions,currentPositions)


    input("Press Enter to exit...")


if __name__ == "__main__":
    main()

