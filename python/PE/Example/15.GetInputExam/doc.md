# GetInputExam

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
2. Read Input/Latch status.
3. Show Input bit.
4. Close connection.

[KR]  
1. 장치 연결.
2. Input/Latch 상태 읽기.
3. Input bit 출력.
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

## 2. Read Input/Latch status
```python
uInput = 0
uLatch = 0

status_result, uInput, uLatch = FAS_GetInput(nBdID)
if status_result != FMM_OK:
    print("Function(FAS_GetInput) was failed.")
    return False
```
[EN]  
You can read information about the Input bit and Latch using the FAS_GetInput() function.

[KR]  
FAS_GetInput() 함수를 사용하여 Input bit와 Latch에 대한 정보를 읽을 수 있습니다.

## 3. Print input bit
```python
for i in range(16):
    bON = (uInput & (0x01 << i)) != 0
    print("Input bit %d is %s." % (i, "ON" if bON else "OFF"))
```
[EN]  
Show input bits 0 to 15 using the data stored in uInput.

[KR]  
uInput에 저장된 데이터를 통하여 0~15번의 Input bit를 출력합니다.

### 3.1 Input/Latch logic
[EN]  
From the LSB to the MSB of uInput(32bit), Input bit 0~31 will be written sequentially.
From the LSB to the MSB of uLatch(32bit), Latch 0~31 will be written sequentially.

[KR]  
uInput(32bit)의 LSB에 0번 Input bit부터 MSB에 31번 Input bit가 순차적으로 쓰여집니다.
uLatch(32bit)의 LSB에 0번 Latch부터 MSB에 31번 Latch가 순차적으로 쓰여집니다.

## 4. Etc
[EN]  
1. Please refer to the [01.ConnectionExam] project document for function descriptions on connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.