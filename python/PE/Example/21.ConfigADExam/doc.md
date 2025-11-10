# ConfigADExam

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
2. Configure AD parameters.
3. Read AD parameters.
4. Close connection.

[KR]  
1. 장치 연결.
2. AD 파라미터 설정.
3. AD 파라미터 읽기.
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

## 2. Set AD Parameter
```python
byChannel = 0  # Channel = 0
lADRange = 0  # AD Range = 0
lFilterLen = 1000  # Filter Length = 1000
lFilterOffset = -1000  # Filter Offset = -1000

print("---------------------------------- ")
# Set AD Range to 0 (-10 ~ 10[V])
status_result, recv_status = FAS_SetADConfig(
    nBdID, byChannel, TYPE_AD_RANGE, lADRange
)
if status_result != FMM_OK:
    print("Function(FAS_SetADConfig) was failed.")

# Set Filter Length to 1000
status_result, recv_status = FAS_SetADConfig(
    nBdID, byChannel, TYPE_AD_FILTER_LENGTH, lFilterLen
)
if status_result != FMM_OK:
    print("Function(FAS_SetADConfig) was failed.")

# Set Filter Offset to -1000
status_result, recv_status = FAS_SetADConfig(
    nBdID, byChannel, TYPE_AD_FILTER_OFFSET, lFilterOffset
)
if status_result != FMM_OK:
    print("Function(FAS_SetADConfig) was failed")
```
[EN]  
You can change AD configurations using the FAS_SetADConfig() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'channel number', 'parameter type', 'parameter value'
And Meaning of each return value is as follows sequentially:
'return code', 'value applied to parameter'

[KR]  
FAS_SetADConfig() 함수를 사용하여 AD 관련 설정을 변경할 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', '채널 번호', '파라미터 타입', '파라미터 값'
그리고, 해당 함수의 반환값은 순차적으로 다음을 의미합니다.
'함수 리턴코드', '파라미터에 적용된 값'

### 2.1 AD_DATA_TYPE
[EN]  
AD_DATA_TYPE is an enum data type declared to identify AD parameters. 
Meaning of each data type is as follows:

TYPE_AD_RANGE : Analog Input Range
TYPE_AD_FILTER_LENGTH : Filter Length
TYPE_AD_FILTER_OFFSET : AD Conversion Offset

You can check AD_DATA_TYPE in the define file (MOTION_DEFINE.py).

[KR]  
AD_DATA_TYPE은 AD 파라미터를 식별하기 위해 선언된 enum 자료형입니다.
각 Type은 다음을 의미합니다.

TYPE_AD_RANGE: 아날로그 입력 범위
TYPE_AD_FILTER_LENGTH: Filter 길이
TYPE_AD_FILTER_OFFSET: AD 변환 Offset

AD_DATA_TYPE은 define파일 (MOTION_DEFINE.py)에서 확인하실 수 있습니다.

## 3. Read AD parameter
```python
byChannel = 0  # Channel 0

print("---------------------------------- ")
# Get AD Range
status_result, value = FAS_GetADConfig(nBdID, byChannel, TYPE_AD_RANGE)
if status_result != FMM_OK:
    print("Function(FAS_GetADConfig) was failed.")

# Get Filter Length
status_result, value = FAS_GetADConfig(nBdID, byChannel, TYPE_AD_FILTER_LENGTH)
if status_result != FMM_OK:
    print("Function(FAS_GetADConfig) was failed.")

# Get Filter Length
status_result, value = FAS_GetADConfig(nBdID, byChannel, TYPE_AD_FILTER_OFFSET)
if status_result != FMM_OK:
    print("Function(FAS_GetADConfig) was failed.")
```
[EN]  
You can read AD configurations using the FAS_GetADConfig() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'channel number', 'parameter type'
And Meaning of each return value is as follows sequentially:
'return code', 'stored parameter value'

[KR]  
FAS_GetADConfig() 함수를 사용하여 AD 관련 설정을 읽어올 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', '채널 번호', '파라미터 타입'
그리고, 해당 함수의 반환값은 순차적으로 다음을 의미합니다.
'함수 리턴코드', '저장된 파라미터 값'
 

## 4. Etc
[EN]  
1. Please refer to the [01.ConnectionExam] project document for function descriptions on connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.