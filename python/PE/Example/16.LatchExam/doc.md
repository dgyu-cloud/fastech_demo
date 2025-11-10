# LatchExam

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
2. Read Input/Latch status for 60 seconds, Read Latch Count of Pin 0.
3. Clear Latch status of Pin 0.
4. Read Input/Latch status.
5. Read total Latch Count.
6. Clear Latch Count of Pin 0.
5. Close connection.

[KR]  
1. 장치 연결.
2. 60초간 Input / Latch 상태 읽기, 0번 Pin의 Latch Count 읽기.
3. 0번 Pin의 Latch 상태 초기화.
4. Input / Latch 상태 읽기.
5. 전체 Latch Count 읽기.
6. 0번 Pin의 Latch Count 초기화.
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

## 2. Read latch Count
```python
cInputNo = 0  # Pin 0

for i in range(600):
    # Latch status
    status_result, uInput, uLatch = FAS_GetInput(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetInput) was failed.")
        return False

    # Latch count
    status_result, nLatchCount = FAS_GetLatchCount(nBdID, cInputNo)
    if status_result != FMM_OK:
        print("Function(FAS_GetLatchCount) was failed.")
        return False

    print(
            "Pin %d is %s and %s (latch count %d)" % (
                cInputNo,
                "ON" if (uInput & (0x01 << cInputNo)) else "OFF",
                "latched" if (uLatch & (0x01 << cInputNo)) else "not latched",
                nLatchCount
            )
        )
    time.sleep(0.1)
```
[EN]  
You can read the Latch Count of a specific pin using the FAS_GetLatchCount() function. 
The above source code repeats 'Read Input / Latch Status' and 'Read Latch Count' for 60 seconds.

[KR]  
FAS_GetLatchCount() 함수를 사용하여 특정 핀의 Latch Count를 읽을 수 있습니다.
위 소스 코드는 60초간 'Input / Latch 상태 읽기'와 'Latch Count 읽기'를 반복합니다.

### 2.1 Read Input/Latch status
[EN]  
You can read information about the Input bit and Latch using the FAS_GetInput() function. 
For more information, please refer to the [15.GetInputExam] project document.

[KR]  
FAS_GetInput() 함수를 사용하여 Input bit와 Latch에 대한 정보를 읽을 수 있습니다.
자세한 내용은 [15.GetInputExam] 프로젝트 문서를 참고하시기 바랍니다.

## 3. Clear latch
```python
# Clear the specific pin's Latch status
uLatchMask = 0x01 << cInputNo
if FAS_ClearLatch(nBdID, uLatchMask) != FMM_OK:
    print("Function(FAS_ClearLatch) was failed.")
    return False
```
[EN]  
You can clear the latch state using the FAS_ClearLatch() function.

[KR]  
FAS_ClearLatch() 함수를 사용하여 Latch 상태를 초기화 할 수 있습니다.

### 3.1 Send data logic
[EN]  
The request for Latch state 0 is sequentially written to the LSB of uLatchMask (32 bits) and the request for Latch state 31 is sequentially written to the MSB. 
If the value of each bit is 0, the current state is maintained, and if it is 1, the Latch is cleared.

[KR]  
uLatchMask(32bit)의 LSB에 0번 Latch 상태에 대한 요청부터 MSB에 31번 Latch 상태에 대한 요청이 순차적으로 쓰여집니다.
각 bit의 값이 0인 경우 현재 상태 유지, 1인 경우 Latch를 Clear합니다.

## 4. Read latch count all (16 Input)
```python
cntLatchAll = [0] * 16

# Get latch counts of all inputs (16 inputs)
status_result, cntLatchAll = FAS_GetLatchCountAll(nBdID)
if status_result != FMM_OK:
    print("Function(FAS_GetLatchCountAll) was failed.")
    return False
else:
    for i in range(16):
        print("[fas_get_latch_count_all] Pin[%d] : [%d] count" % (i, cntLatchAll[i]))
```
[EN]  
Use the FAS_GetLatchCountAll() function to read the total Latch Count for 16 Inputs. 
For a request for 32 Inputs, use FAS_GetLatchCountAll32().

[KR]  
FAS_GetLatchCountAll() 함수를 사용하여 16 Input에 대해 전체 Latch Count를 읽습니다.
32 Input에 대한 요청은 FAS_GetLatchCountAll32()를 사용합니다.

## 5. Clear latch count
```python
# Clear the latch count of the specific pin
uLatchMask = 0x01 << cInputNo
if FAS_ClearLatchCount(nBdID, uLatchMask) != FMM_OK:
    print("Function(FAS_ClearLatchCount) was failed.")
    return False
```
[EN]  
Initialize the Latch Count of a specific bit using the FAS_ClearLatchCount() function.

[KR]  
FAS_ClearLatchCount() 함수를 통하여 특정 bit의 Latch Count를 초기화 합니다.

## 6. Etc
[EN]  
1. Please refer to the [01.ConnectionExam] project document for function descriptions on connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.