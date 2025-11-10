# InputPinControlExam 

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
2. Configure input pin setting.
3. Monitor the input pin signals for a minute.
4. Close connection.

[KR]  
1. 장치 연결.
2. Input Pin 설정.
3. 일정 시간(1분) 동안 입력핀 신호 감시.
4. 연결 해제.

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

## 2. Input Pin setting
```python
# Set Input pin Value.
byPinNo = 3
byLevel = LEVEL_LOW_ACTIVE
dwInputMask = SERVO2_IN_BITMASK_USERIN0

if FAS_SetIOAssignMap(nBdID, byPinNo, dwInputMask, byLevel) != FMM_OK:
    print("Function(FAS_SetIOAssignMap) was failed.")
    return False
```
### ※ Function detail
[EN]  
> FAS_SetIOAssignMap(iBdID: int, iIOPinNo: int, dwIOLogicMask: int, bLevel: int):
> - iBdID: Board ID number set in the 'FAS_Connect' function.
> - iIOPinNo: I/O Pin number to read.
> - dwIOLogicMask: Logic Mask value to assign to the corresponding pin.
> - bLevel: Active Level value to set for the corresponding pin.

The source code above uses the 'FAS_SetIOAssignMap()' function to set the Logic Mask (SERVO2_IN_Bitmask_PJOG) and operation signal Level value for pin 3.
Accordingly, if a signal is input to pin 3, the motor will perform a Positive JOG Move operation. 
As above, the Logic Mask signal uses the Bit Mask value defined for various motor operations [Origin / Limit- / Limit+ / PT Start, etc.], and can be checked in the model's define file ('MOTION_EziSERVO2_DEFINE.py' for Ezi-SERVOII Plus-E).
Therefore, the 'FAS_SetIOAssignMap()' function assigns the meaning of the corresponding signal by matching the Logic Mask and operation signal level value to the input/output pins, and the user can perform the desired motor operation through the input/output signals to the corresponding pins.
In addition, when the 'FAS_SetIOAssignMap()' function is used, the Logic Mask value of the corresponding pin is stored in RAM.

[KR]  
> FAS_SetIOAssignMap(iBdID: int, iIOPinNo: int, dwIOLogicMask: int, bLevel: int):
> - iBdID : 'FAS_Connect' 함수에서 설정한 Board ID 번호.
> - iIOPinNo : 읽어올 I/O Pin 번호.
> - dwIOLogicMask : 해당 핀에 할당할 Logic Mask 값.
> - bLevel : 해당 핀에 설정할 Active Level 값.

위 소스코드는 'FAS_SetIOAssignMap()' 함수를 사용하여 3번 핀에 Logic Mask(SERVO2_IN_Bitmask_PJOG) 및 동작 신호 Level 값을 설정합니다.
그에 따라 3번 핀으로 신호가 입력된다면 모터는 Positive JOG Move 동작을 실시하게 됩니다.
위와같이 Logic Mask 신호는 [Origin / Limit- / Limit+ / PT Start 등..]모터의 다양한 동작을 위해 정의된 Bit Mask 값이 사용되며, 모델의 define 파일(Ezi-SERVOII Plus-E의 경우 'MOTION_EziSERVO2_DEFINE.py')에서 확인하실 수 있습니다.
따라서 'FAS_SetIOAssignMap()' 함수는 입출력핀에 Logic Mask 및 동작 신호 Level 값의 매칭을 통하여 해당 신호의 의미를 부여하게 되며, 의미가 부여된 핀에 입출력 신호를 통하여 사용자가 원하는 모터 동작을 진행할 수 있습니다.
더하여, 'FAS_SetIOAssignMap()' 함수 사용시 해당 핀에 매칭되는 Logic Mask값은 RAM에 저장되게 됩니다.

