# JogMovementExExam

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
4. Operate the motor by setting the acceleration/deceleration parameters. (3 seconds)
5. Operate the motor by setting the acceleration/deceleration structure variables. (3 seconds)
6. Close connection.

[KR]  
1. 장치 연결.
2. 드라이브 에러 체크.
3. Servo Enable.
4. 가감속 파라미터 설정을 통한 모터 동작 실시. (3초)
5. 가감속 구조체 변수 설정을 통한 모터 동작 실시. (3초)
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

### 2.1 Axis Status
[EN]  
EZISERVO2_AXISSTATUS is a structure that organizes drive status values.
It can be checked in the define file (MOTION_EziSERVO2_DEFINE.py).

[KR]  
EZISERVO2_AXISSTATUS 는 드라이브 상태값이 정리된 구조체이며 define파일 (MOTION_EziSERVO2_DEFINE.py)에서 확인하실 수 있습니다.

## 3. Servo Enable
```python
if FAS_ServoEnable(nBdID, 1) != FMM_OK:
    print("Function(FAS_ServoEnable) was failed.")
    return False
```
[EN]  
You can set the Servo Enable signal of the drive using the FAS_ServoEnable() function.

[KR]  
FAS_ServoEnable() 함수를 사용하여 드라이브의 Servo Enable 신호를 설정할 수 있습니다.

## 4. Watch drive status
```python
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
```
[EN]  
The FAS_GetAxisStatus() function indicates the drive status value.
The user can use it to check the status and wait until a specific status value is confirmed.

[KR]  
드라이브의 운전 상태값을 나타내는 FAS_GetAxisStatus() 함수를 사용하여 사용자가 원하는 특정상태 값이 확인 될 때까지 대기할 수 있습니다.

## 5. Set parameter value
```python
# Set Jog Acc/Dec Time
if FAS_SetParameter(nBdID, SERVO2_JOGACCDECTIME, nAccDecTime) != FMM_OK:
    print("Function(FAS_SetParameter) was failed.")
    return False
```
[EN]  
You can change parameter values using the FAS_SetParameter function.
The parameter values take effect immediately after they are set.

[KR]  
FAS_SetParameter 함수를 사용하여 파라미터의 값을 변경할 수 있습니다.
파라미터의 값은 설정하는 즉시 적용됩니다.

### 5.1 Setting jog parameter
[EN]  
SERVO2_JOGACCDECTIME is the parameter number for Jog operation.
You can check the parameter number in the corresponding define file (MOTION_SERVO2_DEFINE.py for Ezi-SERVOII Plus-E). 
Or, refer to the number displayed on the Parameter List screen of the Ezi-MOTION Plus-E program.

[KR]  
SERVO2_JOGACCDECTIME는 Jog 운전에 대한 설정 파라미터 번호입니다.
설정하고자 하는 파라미터의 번호는 해당하는 define 파일(Ezi-SERVOII Plus-E의 경우 MOTION_SERVO2_DEFINE.py)에서 확인하실 수 있습니다. 
혹은, Ezi-MOTION Plus-E 프로그램의 Parameter List 화면에 표시되는 번호를 참고하시기 바랍니다.

## 6. Motor motion test1
```python
nTargetVeloc = 10000
nDirect = 1
CW = 0
CCW = 1

if FAS_MoveVelocity(nBdID, nTargetVeloc, nDirect) != FMM_OK:
    print("Function(FAS_MoveVelocity) was failed.")
    return False
```
[EN]  
The FAS_MoveVelocity() function allows the user to operate the motor at the desired [speed, direction].

[KR]  
FAS_MoveVelocity() 함수를 사용하여 사용자가 원하는 모터의 [속도, 방향]으로 동작할 수 있습니다.

## 7. Motor motion test2
```python
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
```
[EN]  
The FAS_MoveVelocityEx() function allows the user to operate the motor at the desired [speed, direction, acceleration].

[KR]  
FAS_MoveVelocityEx() 함수를 사용하여 사용자가 원하는 모터의 [속도, 방향, 가속도]으로 동작할 수 있습니다.

### 7.1 Velocity option

[EN]  
VELOCITY_OPTION_EX is a structure variable that can set the acceleration/deceleration time when the motor is operating.

[KR]  
VELOCITY_OPTION_EX는 모터 동작시 가감속 시간을 설정할 수 있는 구조체 변수입니다.

## 8. Stop Motor
```python
if FAS_MoveStop(nBdID) != FMM_OK:
    print("Function(FAS_MoveStop) was failed.")
    return False
```
[EN]  
You can stop a running motor using the FAS_MoveStop() function.

[KR]  
FAS_MoveStop() 함수를 사용하여 동작중인 모터를 정지 할 수 있습니다.

## 9. Etc

[EN]  
1. For function descriptions on connecting and disconnecting devices, please refer to the [01.ConnectionExam] project document. 
2. For function descriptions on setting parameters, please refer to the [02.ParameterTestExam] project document.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.
2. 파라미터 설정에 대한 함수 설명은 [02.ParameterTestExam] 프로젝트 문서를 참고하시기 바랍니다.
