# SetCounterTriggerExam

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
4. Configure Count Command
5. Configure Count Trigger
6. Operate the motor with incremental position
7. Close connection.

[KR]  
1. 장치 연결.
2. 드라이브 에러 체크.
3. Servo Enable.
4. Count Command Setting
5. Count Trigger Setting
6. 상대 위치 이동
7. 연결 해제.

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

## 4. Set Counter Command
```python
byChannel = 0

# Set Counter Enable
if FAS_CounterCommand(nBdID2, byChannel, CNTCMD_CH_ENABLE, 1) != FMM_OK:
    print("Function(FAS_CounterCommand) was failed.")
    return False
else:
    print("FAS_CounterCommand Success!")

# Reset Counter
if FAS_CounterCommand(nBdID2, byChannel, CNTCMD_RESET_ALL, 0) != FMM_OK:
    print("Function(FAS_CounterCommand) was failed.")
    return False
else:
    print("FAS_CounterCommand Success!")
```
[EN]  
You can set the Counter Command using the FAS_CounterCommand() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'Channel number', 'Counter Command Type', 'Value to modify'
In this example, the Counter Enable and Counter Value of Ch1 are initialized.

[KR]  
FAS_CounterCommand() 함수를 사용하여 Counter Command를 설정할 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', '채널 번호', 'Counter Command Type', '수정할 값'
해당 예제에서는 Ch1의 Counter Enable 및 Counter Value를 초기화합니다.

### 4.1 Counter Command Type
[EN]  
COUNTER_CMD(CNTCMD_CH_ENABLE, CNTCMD_RESET_ALL) is a structure that organizes Counter Command Types.
It can be checked in the define file (MOTION_DEFINE.py).

[KR]  
COUNTER_CMD(CNTCMD_CH_ENABLE, CNTCMD_RESET_ALL)는 Counter Command Type이 정리된 구조체이며 define파일 (MOTION_DEFINE.py)에서 확인하실 수 있습니다.

## 5. Counter Trigger Setting
```python
byChannel = 0
bStartTrigger = True
lStartPos = 50000
dwPeriod = 50000
dwPulseTime = 500
dwTriggerCount = 10

# Set Counter Trigger
if (
    FAS_SetCounterTrigger(
        nBdID2,
        byChannel,
        bStartTrigger,
        lStartPos,
        dwPeriod,
        dwPulseTime,
        dwTriggerCount,
    )
    != FMM_OK
):
    print("Function(FAS_SetCounterTrigger) was failed.")
    return False
```
[EN]  
You can set the Counter Trigger using the FAS_SetCounterTrigger() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'Channel number', 'Whether Trigger is Off/On', 'Trigger initial starting position', 'Trigger operation cycle', 'Trigger On Time', 'Trigger operation count'

[KR]  
FAS_SetCounterTrigger() 함수를 사용하여 Counter Trigger를 설정할 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', '채널 번호', 'Trigger Off/On 여부', 'Trigger 최초 시작 위치', 'Trigger 동작 주기', 'Trigger On Time', 'Trigger 동작 회수'

## 6. Move increase position
```python
lIncPos = 500000
lVelocity = 30000

if FAS_MoveSingleAxisIncPos(nBdID, lIncPos, lVelocity) != FMM_OK:
    print("Function(FAS_MoveSingleAxisIncPos) was failed.")
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
```
[EN]  
You can use the FAS_MoveSingleAxisIncPos() function to operate the motor with [incremental position, speed].

[KR]  
FAS_MoveSingleAxisIncPos() 함수를 사용하여 모터의 [상대 위치, 속도]으로 동작시킬 수 있습니다.

## 7. Etc
[EN]  
1. Please refer to the [01.ConnectionExam] project document for function descriptions on connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.