## 3. Check IO Map
```python
# Show Input pins status
for i in range(INPUTPIN):
    status_result, dwLogicMask, byLevel = FAS_GetIOAssignMap(nBdID, i)
    if status_result != FMM_OK:
        print("Function(FAS_GetIOAssignMap) was failed.")
        return False

    if dwLogicMask != IN_LOGIC_NONE:
            print(
                "Input PIN[%d] : Logic Mask 0x%08x (%s)" 
                % (i, dwLogicMask, "Low Active" if byLevel == LEVEL_LOW_ACTIVE else "High Active")
            )
        else:
            print("Input Pin[%d] : Not Assigned" % i)
```
### ※ Function detail
[EN]  
> FAS_GetIOAssignMap(iBdID: int, iIOPinNo: int) -> tuple[result, dwIOLogicMask, bLevel]:
> - iBdID: Board ID number set in the FAS_Connect function.
> - iIOPinNo: I/O Pin number to read.
> - result: Return_Code of function.
> - dwIOLogicMask: Logic Mask assigned to the corresponding Pin.
> - bLevel: Active Level assigned to the corresponding Pin.

The source code above use the FAS_GetIOAssignMap() function to read the Logic Mask (Bit Mask) and Level values ​​for each pin set by the FAS_SetIOAssignMap() function.
The Logic Mask and Level values ​​of each pin are printed on the screen.

[KR]  
> FAS_GetIOAssignMap(iBdID: int, iIOPinNo: int) -> tuple[result, dwIOLogicMask, bLevel]:
> - iBdID : FAS_Connect 함수에서 설정한 Board ID 번호.
> - iIOPinNo : 읽어올 I/O Pin 번호.
> - result : 함수의 Return_Code.
> - dwIOLogicMask : 해당 Pin에 할당된 Logic Mask값.
> - bLevel : 해당 핀의 Active Level 값.

위 소스코드는 FAS_SetIOAssignMap() 함수를 통하여 설정한 각 핀에 대한 Logic Mask (Bit Mask) 및 Level 값을 FAS_GetIOAssignMap() 함수를 통하여 읽어들입니다.
읽어들인 각 핀의 Logic Mask 및 Level 값을 화면에 출력합니다.


## 4. Check Input Pin
```python
dwInputMask = SERVO2_IN_BITMASK_USERIN0

print(
        "-----------------------------------------------------------------------------"
    )

# When the value SERVO2_IN_BITMASK_USERIN0 is entered with the set PinNo, an input confirmation message is displyed.
# Monitoring input signal for 60 seconds
for i in range(600):
    status_result, dwInput = FAS_GetIOInput(nBdID)
    if status_result == FMM_OK:
        if dwInput & dwInputMask:
            print("INPUT PIN DETECTED.")
    else:
        print("Function(FAS_GetIOInput) was failed.")
        return False
    time.sleep(0.1)
print("finish WaitSecond!")
return True
```
[EN]  
The above source code checks the status of all pins using the FAS_GetIOInput() function for 1 minute.
Also, it compares the Logic Mask (Bit Mask) value for Positive Jog and if the input of the corresponding bit is confirmed, the phrase "INPUT PIN DETECTED" is displayed on the screen.

[KR]  
위 소스코드는 1분동안 FAS_GetIOInput() 함수를 사용하여 핀 전체의 상태값을 확인합니다.
특히 Positive Jog에 대한 Logic Mask(Bit Mask)값을 비교하여 해당 비트의 입력이 확인된다면 "INPUT PIN DETECTED" 문구를 화면해 현시합니다.

### ※ Function detail
[EN]  
> FAS_GetIOInput(iBdID: int) -> tuple[result, dwIOInput]:
> - iBdID: Board ID number set in the FAS_Connect function.
> - result: Return_Code of function.
> - dwIOInput: Pointer variable where the input value will be stored.

[KR]  
> FAS_GetIOInput(iBdID: int) -> tuple[result, dwIOInput]:
> - iBdID : FAS_Connect 함수에서 설정한 Board ID 번호.
> - result : 함수의 Return_Code.
> - dwIOInput : Input 값이 저장될 포인터 변수.

## 5. Etc
[EN]  
1. Please refer to the ConnectionExam project documentation for functional descriptions of device connection and disconnection.

[KR]  
1. 장치 연결 및 해제에 대한 기능 설명은 ConnectionExam 프로젝트 문서를 참고하시기 바랍니다.