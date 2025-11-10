# PushStopExam

Notification before use
-------------------------------------------------------
Depending on the type of product you are using, the definitions of 'Parameter', 'IO Logic', 'AxisStatus', etc. may be different.
This example is based on 'Ezi-SERVO2', so please apply the appropriate value depending on the product you are using.

```
Example)

FM_EZISERVO2_PARAM			// Parameter enum when using 'Ezi-SERVO2'
FM_EZIMOTIONLINK2_PARAM		// Parameter enum when using 'Ezi-MOTIONLINK2'
```
[EN]    
This example code is implemented to run on Python 3.x and later.
If you use version 3.0 or less, you need to change the print and input functions.

[KR]  
이 예제코드는 파이썬 3.x이상에서 동작하도록 구현되어있습니다.
3.0이하 버전에서 사용하실경우 print, input함수의 변형이 필요합니다.

## 0. Program scenario
[EN]  
1. Connect a device.
2. Check the drive error.
3. Enable Servo.
4. Operate the motor with Push Mode (Stop Mode).
5. Operate the motor with the return operation.
6. Connection close.

[KR]  
1. 장치 연결.
2. 드라이브 에러 체크.
3. Servo Enable.
4. Push Mode(Stop Mode) 운전 실시.
5. 복귀 운전 실시.
6. 연결 해제.

## 1. Setting the Path
```python
import sys
import os
import platform
try:
    include_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
except NameError:
    include_path = os.path.abspath(
        os.path.join(os.getcwd(), "..")
    )

arch = platform.architecture()[0]
if arch == '64bit':
    library_path = os.path.join(include_path, "Include_Python_x64")
else:
    library_path = os.path.join(include_path, "Include_Python")

sys.path.append(library_path)
```
[EN]    
This code adds the appropriate Library folder path according to the Python architecture to import FAS_EziMOTIONPlusE, MOTION_DEFINE, and ReturnCodes_Define modules.
If the Library folder is in a different path, enter that path in Library_path.

[KR]  
FAS_EziMOTIONPlusE, MOTION_DEFINE, ReturnCodes_Define 모듈들을 Import 하기 위하여 파이썬 아키텍쳐에 따라 알맞은 Library 폴더 경로를 추가하는 코드입니다.
Library 폴더가 다른 경로에 있는 경우, library_path에 해당 경로를 입력해 주시기 바랍니다.

## 2. Check drive error
```python
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
```
[EN]  
You can check the current drive's operating status using the FAS_GetAxisStatus() function. You can reset the current drive's alarm status using the FAS_ServoAlarmReset() function.

[KR]  
FAS_GetAxisStatus() 함수를 사용하여 현재 드라이브의 운전 상태를 확인 할 수 있습니다. FAS_ServoAlarmReset() 함수를 사용하여 현재 드라이브의 알람상태를 리셋 할 수 있습니다.

### 2.1 Axis status
[EN]  
EZISERVO2_AXISSTATUS is a structure that organizes drive status values ​​and can be checked in the define file (MOTION_EziSERVO2_DEFINE.py).

[KR]  
EZISERVO2_AXISSTATUS 는 드라이브 상태값이 정리된 구조체이며 define파일 (MOTION_EziSERVO2_DEFINE.py)에서 확인하실 수 있습니다.

## 3. Servo Enable
```python
if FAS_ServoEnable(nBdID, TRUE) != FMM_OK:
    print("Function(FAS_ServoEnable) was failed.")
    return False
```
[EN]  
You can set the Servo Enable signal of the drive using the FAS_ServoEnable() function.

[KR]  
FAS_ServoEnable() 함수를 사용하여 드라이브의 Servo Enable 신호를 설정할 수 있습니다.

