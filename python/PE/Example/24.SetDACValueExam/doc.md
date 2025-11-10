# SetDACValueExam

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
2. Configure the DAC value.
3. Read the DAC value.
4. Close connection.

[KR]  
1. 장치 연결.
2. DAC 변환 값 설정.
3. DAC 변환 값 읽기.
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

## 2. Set DAC value
```python
byChannel = 0  # Channel = 0
bEnable = True  # Enable = True
lDACValue = 10000  # DAC Value = 10000

print("---------------------------------- ")
# Set DAC Value to 10000
if FAS_SetDACValue(nBdID, byChannel, bEnable, lDACValue) != FMM_OK:
    print("Function(FAS_SetDACValue) was failed.")
```
[EN]  
You can set the DAC conversion value using the FAS_SetDACValue() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'channel number', 'whether to enable the DAC function', 'DAC conversion value'

[KR]  
FAS_SetDACValue() 함수를 사용하여 DAC 변환 값을 설정할 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', '채널 번호', 'DAC 기능 활성화 여부 ', 'DAC 변환 값'

## 3. Get DAC value
```python
print("---------------------------------- ")
# Get DAC Value
status_result, Enable, Value = FAS_GetDACValue(nBdID, 0)
if status_result != FMM_OK:
    print("Function(FAS_GetDACValue) was failed.")
```
[EN]  
You can read the DAC value using the FAS_GetDACValue() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'channel number'
AND Meaning of each return value is as follows sequentially:
'return code', 'DAC function enabled', 'DAC value'

[KR]  
FAS_GetDACValue() 함수를 사용하여 DAC 값을 읽어올 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', '채널 번호'
그리고, 해당 함수의 반환값은 순차적으로 다음을 의미합니다.
'함수 리턴코드', 'DAC 기능 활성화 여부', 'DAC 값'

## 4. Etc
[EN]  
1. Please refer to the [01.ConnectionExam] project document for function descriptions on connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.