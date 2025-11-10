# SetCounterConfigExam

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
2. Read the Counter Config value.
3. Configure the Counter Config value.
4. Read the modified Counter Config value.
5. Close connection.

[KR]  
1. 장치 연결.
2. Counter Config 값 읽기.
3. Counter Config 값 설정.
4. 수정 된 Counter Config 값 읽기.
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

## 2. Set Counter Config
```python
byChannel = 0  # Channel = 0

print("----------------------------------")
# Set Counter Input Mode
status_result, recv_status = FAS_SetCounterConfig(
    nBdID, byChannel, CFG_INPUT_MODE, 1
)
if status_result != FMM_OK:
    print("Function(FAS_SetCounterConfig) was failed.")
```
[EN]  
You can set the Counter Config using the FAS_SetCounterConfig() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'Channel number', 'Counter Config Type', 'Value to be modified'
And Meaning of each return value is as follows sequentially:
'return code', 'Modified value'

[KR]  
FAS_SetCounterConfig() 함수를 사용하여 Counter Config를 설정할 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', '채널 번호', 'Counter Config Type', '수정할 값'
그리고 해당 함수의 반환값은 순차적으로 다음을 의미합니다.
'함수 리턴코드', '수정된 값' 

### 2.1 Counter Config Type
[EN]  
COUNTER_CONFIG(CFG_INPUT_MODE) is a structure that organizes Counter Config Type and can be checked in the define file (MOTION_DEFINE.py).

[KR]  
COUNTER_CONFIG(CFG_INPUT_MODE)는 Counter Config Type이 정리된 구조체이며 define파일 (MOTION_DEFINE.py)에서 확인하실 수 있습니다.

## 3. Get Counter Config
```python
byChannel = 0  # Channel = 0

print("----------------------------------")
# Get Counter Input Mode
status_result, data_status = FAS_GetCounterConfig(nBdID, byChannel, CFG_INPUT_MODE)
if status_result != FMM_OK:
    print("Function(FAS_GetCounterConfig) was failed.")
```
[EN]  
You can read the set Counter Config value using the FAS_GetCounterConfig() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'channel number', 'Counter Config Type number to read'
And Meaning of each return value is as follows sequentially:
'return code', 'read value'

[KR]  
FAS_GetCounterConfig() 함수를 사용하여 설정된 Counter Config 값을 읽어올 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', '채널 번호', '읽어들일 Counter Config Type 번호'
그리고 해당 함수의 반환값은 순차적으로 다음을 의미합니다.
'함수 리턴코드', '읽어들인 값' 

## 4. Etc
[EN]  
1. Please refer to the [01.ConnectionExam] project document for function descriptions on connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.
