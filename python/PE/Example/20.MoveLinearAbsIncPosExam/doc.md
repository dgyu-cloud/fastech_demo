# MoveLinearAbsIncPosExam

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
4. Operate the motor with Linear interpolation move (incremental position).
5. Operate the motor with Linear interpolation move (absolute position).
6. Close connection.

[KR]  
1. 장치 연결.
2. 드라이브 에러 체크.
3. Servo Enable.
4. 직선 보간 이송 (상대 좌표).
5. 직선 보간 이송 (절대 좌표).
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
    print("[nBdID : %d ] Function(FAS_GetAxisStatus) was failed." % nBdID)
    return False

if axis_status & EZISERVO2_AXISSTATUS.FFLAG_ERRORALL:
    # if Drive's Error was detected, Reset the ServoAlarm
    if FAS_ServoAlarmReset(nBdID) != FMM_OK:
        print("[nBdID : %d ] Function(FAS_ServoAlarmReset) was failed." % nBdID)
        return False

return True
```
[EN]  
You can check the current drive's operating status using the FAS_GetAxisStatus() function. You can reset the current drive's alarm status using the FAS_ServoAlarmReset() function.

[KR]  
FAS_GetAxisStatus() 함수를 사용하여 현재 드라이브의 운전 상태를 확인 할 수 있습니다. FAS_ServoAlarmReset() 함수를 사용하여 현재 드라이브의 알람상태를 리셋 할 수 있습니다.

### 2.1 Axis status
[EN]  
EZISERVO2_AXISSTATUS is a structure that organizes drive status values.
It can be checked in the define file (MOTION_EziSERVO2_DEFINE.py).

[KR]  
EZISERVO2_AXISSTATUS 는 드라이브 상태값이 정리된 구조체이며 define파일 (MOTION_EziSERVO2_DEFINE.py)에서 확인하실 수 있습니다.

## 3. Linear interpolation move (relative coordinates).
```python
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
```
[EN]  
You can perform incremental position linear interpolation movement using the FAS_MoveLinearIncPos2() function.
Meaning of each argument in the function is as follows sequentially:
'Number of drives to linearly interpolate', 'ID array of drives', 'Coordinate array', 'Speed', 'Acceleration/deceleration time'

[KR]  
FAS_MoveLinearIncPos2() 함수를 사용하여 상대 좌표 직선 보간 이송을 수행할 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'직선 보간할 드라이브의 수', '드라이브들의 ID배열', '좌표 배열', '속도', '가감속 시간'

## 4. Linear interpolation move (absolute coordinates).
```python
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
```
[EN]  
You can perform absolute position linear interpolation using the FAS_MoveLinearIncPos2() function. 
It has same argument as 'Incremental position linear interpolation'.

[KR]  
FAS_MoveLinearIncPos2() 함수를 사용하여 절대 좌표 직선 보간 이송을 수행할 수 있습니다.
해당 함수의 각 인자는 '상대 좌표 직선 보간 이송'과 동일합니다.

## 5. Etc
[EN]  
1. For function descriptions on device connection and disconnection, please refer to the [01.ConnectionExam] project document. 
2. For function descriptions on driver error check, please refer to the [05.JogMovementExam] project document.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.
2. 드라이버 에러 체크에 대한 함수 설명은 [05.JogMovementExam] 프로젝트 문서를 참고하시기 바랍니다.