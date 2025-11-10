# SetOutputExam

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
2. Initialize all Output bits(16).
3. Configure Output bits.
4. Simultaneously configure Output bits and initialize Output bits.
5. Close connection.

[KR]  
1. 장치 연결.
2. 모든 Output bit 초기화(16 Output).
3. Output bit 설정.
4. Output bit 설정과 Output bit 초기화 동시 진행.
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

## 2. Initialize output bit (16 Output)
```python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Fastech's product which has Input (or Output) only (Ezi-IO-I16, Ezi-IO-O16, Ezi-IO-I32, Ezi-IO-O32...), BitMask of Input (or Output) starts from 0x01,	~~
#~ However, for Input+Output mixed products (Ezi-IO-I8O8, Ezi-IO-I16O16, etc.), the BitMask of Output is allocated after the BitMasks of Input.				~~
#~ Ezi-IO-I8O8, for example, the BitMask of Input 0 is 0x0001, and the BitMask of Output 0 is 0x0100.														~~
#~ For detailed allocation methods, please refer to Section 2.3 of the "doc.md" file of this example.														~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Fastech의 Input/Output 단일 제품 (Ezi-IO-I16, Ezi-IO-O16, Ezi-IO-I32, Ezi-IO-O32 등)은 Input과 Output의 BitMask가 각각 0x01부터 시작하지만,				   ~~
#~ Input+Output 혼합 제품 (Ezi-IO-I8O8, Ezi-IO-I16O16 등)은 Input의 BitMask를 전부 할당한 뒤, Output의 BitMask가 이어서 할당되어있습니다.						 ~~
#~ 예를들어 Ezi-IO-I8O8의 Input 0번의 BitMask는 0x0001, Output 0번의 BitMask는 0x0100입니다.																   ~~ 
#~ 자세한 할당 방식은 본 예제의 "doc.md"파일 2.3절을 참고 부탁드립니다.																							 ~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("-----------------------------------------")
print("Clearing All outputs (bit 0 ~ bit 15.)")
uSetMask = 0x00
uClrMask = 0xFFFF

if FAS_SetOutput(nBdID, uSetMask, uClrMask) != FMM_OK:
    print("Function(FAS_SetOutput) was failed.")
else:
    print("FAS_SetOutput Success!")

# Check OutputPin Status
status_result, uOutput, uStatus = FAS_GetOutput(nBdID)
if status_result != FMM_OK:
    print("Function(FAS_GetOutput) was failed.")
else:
    for i in range(OUTPUTPIN):
        bON = (uOutput & (0x01 << i)) != 0
        print("OutPin[%d] = %s" % (i, "ON" if bON else "OFF"))
```
[EN]  
You can set the Output bits using the FAS_SetOutput() function.
You can read the Output bits using the FAS_GetOutput() function.
The above source code initializes all Output bits (16 Outputs).

[KR]  
FAS_SetOutput() 함수를 사용하여 Output bit를 설정할 수 있습니다.
FAS_GetOutput() 함수를 사용하여 Output bit를 읽을 수 있습니다.
위 소스 코드는 모든 Output bit(16 Output)를 초기화합니다.

### 2.1 FAS_SetOutput() send data logic
[EN]  
uSetMask is a Bitmask value for the Output bit to be Set (On).
uClrMask is a Bitmask value for the Output bit to be Reset (Off).
If the same bits in uSetMask and uClrMask are both 1, the setting for that bit is executed as Reset.

[KR]  
uSetMask는 Set(On) 시킬 Output bit에 대한 Bitmask 값입니다.
uClrMask는 Reset(Off)시킬 Output bit에 대한 Bitmask 값입니다.
uSetMask와 uClrMask의 동일한 bit가 둘 다 1일 경우, 해당 bit에 대한 설정은 Reset으로 실행합니다.

### 2.2 FAS_GetOutput() receive data logic
[EN]  
Output bits are written sequentially from LSB to MSB of uOutput.
For example, output bit 0 is written in the LSB, and output bit 31 is written in the MSB.
Operation status of trigger are written sequentially from LSB to MSB of uStatus.
For example, trigger status 0 is written in the LSB, and trigger status 31 is written in the MSB. (0: Off / 1: On)

[KR]  
uOutput의 LSB에 0번 Output bit부터 MSB에 31번 Output bit가 순차적으로 쓰여집니다.
uStatus의 LSB에 0번 Trigger의 동작 여부부터 MSB에 31번 Trigger의 동작 여부가 순차적으로 쓰여집니다. (0: Off / 1: On)

### 2.3 Bitmask logic of Fastech IO product

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

## 3. Set Output
```python
print("-----------------------------------------")
    print("Set output bit #0.")
    uSetMask = 0x01
    uClrMask = 0x00
    if FAS_SetOutput(nBdID, uSetMask, uClrMask) != FMM_OK:
        print("Function(FAS_SetOutput) was failed.")
    else:
        print("FAS_SetOutput Success!")

    # Check OutputPin Status

    status_result, uOutput, uStatus = FAS_GetOutput(nBdID)
    if status_result != FMM_OK:
        print("Function(FAS_GetOutput) was failed.")
    else:
        for i in range(OUTPUTPIN):
            bON = (uOutput & (0x01 << i)) != 0
            print("OutPin[%d] = %s" % (i, "ON" if bON else "OFF"))
```
[EN]  
Configure output bit 0.

[KR]  
0번 Output bit를 설정합니다.

## 4. Simultaneously set Output bits and initialize Output bits.
```python
print("-----------------------------------------")
print("Clear bit #0 and Set bit #3, #4, #5.")
uSetMask = 0x08 | 0x10 | 0x20
uClrMask = 0x01
if FAS_SetOutput(nBdID, uSetMask, uClrMask) != FMM_OK:
    print("Function(FAS_SetOutput) was failed.")
else:
    print("FAS_SetOutput Success!")

# Check OutputPin Status

status_result, uOutput, uStatus = FAS_GetOutput(nBdID)
if status_result != FMM_OK:
    print("Function(FAS_GetOutput) was failed.")
else:
    for i in range(OUTPUTPIN):
        bON = (uOutput & (0x01 << i)) != 0
        print("OutPin[%d] = %s" % (i, "ON" if bON else "OFF"))
```
[EN]  
Configure output bits 3, 4, and 5. (0x08 = 3, 0x10 = 4, 0x20 = 5)
Initialize output bit 0.

[KR]  
3번, 4번, 5번 Output bit를 설정합니다. (0x08 = 3, 0x10 = 4, 0x20 = 5)
0번 Output bit를 초기화합니다.

## 5. Etc
[EN]  
1. Please refer to the [01.ConnectionExam] project document for function descriptions on connecting and disconnecting devices.

[KR]  
1. 장치 연결 및 해제에 대한 함수 설명은 [01.ConnectionExam] 프로젝트 문서를 참고하시기 바랍니다.
