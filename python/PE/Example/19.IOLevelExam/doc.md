# IOLevelExam

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
2. Check IO Level information.
3. Configure IO Level.
4. Close connection.

[KR]  
1. 장치 연결.
2. IO Level 정보 읽기.
3. IO Level 설정.
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

## 2. Get IO level
```python
def GetIOLevel(nBdID: int) -> bool:

    print("----------------------------------")
    # [Before] Check IO Level Status
    status_result, uIOLevel = FAS_GetIOLevel(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetIOLevel) was failed.")
        return False
    print("Load IO Level Status : 0x%08x" % uIOLevel)

    for i in range(16):
        bLevel = (uIOLevel & (0x01 << i)) != 0
        print("I/O pin %d : %s" % (i, "High Active" if bLevel else "Low Active"))

    return True
```
[EN]  
With FAS_GetIOLevel() function, you can read the level information for each IO Pin.
IO level information is written sequentially from LSB to MSB of uIOLevel.
For example, IO level information of pin 0 is written in the LSB, and IO level information of pin 31 is written in the MSB.
0: Low Active Level / 1: High Active Level

[KR]  
FAS_GetIOLevel() 함수를 사용하여 각 IO Pin에 대해 설정된 Level을 읽을 수 있습니다.
uIOLevel의 LSB에 0번 Pin의 Level부터 MSB에 31번 31번 Pin의 Level이 순차적으로 쓰여집니다.
0: Low Active Level / 1: High Active Level을 의미합니다.

### 2.1 Bitmask logic of Fastech IO product 

||0x0001|0x0002|0x0004|0x0008|0x0010|0x0020|0x0040|0x0080|0x0100|0x0200|0x0400|0x0800|...|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Ezi-IO-I16|IN0|IN1|IN2|IN3|IN4|IN5|IN6|IN7|IN8|IN9|IN10|IN11|...|
|Ezi-IO-O16|OUT0|OUT1|OUT2|OUT3|OUT4|OUT5|OUT6|OUT7|OUT8|OUT9|OUT10|OUT11|...	|
|Ezi-IO-I8O8|IN0|IN1|IN2|IN3|IN4|IN5|IN6|IN7|OUT0|OUT1|OUT2|OUT3|...|


||0x0001|0x0002|0x0004|0x0008|...|0x10000|0x20000|0x40000|0x80000|...|
|---|---|---|---|---|---|---|---|---|---|---|
|Ezi-IO-I32|IN0|IN1|IN2|IN3|...|IN16|IN17|IN18|...|
|Ezi-IO-O32|OUT0|OUT1|OUT2|OUT3|...|OUT16|OUT17|OUT18|...|
|Ezi-IO-I16O16|IN0|IN1|IN2|IN3|...|OUT0|OUT1|OUT2|...||

## 3. Set IO level
```python
def SetIOLevel(nBdID: int) -> bool:

    uIOLevel = 0x0000FF00

    print("----------------------------------")

    # Set IO Level Status
    if FAS_SetIOLevel(nBdID, uIOLevel) != FMM_OK:
        print("Function(FAS_SetIOLevel) was failed.")

    else:
        print("Set IO Level Status : 0x%08x" % uIOLevel)
    return True
```
[EN]  
You can set the level for each IO Pin using the FAS_SetIOLevel() function.
IO level information is written sequentially from LSB to MSB of uIOLevel.
For example, IO level information of pin 0 is written in the LSB, and IO level information of pin 31 is written in the MSB.
0: Low Active Level / 1: High Active Level.
The source code above sets Pins 0 to 7 to Low Active Level and Pins 8 to 15 to High Active Level. (16 Pins)

[KR]  
FAS_SetIOLevel() 함수를 사용하여 각 IO Pin에 대해 Level을 설정할 수 있습니다.
uIOLevel의 LSB에 0번 Pin의 Level부터 MSB에 31번 31번 Pin의 Level을 순차적으로 입력합니다.
0: Low Active Level / 1: High Active Level을 의미합니다.
위 소스 코드는 0~7번 Pin을 Low Active Level로, 8~15번 Pin을 High Active Level로 설정합니다. (16 Pin)

## 4. Etc
[EN]  
1. Please refer to the [01.ConnectionExam] project document for function descriptions on connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.