## 4. Move push mode
```python
# normal position motion
dwStartSpd = 1
dwMoveSpd = 50000
wAccel = 500
wDecel = 500
lPosition = 500000

# push motion
dwPushSpd = 2000
wPushRate = 50
wPushMode = 0  # Stop Mode Push
lEndPosition = lPosition + 10000

print("---------------------------")

if (
    FAS_MovePush(
        nBdID,
        dwStartSpd,
        dwMoveSpd,
        lPosition,
        wAccel,
        wDecel,
        wPushRate,
        dwPushSpd,
        lEndPosition,
        wPushMode,
    )
    != FMM_OK
):
    print("Function(FAS_MovePush) was failed.")
    return False
```
[EN]  
With FAS_MovePush() function, you can operate the motor to a desired position with a specified force.
For your information, there are two operation parts in 'push mode'.
The first one is position control before applying a specified force, and the second one is the force control with the specified force.
The position control part can set [start speed, maximum speed, acceleration/deceleration time, absolute position].
The force control part can set [push force ratio, push operation speed, push operation absolute position, push operation mode].


[KR]  
FAS_MovePush() 함수를 사용하여 특정 위치에서 지정된 힘을 유지하며 이동할 수 있다.
더하여 PUSH MODE 운전은 힘을 가하기 이전 움직임에 대한 설정 [시작속도, 최대속도, 가감속 시간, 절대 위치]을 할 수 있으며, 
힘을 가하는 운전에 대한 설정 [PUSH 힘 비율, Push 운전 속도, PUSH 운전 절대 위치, PUSH 운전 모드]또한 할 수 있습니다.

## 5. Check IO Output
```python
dwOutPut = 0

status_result, dwOutput = FAS_GetIOOutput(nBdID)

if status_result != FMM_OK:
    print("Function(FAS_GetIOOutput) was failed.")
    return False
else:
    if dwOutput & SERVO2_OUT_BITMASK_PUSHDETECT:
        print("Work Detected!")
    else:
        print("Work Not Detected!")
```
[EN]  
You can check the status of the IO output pin using the FAS_GetIOOutput() function.

[KR]  
FAS_GetIOOutput() 함수를 통하여 IO 출력핀의 상태를 확인 할 수 있습니다.

### 5.1 Output logic
[EN]  
EZISERVO2_OUTLOGIC is a structure that organizes the meaning of IO output status, and when an obstacle is detected in force control mode, the BIT_RESERVED0 signal is output. 
You can check EZISERVO2_OUTLOGIC in the define file (MOTION_EziSERVO2_DEFINE.py).

[KR]  
EZISERVO2_OUTLOGIC는 IO 출력 상태 의미를 정리한 구조체이며, PUSH 운전에서 장애물 감지시 BIT_RESERVED0 신호를 출력하게 됩니다.
EZISERVO2_OUTLOGIC는 define파일(MOTION_EziSERVO2_DEFINE.py)에서 확인하실 수 있습니다.

## 6. Watch drive status
```python
# Check the Axis status until motor stops and the FFLAG_MOTIONING value is released.

while True:
    time.sleep(0.001)
    status_result, axis_status = FAS_GetAxisStatus(nBdID)

    if status_result != FMM_OK:
        print("Function(FAS_GetAxisStatus) was failed.")
        return False

    if not (axis_status & EZISERVO2_AXISSTATUS.FFLAG_MOTIONING):
        break
```
[EN]  
The FAS_GetAxisStatus() function indicates the drive status value.
The user can use it to check the status and wait until a specific status value is confirmed.
In addition, the user can check whether the push mode operation is completed with the values ​​FFLAG_MOTIONING ('0').

[KR]  
드라이브의 운전 상태값을 나타내는 FAS_GetAxisStatus() 함수를 사용하여 사용자가 원하는 특정상태 값이 확인 될 때까지 대기할 수 있습니다.
더하여 PUSH 모드 동작 완료 상태는 FFLAG_MOTIONING ('0')값으로 확인 할 수 있습니다.

## 7. Etc
[EN]  
1. For function descriptions on device connection and disconnection, please refer to the [01.ConnectionExam] project document. 
2. For function descriptions on relative position movement operation, please refer to the [07.MoveAbsIncPosExam] project document.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.
2. 상대 위치 이동 운전에 대한 함수 설명은 [07.MoveAbsIncPosExam] 프로젝트 문서를 참고하시기 바랍니다.
