# ReadADExam

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
2. Read the AD conversion value of 1 channel.
3. Read the AD conversion value of 8 channels.
4. Close connection.

[KR]  
1. 장치 연결.
2. 1개 채널의 AD 변환 값 읽기.
3. 8개 채널의 AD 변환 값 읽기.
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

## 2. Read AD value (1 channel)
```python
def ReadADValue(nBdID: int) -> bool:
    byChannel = 0  # Channel 0

    print("---------------------------------- ")
    # Read AD (Channel 0)
    status_result, advalue = FAS_ReadADValue(nBdID, byChannel)
    if status_result != FMM_OK:
        print("Function(FAS_ReadADValue) was failed.")
    else:
        print("Read AD Success : Channel[%d] %d" % (byChannel + 1, advalue))
    return True
```
[EN]  
You can read the AD conversion value for one channel using the FAS_ReadADValue() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'channel number'
And Meaning of each return value is as follows sequentially:
'return code', 'AD conversion value'

[KR]  
FAS_ReadADValue() 함수를 사용하여 1개 채널에 대해 AD 변환 값 을 읽을 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', '채널 번호', 
그리고, 해당 함수의 반환값은 순차적으로 다음을 의미합니다.
'함수 리턴코드', 'AD 변환 값'

## 3. Read AD all value (8 channel)
```python
def ReadADAllValue(nBdID: int) -> bool:
    byOffset = 0  # Offset Should be 0

    print("---------------------------------- ")
    # Read All AD
    status_result, advalue = FAS_ReadADAllValue(nBdID, byOffset)
    if status_result != FMM_OK:
        print("Function(FAS_ReadADAllValue) was failed.")
    else:
        print("Read AD All Success")
        for i in range(8):
            print("Channel[%d] : %d" % (i + 1, advalue[i]))

        return True
```
[EN]  
You can read AD conversion values ​​for 8 channels using the FAS_ReadADAllValue() function.
Meaning of each argument is as follows sequentially:
'ID number of the board', 'Offset'
And Meaning of each return value is as follows sequentially:
'return code', 'AD conversion value'
Offset must be sent as 0.

[KR]  
FAS_ReadADAllValue() 함수를 사용하여 8개 채널에 대해 AD 변환 값 을 읽을 수 있습니다.
해당 함수의 각 인자는 순차적으로 다음을 의미합니다.
'해당 보드의 ID번호', 'Offset'
그리고, 해당 함수의 반환값은 순차적으로 다음을 의미합니다.
'함수 리턴코드', 'AD 변환 값'
Offset은 0으로 송신해야 합니다.

### 3.1 AD_BUFFER
[EN]  
AD_BUFFER is a structure that manages AD conversion values ​​for 8 channels.
AD_BUFFER can be found in the define file (MOTION_DEFINE.py).

[KR]  
AD_BUFFER는 8개 채널에 대해 AD 변환 값을 관리하는 구조체 입니다. 
AD_BUFFER는 define파일 (MOTION_DEFINE.py)에서 확인하실 수 있습니다.

## 4. Etc
[EN]  
1. Please refer to the [01.ConnectionExam] project document for function descriptions on connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.