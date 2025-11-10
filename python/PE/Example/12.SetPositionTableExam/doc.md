# SetPositionTableExam

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
4. Configure and check the position table.
5. Operate the motor with the position table.
6. Close connection.

[KR]  
1. 장치 연결.
2. 드라이브 에러 체크.
3. Servo Enable.
4. 포지션 테이블 설정 및 확인 실시.
5. 포지션 테이블 실행.
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
EZISERVO2_AXISSTATUS is a structure that organizes drive status values.
It can be checked in the define file (MOTION_EziSERVO2_DEFINE.py).

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

## 4. Set position table
```python
# Sets values in the position table.
nodeItem = ITEM_NODE()
wItemNo = 1

# Overwrite part of node's data
nodeItem.dwMoveSpd = 50000
nodeItem.lPosition = 250000
nodeItem.wBranch = 3
nodeItem.wContinuous = 1

# Set node data in Position Table
if FAS_PosTableWriteItem(nBdID, wItemNo, nodeItem):
    print("Function(FAS_PosTableWriteItem) was failed.")
    return False
```
[EN]  
The FAS_PosTableWriteItem() function configures various properties on the indexes in the position table.

[KR]  
FAS_PosTableWriteItem() 함수를 사용하여 포지션 테이블을 구성하는 인덱스에 다양한 속성을 설정할 수 있습니다.

### 4.1 Position table item node
[EN]  
ITEM_NODE is a structure that organizes the attribute values ​​of the indexes in the position table.
It can be checked in the define file (MOTION_DEFINE.py).

[KR]  
ITEM_NODE는 포지션 테이블을 구성하는 인덱스의 속성값이 정리된 구조체이며 define파일(MOTION_DEFINE.py)에서 확인하실 수 있습니다.

## 5. Read position table
```python
nodeItem = ITEM_NODE()
wItemNo = 1

# Gets the data values of that node.
status_result, nodeItem = FAS_PosTableReadItem(nBdID, wItemNo)
if status_result != FMM_OK:
    print("Function(FAS_PosTableReadItem) was failed.")
    return False
```
[EN]  
FAS_PosTableReadItem() function checks the table properties stored at a specific index in the positions table.

[KR]  
FAS_PosTableReadItem() 함수를 사용하여 포지션 테이블내 특정 인덱스에 저장된 테이블 속성을 확인 할 수 있습니다.

## 6. Run position table
```python
wItemNo = 1

if FAS_PosTableRunItem(nBdID, wItemNo) != FMM_OK:
    print("Function(FAS_PosTableRunItem) was failed.")
    return False
```
[EN]  
FAS_PosTableRunItem() function operates the motor according to the specific index in the position table.

[KR]  
FAS_PosTableRunItem() 함수를 사용하여 포지션 테이블내 특정 인덱스의 설정값에 맞게 동작시킬수 있습니다.

## 7. Watch drive status
```python
while True:
    time.sleep(0.001)

    status_result, axis_status = FAS_GetAxisStatus(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetAxisStatus) was failed.")
        return False

    if axis_status & EZISERVO2_AXISSTATUS.FFLAG_PTSTOPPED:
        print("Position Table Run Stop!")
        break
```
[EN]  
The FAS_GetAxisStatus() function indicates the drive status value.
The user can use it to check the status and wait until a specific status value is confirmed.
In addition, the user can check whether the position table operation is completed with the values ​​FFLAG_MOTIONING ('0') and FFLAG_INPOSITION ('1').

[KR]  
드라이브의 운전 상태값을 나타내는 FAS_GetAxisStatus() 함수를 사용하여 사용자가 원하는 특정상태 값이 확인 될 때까지 대기할 수 있습니다.
더하여 포지션 테이블 동작 완료 상태는 FFLAG_ORIGINRETURNING ('0')값으로 확인 할 수 있습니다.

## 8. Etc
[EN]  
1. Please refer to the [01.ConnectionExam] project document for function descriptions on connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.