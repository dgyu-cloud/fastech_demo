# ConfigDACExam

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
2. Configure DAC config.
3. Read DAC config.
4. Close connection.

[KR]  
1. 장치 연결.
2. DAC 파라미터 설정.
3. DAC 파라미터 읽기.
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

## 2. Set DAC config
```python
byChannel = 0  # Channel = 0
lDACRange = 0  # AD Range = 0
lCalbrationHigh = 24000  # Calibration High = 24000
lCalbrationLow = -1000  # Calibration Low = -1000

print("---------------------------------- ")
# Set DAC Range to 0 (0 ~ 5[V])
status_result, recv_result = FAS_SetDACConfig(
    nBdID, byChannel, DAC_RANGE, lDACRange
)
if status_result != FMM_OK:
    print("Function(FAS_SetDACConfig) was failed.")

# Set DAC Calibration High to 24000
status_result, recv_result = FAS_SetDACConfig(
    nBdID, byChannel, DAC_CALIBRATION_HIGH, lCalbrationHigh
)
if status_result != FMM_OK:
    print("Function(FAS_SetDACConfig) was failed.")

# Set DAC Calibration Low to -1000
status_result, recv_result = FAS_SetDACConfig(
    nBdID, byChannel, DAC_CALIBRATION_LOW, lCalbrationLow
)
if status_result != FMM_OK:
    print("Function(FAS_SetDACConfig) was failed.")
```
[EN]  
You can set DAC related parameters using the FAS_SetDACConfig() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'channel number', 'parameter type', 'parameter value'
And Meaning of each return value is as follows sequentially:
'return code', 'value applied to parameter'

[KR]  
FAS_SetDACConfig() 함수를 사용하여 DAC 관련 파라미터를 설정할 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', '채널 번호', '파라미터 타입', '파라미터 값'
그리고, 해당 함수의 반환값은 순차적으로 다음을 의미합니다.
'함수 리턴코드', '파라미터에 적용된 값'

### 2.1 DAC_CONFIG
[EN]  
DAC_CONFIG is an enum data type declared to identify DAC parameters.
Meaning of each data type is as follows:

DAC_RANGE: DAC output range
DAC_CALIBRATION_HIGH: High Calibration Value
DAC_CALIBRATION_LOW: Low Calibration Value

DAC_CONFIG can be found in the define file (MOTION_DEFINE.py).

[KR]  
DAC_CONFIG은 DAC 파라미터를 식별하기 위해 선언된 enum 자료형입니다.
각 Type은 다음을 의미합니다.

DAC_RANGE: DAC 출력 범위
DAC_CALIBRATION_HIGH: High Calibration Value
DAC_CALIBRATION_LOW: Low Calibration Value

DAC_CONFIG은 define파일 (MOTION_DEFINE.py)에서 확인하실 수 있습니다.

## 3. Get DAC config
```python
byChannel = 0  # Channel 0

print("---------------------------------- ")
# Get DAC Range
status_result, data = FAS_GetDACConfig(nBdID, byChannel, DAC_RANGE)
if status_result != FMM_OK:
    print("Function(FAS_GetDACConfig) was failed.")

# Get DAC Calibration High
status_result, data = FAS_GetDACConfig(nBdID, byChannel, DAC_CALIBRATION_HIGH)
if status_result != FMM_OK:
    print("Function(FAS_GetDACConfig) was failed.")

# Get DAC Calibration Low
status_result, data = FAS_GetDACConfig(nBdID, byChannel, DAC_CALIBRATION_LOW)
if status_result != FMM_OK:
    print("Function(FAS_GetDACConfig) was failed.")
```
[EN]  
You can read DAC related parameters using the FAS_GetDACConfig() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'channel number', 'parameter type'
And Meaning of each return value is as follows sequentially:
'return code', 'stored parameter value'

[KR]  
FAS_GetDACConfig() 함수를 사용하여 DAC 관련 파라미터를 읽어올 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', '채널 번호', '파라미터 타입'
그리고, 해당 함수의 반환값은 순차적으로 다음을 의미합니다.
'함수 리턴코드', '저장된 파라미터 값'

## 4. Etc
[EN]  
1. Please refer to the [01.ConnectionExam] project document for function descriptions on connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.