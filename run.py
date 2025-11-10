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
        print("Connected successfully!.")

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




def MoveAbsPos(nBdID: int, nAbsPos, nVelocity) -> bool:

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#~~ In this function,												~~
	#~~ please modify the value depending on the product you are using.	~~
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # Move AxisAbsPos

    # Move the motor by 0 pulse (target position: Absolute position)
   

    print("---------------------------")
    print("[Abs Mode] Move Motor!")

    if FAS_MoveSingleAxisAbsPos(nBdID, nAbsPos, nVelocity) != FMM_OK:
        print("Function(FAS_MoveSingleAxisAbsPos) was failed.")
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

def SetServoOff(nBdID: int) -> bool:
    """
    Turn servo OFF for the given board ID.
    """

    # 현재 축 상태 읽기
    status_result, axis_status = FAS_GetAxisStatus(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetAxisStatus) failed.")
        return False

    # Servo가 켜져 있으면 끄기
    if (axis_status & EZISERVO2_AXISSTATUS.FFLAG_SERVOON) != 0:
        # Servo Disable
        if FAS_ServoEnable(nBdID, 0) != FMM_OK:
            print("Function(FAS_ServoEnable) failed.")
            return False

        # OFF 될 때까지 대기
        while (axis_status & EZISERVO2_AXISSTATUS.FFLAG_SERVOON) != 0:
            time.sleep(0.001)
            status_result, axis_status = FAS_GetAxisStatus(nBdID)
            if status_result != FMM_OK:
                print("Function(FAS_GetAxisStatus) failed.")
                return False

            if (axis_status & EZISERVO2_AXISSTATUS.FFLAG_SERVOON) == 0:
                print("Servo OFF")

    else:
        print("Servo is already OFF")

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
        2  # Origin Method = 2 is 'Limit Origin' in the Ezi-SERVOII Plus-E model
    )
    nOrgDir = CCW
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
    print("origin paramenter set successfully")
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



def calculateTargetAbsPositionAtTime(t:float) -> float:
    return 10000

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




def checkConnection(nBdIDPosition,ipPosition,nBdIDAngular,ipAngular):
    

    # Device Connect
    if not Connect(TCP, nBdIDPosition,ipPosition) or not Connect(TCP, nBdIDAngular, ipAngular):
        return False

    # Drive Error Check
    if not CheckDriveErr(nBdIDPosition) or not CheckDriveErr(nBdIDAngular):
        input("Press Enter to exit...")
        return False

    # ServoOn
    if not SetServoOn(nBdIDPosition) or not SetServoOn(nBdIDAngular):
        input("Press Enter to exit...")
        return False

    return True

def initializePositionMotor(nBdIDPosition):
    
       # Set Origin Parameter
    if not SetOriginParameter(nBdIDPosition):
       return False

    # Act Origin Search Function
    if not OriginSearch(nBdIDPosition):
        input("Press Enter to exit...")
        return False
    return True

def exitProcess(nBdIDPosition,nBdIDAngular):
    SetServoOff(nBdIDPosition)
    SetServoOff(nBdIDAngular)
    FAS_Close(nBdIDPosition)
    FAS_Close(nBdIDAngular)
    exit(1)

def initialJointing(nBdIDPosition,nBdIDAngular,positionMotorInitialLocation,angularMotorInitialJointingSpeed):

    if FAS_MoveVelocity(nBdIDAngular,angularMotorInitialJointingSpeed,CW) != FMM_OK:
        print("ang motor can not rotate")
        return False
    
    if not MoveAbsPos(nBdID=nBdIDPosition, nAbsPos=positionMotorInitialLocation, nVelocity=MTSPEED):
    # if FAS_MoveSingleAxisAbsPos(nBdIDPosition,positionMotorInitialLocation,MTSPEED) != FMM_OK:
        return False
    if  FAS_MoveStop(nBdIDAngular) != FMM_OK:
        print("cancel failed")
        return False
    return True



def main():

    nBdIDPosition = 0
    ipPosition = [192,168,0,3]
    nBdIDAngular = 1
    ipAngular = [192,168,0,2]

    positionMotorInitialLocation = 268000
    angularMotorInitialJointingSpeed = 2000

    currentTime = 0
    dt = 0.1
    currentPositions = []
    targetPositions = []
    times = []

    if not checkConnection(nBdIDPosition=nBdIDPosition,ipPosition=ipPosition,nBdIDAngular=nBdIDAngular,ipAngular=ipAngular, ):
        input("motor/driver connection check failed")
        exitProcess(nBdIDPosition,nBdIDAngular)

    if not initializePositionMotor(nBdIDPosition=nBdIDPosition):
        input("position motor initialization failed.")
        exitProcess(nBdIDPosition,nBdIDAngular)

    if not initialJointing(nBdIDPosition=nBdIDPosition,
                           nBdIDAngular=nBdIDAngular,
                            positionMotorInitialLocation= positionMotorInitialLocation,
                            angularMotorInitialJointingSpeed= angularMotorInitialJointingSpeed):
        input("initialJointing failed")
        exitProcess(nBdIDPosition,nBdIDAngular)
    # time.sleep(5)


    


        

    # Move AxisAbsPos & PositionAbsOverride
    
    # for i in range(0,20):

    #     targetAbsPos = round(calculateTargetAbsPositionAtTime(t=currentTime))

    #     if not updateAbsPos(nBdIDPosition,targetAbsPos=targetAbsPos):
    #         input("updated failed: Press Enter to exit...")
    #         exit(1)
    #     times.append(currentTime)
    #     currentPosition = getCurrentPosition(nBdIDPosition)
    #     currentPositions.append(currentPosition)
    #     targetPositions.append(targetAbsPos)

    #     currentTime += dt
    #     time.sleep(dt)

    # Connection Close
    print("fas close called")
    SetServoOff(nBdIDPosition)
    SetServoOff(nBdIDAngular)
    FAS_Close(nBdIDPosition)
    FAS_Close(nBdIDAngular)
    plotChart(times,targetPositions,currentPositions)


    input("Press Enter to exit...")


if __name__ == "__main__":
    main()

