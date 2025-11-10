# CounterCommandExam

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
2. Read the Counter Command value.
3. Configure the Counter Command.
4. Read the modified Counter Command value.
5. Connection close.

[KR]  
1. 장치 연결.
2. Counter Command 값 읽기.
3. Counter Command 설정.
4. 수정 된 Counter Command 값 읽기.
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

## 2. Set counter command
```python
 byChannel = 0  # Channel = 0

print("----------------------------------")
# Set Counter Command Channel Enable
if FAS_CounterCommand(nBdID, byChannel, CNTCMD_CH_ENABLE, 1) != FMM_OK:
    print("Function(FAS_CounterCommand) was failed.")
```
[EN]  
You can set the Counter Command using the FAS_CounterCommand() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'Channel number', 'Counter Command Type', 'Value to modify'

[KR]  
FAS_CounterCommand() 함수를 사용하여 Counter Command를 설정할 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', '채널 번호', 'Counter Command Type', '수정할 값'

### 2.1 Counter Command Type
[EN]  
COUNTER_CMD(CNTCMD_CH_ENABLE) is a structure that organizes Counter Command Types and can be found in the define file (MOTION_DEFINE.py).

[KR]  
COUNTER_CMD(CNTCMD_CH_ENABLE)는 Counter Command Type이 정리된 구조체이며 define파일 (MOTION_DEFINE.py)에서 확인하실 수 있습니다.

## 3. Get counter command
```python
print("----------------------------------")
# Get Counter Status
status_result, dwStatus = FAS_GetCounterStatus(nBdID)
if status_result != FMM_OK:
    print("Function(FAS_GetCounterStatus) was failed.")
```
[EN]  
You can read the set Counter Command value using the FAS_GetCounterStatus() function.
Meaning of argumnet is 'ID number of the board'
And Meaning of each return value is as follows sequentially:
'return code', 'read value (saved as Bitmask)'

[KR]  
FAS_GetCounterStatus() 함수를 사용하여 설정된 Counter Command 값을 읽어올 수 있습니다.
해당 함수의 인자는 다음을 의미합니다.
'해당 보드의 ID번호'
그리고 해당 함수의 반환값은 순차적으로 다음을 의미합니다.
'함수 리턴코드', '읽어들인 값(Bitmask로 저장됨)'

### 3.1 Counter Command BitMask
[EN]  
The meaning of Counter Command Bitmask is as follows, with the lower 4 bytes indicating Cnt1 and the upper 4 bytes indicating Cnt2.
0x0001: Enabled
0x0002: Latch A Enabled
0x0004: Latch B Enabled
0x0008: Z-Phase Latch Enabled
0x0010: Latch A Latcheds
0x0020: Latch B Latcheds
0x0040: Z-Phase Latch Latcheds
0x0080: Reset
0x0100: Trigger Status
0x0200: Comparison
For more information, please refer to the define file (MOTION_DEFINE.py).

[KR]  
읽어들인 Counter Command Bitmask는 하위 4Byte는 Cnt1, 상위 4Byte는 Cnt2를 표시하며 다음과 같습니다.
0x0001: Enabled
0x0002: Latch A Enabled
0x0004: Latch B Enabled
0x0008: Z-Phase Latch Enabled
0x0010: Latch A Latcheds
0x0020: Latch B Latcheds
0x0040: Z-Phase Latch Latcheds
0x0080: Reset
0x0100: Trigger Status
0x0200: Comparison
자세한 내용은 define파일 (MOTION_DEFINE.py)에서 확인하실 수 있습니다.

## 4. Etc
[EN]  
1. Please refer to the [01.ConnectionExam] project document for function descriptions on connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.