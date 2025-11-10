# OutputPinControlExam

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
2. Configure output pin setting.
3. Check the output pin setting.
4. Control the output signals (ON / OFF) for a certain period of time (1 minute).
5. Close connection.

[KR]  
1. 장치 연결.
2. Output PIN 설정.
3. Output PIN 설정 확인.
4. 일정 시간(1분) 동안 출력PIN 제어(ON / OFF).
5. 연결 해제.

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

## 2. Check IO Map
```python
# Check OutputPin Status
for i in range(OUTPUTPIN):
    status_result, dwLogicMask, byLevel = FAS_GetIOAssignMap(nBdID, INPUTPIN + i)
    if status_result != FMM_OK:
        print("Function(FAS_GetIOAssignMap) was failed.")
        return False

    if dwLogicMask != IN_LOGIC_NONE:
            print(
                "Output Pin[%d] : Logic Mask 0x%08x (%s)" 
                % (i, dwLogicMask, "Low Active" if byLevel == LEVEL_LOW_ACTIVE else "High Active")
            )
        else:
            print("Output Pin[%d] : Not Assigned" % i)
```
[EN]  
You can use the FAS_GetIOAssignMap() function to check the function and operation level status values ​​for a specific pin of the drive's I/O connector (CN1).

[KR]  
FAS_GetIOAssignMap() 함수를 사용하여 드라이브의 I/O 커넥터(CN1)의 특정 핀에 대한 기능 및 동작 Level 상태값을 확인 할 수 있습니다.

### 2.1 Check logic value
[EN]  
Please check the define file (MOTION_DEFINE.py) for the definition of comparison data to check the validity of the Logic value of a specific pin.

[KR]  
특정 핀의 Logic값 유효성을 확인할 비교 데이터는 define파일(MOTION_DEFINE.py)에 정의되어 있습니다.

## 3.Output PIN Control
```python
# Set Output pin Value.
byPinNo = 3
byLevel = LEVEL_HIGH_ACTIVE
dwOutputMask = SERVO2_OUT_BITMASK_USEROUT0

if FAS_SetIOAssignMap(nBdID, INPUTPIN + byPinNo, dwOutputMask, byLevel) != FMM_OK:
    print("Function(FAS_SetIOAssignMap) was failed.")
    return False
```
[EN]  
You can use the FAS_SetIOAssignMap() function to set the Logic value and operation Level value for a specific pin of CN1.

[KR]  
FAS_SetIOAssignMap()함수를 사용하여 CN1의 특정핀에 대한 Logic값 및 동작 Level 값을 설정 할 수 있습니다.

### 3.1 Check Bit Mask value

[EN]  
The BIT MASK value for the output PIN can be found in the define file (MOTION_EziSERVO2_DEFINE.py).

[KR]  
출력 PIN에 매칭될 BIT MASK값은 define파일(MOTION_EziSERVO2_DEFINE.py)에서 확인하실 수 있습니다.

## 4.Output Pin control
```python
dwOutputMask = SERVO2_OUT_BITMASK_USEROUT0

# Control output signal on and off for 60 seconds
for i in range(30):
    time.sleep(1)
    # USEROUT0: ON
    if FAS_SetIOOutput(nBdID, dwOutputMask, 0) != FMM_OK:
        print("Function(FAS_SetIOOutput) was failed.")
        return False

    time.sleep(1)
    # USEROUT0: OFF
    if FAS_SetIOOutput(nBdID, 0, dwOutputMask) != FMM_OK:
        print("Function(FAS_SetIOOutput) was failed.")
        return False

print("finish WaitSecond!")
```
[EN]  
You can control (Set & Clear) the output status of a specific pin using the FAS_SetIOOutput() function.

[KR]  
FAS_SetIOOutput() 함수를 사용하여 특정 핀의 출력 상태값을 제어(Set & Clear)할 수 있습니다.

## 5. Etc
[EN]  
1. Please refer to the ConnectionExam project documentation for a description of the functions related to connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 관한 기능 설명은 ConnectionExam 프로젝트 문서를 참고하시기 바랍니다.