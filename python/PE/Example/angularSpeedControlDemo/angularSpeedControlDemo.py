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

MTSPEED = 100000

def Connect(nCommType: int, nBdID: int) -> bool:
    byIP = [192, 168, 0, 3]  # IP: 192.168.0.2
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


def calculateTargetAngSpeedAtTime(t:float) -> float:

    # max_pos = 200000
    match t:
        case _ if t < 2.5:
            angSpeed = 80000 * t
        case _ if 2.5 <= t < 5:
            angSpeed = -40000*t + 300000
        case _ if 5<=t<7.5:
            angSpeed = 40000*t - 100000
        case _ if 7.5<=t<10:
            angSpeed = -80000 * t +800000
        case _ :
            angSpeed = 0
    return angSpeed
def getCurrentAngSpeed(nBdID: int) -> int:
    status, lActualVel = FAS_GetActualVel(nBdID)
    return lActualVel

def plotChart(times,targetAngSpeeds,currentAngSpeeds):
    plt.figure(figsize=(8,4))
    plt.plot(times, currentAngSpeeds, label='Current AngSpeed')
    plt.plot(times, targetAngSpeeds, label='Target AngSpeed', linestyle='--')
    plt.xlabel('Time [s]')
    plt.ylabel('AngSpeed')
    plt.title('AngSpeed Tracking')
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig("plot_ang_speeds.png")
    

def main():
    nBdID = 0

    dt = 0.1
    currentTime = dt
    currentAngSpeeds = []
    targetAngSpeeds = []
    times = []

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


    # Move AxisAbsPos & PositionAbsOverride
    if FAS_MoveVelocity(nBdID,MTSPEED,CCW) != FMM_OK:
        print("move vel error")
        input("Press Enter to exit...")
        exit(1)
    for i in range(0,100):
        print(f"currentTime:{currentTime}")

        targetAngSpeed = round(calculateTargetAngSpeedAtTime(t=currentTime))
        print(f"targetAngSpeed:{targetAngSpeed}")
        if FAS_VelocityOverride(nBdID,targetAngSpeed) != FMM_OK:
            input("vel override failed")
            exit(1)

        # if not updateAbsPos(nBdID,targetAbsPos=targetAbsPos):
        #     input("updated failed: Press Enter to exit...")
        #     exit(1)
        times.append(currentTime)
        currentAngSpeed = getCurrentAngSpeed(nBdID)
        currentAngSpeeds.append(currentAngSpeed)
        targetAngSpeeds.append(targetAngSpeed)

        currentTime += dt
        time.sleep(dt)
    if  FAS_MoveStop(nBdID) != FMM_OK:
        print("cancel failed")
        input("Press Enter to exit...")
        exit(1)
    # Connection Close
    print("fas close called")
    FAS_Close(nBdID)
    plotChart(times,targetAngSpeeds,currentAngSpeeds)


    input("Press Enter to exit...")


if __name__ == "__main__":
    main()

